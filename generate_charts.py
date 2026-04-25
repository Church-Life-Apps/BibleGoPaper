"""
Generate figures for the BibleGoAI research paper.
Extracts metrics from BHT JSON files and produces PDF charts.
"""

import json
import os
import glob
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Default to a sibling BibleGoAI checkout; override with BIBLEGO_AI_REPO env var
# when generating charts in a different environment.
REPO = os.environ.get("BIBLEGO_AI_REPO", os.path.expanduser("~/BibleGoAI"))
FIGURES_DIR = os.environ.get("BIBLEGO_PAPER_FIGURES_DIR",
                              os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures"))
os.makedirs(FIGURES_DIR, exist_ok=True)

COLORS = {
    'nt': '#2980b9',
    'ot': '#27ae60',
    'split_a': '#e67e22',
    'split_b': '#8e44ad',
    'tier1': '#2980b9',
    'tier2': '#27ae60',
    'tier3': '#f39c12',
}

def load_bht_metrics(directory, metric_keys=None):
    """Load metrics from all BHT JSON files in a directory (recursively)."""
    if metric_keys is None:
        metric_keys = ['qualityScore', 'wordCount', 'quoteTokenProportion',
                       'commentaryAccuracyScore', 'verseAccuracyScore',
                       'commentatorTierSimilarities', 'generationAttempt']
    
    records = []
    pattern = os.path.join(directory, '**', '*.json')
    files = glob.glob(pattern, recursive=True)
    
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        
        best = data.get('bestBHT', data.get('bestBht', None))
        if best is None:
            continue
        
        record = {}
        for key in metric_keys:
            record[key] = best.get(key, None)

        # Parse book / chapter / verse from filename so we can pair split-a
        # and split-b records per-verse. Filenames look like
        # '<book> <chap> <verse> bht.json', e.g. '1 Kings 1 1 bht.json'.
        fname = os.path.basename(fpath)
        base = fname[:-len(' bht.json')] if fname.endswith(' bht.json') else fname[:-5]
        parts = base.rsplit(' ', 2)
        if len(parts) == 3:
            record['book'] = parts[0]
            try:
                record['chapter'] = int(parts[1])
                record['verse'] = int(parts[2])
            except ValueError:
                record['chapter'] = parts[1]
                record['verse'] = parts[2]
        
        # Also collect attempt-level data
        attempts = data.get('bhtAttempts', [])
        attempt_scores = []
        for att in attempts:
            s = att.get('qualityScore', None)
            if s is not None:
                attempt_scores.append((att.get('generationAttempt', 0), s))
        record['attemptScores'] = attempt_scores
        
        records.append(record)
    
    return records


def fig_quality_distribution(nt_records, ot_records):
    """Figure 4: Quality score distribution histogram."""
    nt_scores = [r['qualityScore'] for r in nt_records if r.get('qualityScore')]
    ot_scores = [r['qualityScore'] for r in ot_records if r.get('qualityScore')]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    bins = np.linspace(
        min(min(nt_scores, default=0), min(ot_scores, default=0)),
        max(max(nt_scores, default=3), max(ot_scores, default=3)),
        40
    )
    ax.hist(nt_scores, bins=bins, alpha=0.6, label=f'NT (n={len(nt_scores):,})',
            color=COLORS['nt'], edgecolor='white', linewidth=0.3)
    ax.hist(ot_scores, bins=bins, alpha=0.6, label=f'OT (n={len(ot_scores):,})',
            color=COLORS['ot'], edgecolor='white', linewidth=0.3)
    ax.set_xlabel('Commentary Accuracy', fontsize=9)
    ax.set_ylabel('Number of Verses', fontsize=9)
    ax.set_title('BHT Commentary Accuracy Distribution', fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'quality_distribution.pdf'), dpi=300)
    plt.close(fig)
    print(f"  Quality distribution: NT={len(nt_scores)}, OT={len(ot_scores)}")


def fig_attempt_trajectory(records):
    """Figure 5: Average commentary-accuracy score by generation attempt number."""
    attempt_buckets = {}
    for r in records:
        for attempt_num, score in r.get('attemptScores', []):
            if attempt_num not in attempt_buckets:
                attempt_buckets[attempt_num] = []
            attempt_buckets[attempt_num].append(score)
    
    if not attempt_buckets:
        print("  WARNING: No attempt data found, skipping attempt trajectory")
        return
    
    attempts = sorted(attempt_buckets.keys())
    means = [np.mean(attempt_buckets[a]) for a in attempts]
    stds = [np.std(attempt_buckets[a]) for a in attempts]
    counts = [len(attempt_buckets[a]) for a in attempts]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.errorbar(attempts, means, yerr=stds, fmt='o-', color=COLORS['nt'],
                capsize=3, markersize=5, linewidth=1.5, label='Mean ± Std')
    
    for i, (a, m, n) in enumerate(zip(attempts, means, counts)):
        ax.annotate(f'n={n:,}', (a, m), textcoords="offset points",
                    xytext=(0, 12), ha='center', fontsize=6, color='gray')
    
    ax.set_xlabel('Generation Attempt', fontsize=9)
    ax.set_ylabel('Commentary Accuracy', fontsize=9)
    ax.set_title('Commentary Accuracy by Generation Attempt', fontsize=10, fontweight='bold')
    ax.set_xticks(attempts)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'attempt_trajectory.pdf'), dpi=300)
    plt.close(fig)
    print(f"  Attempt trajectory: {len(attempts)} attempts, {sum(counts)} total data points")


def fig_strategy_comparison(regular, split_a, split_b):
    """Figure 6: Pipeline comparison (Regular vs Split combined).

    Split-A and Split-B are two stages of a single deployed pipeline whose
    per-verse outputs are concatenated and served together. We combine them
    per-verse (mean of the two scores, summed word counts) before comparing
    to the Regular pipeline.
    """
    # Build per-verse index for split-a and split-b so we can pair them.
    def key_of(r):
        return (r.get('book'), r.get('chapter'), r.get('verse'))
    sa_index = {key_of(r): r for r in split_a}
    split_combined = []
    for rb in split_b:
        k = key_of(rb)
        ra = sa_index.get(k)
        if ra is None:
            continue
        def safe(x, d=0.0):
            return x if isinstance(x, (int, float)) else d
        score_a = safe(ra.get('qualityScore'))
        score_b = safe(rb.get('qualityScore'))
        ca_a = safe(ra.get('commentaryAccuracyScore'))
        ca_b = safe(rb.get('commentaryAccuracyScore'))
        va_a = safe(ra.get('verseAccuracyScore'))
        va_b = safe(rb.get('verseAccuracyScore'))
        qp_a = safe(ra.get('quoteTokenProportion'))
        qp_b = safe(rb.get('quoteTokenProportion'))
        wc_a = safe(ra.get('wordCount'))
        wc_b = safe(rb.get('wordCount'))
        split_combined.append({
            'qualityScore': (score_a + score_b) / 2.0,
            'commentaryAccuracyScore': (ca_a + ca_b) / 2.0,
            'verseAccuracyScore': (va_a + va_b) / 2.0,
            'quoteTokenProportion': (qp_a + qp_b) / 2.0,
            'wordCount': wc_a + wc_b,
        })

    strategies = {}
    for name, records in [('Regular', regular), ('Split (combined)', split_combined)]:
        scores = [r['qualityScore'] for r in records if r.get('qualityScore')]
        ca_scores = [r['commentaryAccuracyScore'] for r in records if r.get('commentaryAccuracyScore')]
        va_scores = [r['verseAccuracyScore'] for r in records if r.get('verseAccuracyScore')]
        wc = [r['wordCount'] for r in records if r.get('wordCount')]
        qp = [r['quoteTokenProportion'] for r in records if r.get('quoteTokenProportion')]
        strategies[name] = {
            'quality': np.mean(scores) if scores else 0,
            'commentary_acc': np.mean(ca_scores) if ca_scores else 0,
            'verse_acc': np.mean(va_scores) if va_scores else 0,
            'word_count': np.mean(wc) if wc else 0,
            'quote_prop': np.mean(qp) if qp else 0,
            'n': len(scores),
        }

    fig, axes = plt.subplots(1, 3, figsize=(7, 2.8))
    names = list(strategies.keys())
    colors = [COLORS['ot'], COLORS['split_a']]
    
    # Commentary Accuracy
    vals = [strategies[n]['commentary_acc'] for n in names]
    axes[0].bar(names, vals, color=colors, edgecolor='white', linewidth=0.5)
    axes[0].set_ylabel('Score', fontsize=8)
    axes[0].set_title('Commentary Accuracy', fontsize=9, fontweight='bold')
    axes[0].tick_params(labelsize=7)
    
    # Word Count
    vals = [strategies[n]['word_count'] for n in names]
    axes[1].bar(names, vals, color=colors, edgecolor='white', linewidth=0.5)
    axes[1].set_ylabel('words', fontsize=8)
    axes[1].set_title('Word Count', fontsize=9, fontweight='bold')
    axes[1].tick_params(labelsize=7)
    
    # Quote Proportion
    vals = [strategies[n]['quote_prop'] for n in names]
    axes[2].bar(names, vals, color=colors, edgecolor='white', linewidth=0.5)
    axes[2].set_ylabel('%', fontsize=8)
    axes[2].set_title('Quote Proportion', fontsize=9, fontweight='bold')
    axes[2].tick_params(labelsize=7)
    
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'strategy_comparison.pdf'), dpi=300)
    plt.close(fig)
    
    for name, s in strategies.items():
        print(f"  {name}: quality={s['quality']:.3f}, commentary_acc={s['commentary_acc']:.3f}, "
              f"verse_acc={s['verse_acc']:.3f}, word_count={s['word_count']:.1f}, "
              f"quote_prop={s['quote_prop']:.1f}%, n={s['n']}")


def fig_tier_breakdown(nt_records, ot_records):
    """Figure 7: Commentator tier similarity breakdown."""
    datasets = {'NT': nt_records, 'OT': ot_records}
    tier_means = {}
    
    for name, records in datasets.items():
        t1, t2, t3 = [], [], []
        for r in records:
            tiers = r.get('commentatorTierSimilarities')
            if tiers and len(tiers) == 3:
                t1.append(tiers[0])
                t2.append(tiers[1])
                t3.append(tiers[2])
        tier_means[name] = {
            'Tier 1': np.mean(t1) if t1 else 0,
            'Tier 2': np.mean(t2) if t2 else 0,
            'Tier 3': np.mean(t3) if t3 else 0,
            'n': len(t1),
        }
    
    fig, ax = plt.subplots(figsize=(5, 3))
    x = np.arange(len(datasets))
    width = 0.25
    
    for i, (tier, color) in enumerate([('Tier 1', COLORS['tier1']),
                                        ('Tier 2', COLORS['tier2']),
                                        ('Tier 3', COLORS['tier3'])]):
        vals = [tier_means[name][tier] for name in datasets]
        bars = ax.bar(x + i * width, vals, width, label=tier, color=color,
                      edgecolor='white', linewidth=0.5)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=7)
    
    ax.set_xlabel('Testament', fontsize=9)
    ax.set_ylabel('Average Tier Similarity (%)', fontsize=9)
    ax.set_title('Commentator Tier Contribution', fontsize=10, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(list(datasets.keys()))
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'tier_breakdown.pdf'), dpi=300)
    plt.close(fig)
    
    for name, t in tier_means.items():
        print(f"  {name}: T1={t['Tier 1']:.1f}, T2={t['Tier 2']:.1f}, T3={t['Tier 3']:.1f} (n={t['n']})")


def fig_cross_model():
    """Figure 8: Cross-model comparison from groq output data."""
    comparison_file = os.path.join(REPO, "groq output", "poc_comparison.json")
    if not os.path.exists(comparison_file):
        print("  WARNING: poc_comparison.json not found, skipping cross-model chart")
        return
    
    with open(comparison_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract per-model scores
    models = {}
    if isinstance(data, list):
        for entry in data:
            for model_key in ['existing', 'groq', 'gpt4omini']:
                if model_key in entry:
                    if model_key not in models:
                        models[model_key] = {'scores': [], 'word_counts': [], 'quote_props': []}
                    m = entry[model_key]
                    if isinstance(m, dict):
                        if 'qualityScore' in m:
                            models[model_key]['scores'].append(m['qualityScore'])
                        if 'wordCount' in m:
                            models[model_key]['word_counts'].append(m['wordCount'])
                        if 'quoteTokenProportion' in m:
                            models[model_key]['quote_props'].append(m['quoteTokenProportion'])
    elif isinstance(data, dict):
        for verse, entry in data.items():
            for model_key in ['existing', 'groq', 'gpt4omini']:
                if model_key in entry:
                    if model_key not in models:
                        models[model_key] = {'scores': [], 'word_counts': [], 'quote_props': []}
                    m = entry[model_key]
                    if isinstance(m, dict):
                        if 'qualityScore' in m:
                            models[model_key]['scores'].append(m['qualityScore'])
                        if 'wordCount' in m:
                            models[model_key]['word_counts'].append(m['wordCount'])
                        if 'quoteTokenProportion' in m:
                            models[model_key]['quote_props'].append(m['quoteTokenProportion'])
    
    if not models:
        print("  WARNING: Could not parse cross-model data, skipping")
        return
    
    model_labels = {
        'existing': 'GPT-3.5',
        'groq': 'Llama 3.3',
        'gpt4omini': 'GPT-4o-mini'
    }
    
    fig, axes = plt.subplots(1, 2, figsize=(6, 2.8))
    names = [model_labels.get(k, k) for k in models.keys()]
    colors_list = [COLORS['nt'], COLORS['ot'], COLORS['split_a']]
    
    # Quality scores
    score_means = [np.mean(models[k]['scores']) if models[k]['scores'] else 0 for k in models]
    axes[0].bar(names, score_means, color=colors_list[:len(names)], edgecolor='white')
    axes[0].set_title('Commentary Accuracy', fontsize=9, fontweight='bold')
    axes[0].tick_params(labelsize=7)
    
    # Word counts
    wc_means = [np.mean(models[k]['word_counts']) if models[k]['word_counts'] else 0 for k in models]
    axes[1].bar(names, wc_means, color=colors_list[:len(names)], edgecolor='white')
    axes[1].set_title('Avg Word Count', fontsize=9, fontweight='bold')
    axes[1].tick_params(labelsize=7)
    
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, 'cross_model.pdf'), dpi=300)
    plt.close(fig)
    
    for k, v in models.items():
        label = model_labels.get(k, k)
        print(f"  {label}: score={np.mean(v['scores']):.3f}, wc={np.mean(v['word_counts']):.1f}, "
              f"qp={np.mean(v['quote_props']):.1f}% (n={len(v['scores'])})")


def print_aggregate_stats(nt_records, ot_records, split_a_records, split_b_records):
    """Print aggregate statistics for populating paper tables."""
    print("\n=== AGGREGATE STATS FOR PAPER TABLES ===\n")
    
    for name, records in [('NT', nt_records), ('OT Regular', ot_records),
                          ('OT Split-A', split_a_records), ('OT Split-B', split_b_records)]:
        scores = [r['qualityScore'] for r in records if r.get('qualityScore')]
        wc = [r['wordCount'] for r in records if r.get('wordCount')]
        qp = [r['quoteTokenProportion'] for r in records if r.get('quoteTokenProportion')]
        ca = [r['commentaryAccuracyScore'] for r in records if r.get('commentaryAccuracyScore')]
        va = [r['verseAccuracyScore'] for r in records if r.get('verseAccuracyScore')]
        
        print(f"--- {name} (n={len(records)}) ---")
        if scores:
            print(f"  Commentary Accuracy: {np.mean(scores):.3f} ± {np.std(scores):.3f} "
                  f"(median={np.median(scores):.3f}, min={np.min(scores):.3f}, max={np.max(scores):.3f})")
        if wc:
            print(f"  Word Count: {np.mean(wc):.1f} ± {np.std(wc):.1f} "
                  f"(median={np.median(wc):.1f}, min={np.min(wc)}, max={np.max(wc)})")
        if qp:
            print(f"  Quote Proportion: {np.mean(qp):.1f}% ± {np.std(qp):.1f}%")
        if ca:
            print(f"  Commentary Accuracy: {np.mean(ca):.3f} ± {np.std(ca):.3f}")
        if va:
            print(f"  Verse Accuracy: {np.mean(va):.3f} ± {np.std(va):.3f}")
        print()


def main():
    print("Loading BHT data...")
    
    # NT data
    nt_dir = os.path.join(REPO, "bht", "nt bht v3")
    print(f"  Loading NT from: {nt_dir}")
    nt_records = load_bht_metrics(nt_dir) if os.path.exists(nt_dir) else []
    print(f"  NT records: {len(nt_records)}")
    
    # OT data
    ot_regular_dir = os.path.join(REPO, "bht", "ot bht v1", "bht", "regular")
    ot_split_a_dir = os.path.join(REPO, "bht", "ot bht v1", "bht", "split-a")
    ot_split_b_dir = os.path.join(REPO, "bht", "ot bht v1", "bht", "split-b")
    
    print(f"  Loading OT Regular from: {ot_regular_dir}")
    ot_records = load_bht_metrics(ot_regular_dir) if os.path.exists(ot_regular_dir) else []
    print(f"  OT Regular records: {len(ot_records)}")
    
    print(f"  Loading OT Split-A from: {ot_split_a_dir}")
    split_a_records = load_bht_metrics(ot_split_a_dir) if os.path.exists(ot_split_a_dir) else []
    print(f"  OT Split-A records: {len(split_a_records)}")
    
    print(f"  Loading OT Split-B from: {ot_split_b_dir}")
    split_b_records = load_bht_metrics(ot_split_b_dir) if os.path.exists(ot_split_b_dir) else []
    print(f"  OT Split-B records: {len(split_b_records)}")
    
    # Build per-verse-combined OT corpus (regular + split-as-mean) so OT-corpus
    # figures reflect the full 23,145-verse OT corpus rather than only the
    # 10,492 regular-pipeline subset. Split per-verse score is the mean of
    # split-a and split-b commentaryAccuracyScore (qualityScore in legacy);
    # tier similarities are averaged element-wise; word count is summed.
    def _key(r):
        return (r.get('book'), r.get('chapter'), r.get('verse'))
    sa_idx = {_key(r): r for r in split_a_records}
    split_combined_records = []
    for rb in split_b_records:
        ra = sa_idx.get(_key(rb))
        if ra is None:
            continue
        def _avg(a, b):
            if a is None and b is None: return None
            if a is None: return b
            if b is None: return a
            return (a + b) / 2.0
        ts_a = ra.get('commentatorTierSimilarities')
        ts_b = rb.get('commentatorTierSimilarities')
        ts_combined = None
        if ts_a and ts_b and len(ts_a) == 3 and len(ts_b) == 3:
            ts_combined = [(ts_a[i] + ts_b[i]) / 2.0 for i in range(3)]
        wc_a = ra.get('wordCount') or 0
        wc_b = rb.get('wordCount') or 0
        split_combined_records.append({
            'book': ra.get('book'),
            'chapter': ra.get('chapter'),
            'verse': ra.get('verse'),
            'qualityScore': _avg(ra.get('qualityScore'), rb.get('qualityScore')),
            'commentaryAccuracyScore': _avg(ra.get('commentaryAccuracyScore'), rb.get('commentaryAccuracyScore')),
            'verseAccuracyScore': _avg(ra.get('verseAccuracyScore'), rb.get('verseAccuracyScore')),
            'wordCount': wc_a + wc_b,
            'quoteTokenProportion': _avg(ra.get('quoteTokenProportion'), rb.get('quoteTokenProportion')),
            'commentatorTierSimilarities': ts_combined,
        })
    ot_per_verse_records = ot_records + split_combined_records
    print(f"  OT per-verse-combined records: {len(ot_per_verse_records)} (regular {len(ot_records)} + split-combined {len(split_combined_records)})")

    # Combine for some analyses
    all_records = nt_records + ot_per_verse_records

    print(f"\nTotal records loaded: {len(all_records) + len(split_a_records) + len(split_b_records)}")
    print("\n--- Generating figures ---\n")
    
    print("1. Quality Distribution (Fig 4):")
    fig_quality_distribution(nt_records, ot_per_verse_records)
    
    print("\n2. Attempt Trajectory (Fig 5):")
    fig_attempt_trajectory(all_records)
    
    print("\n3. Strategy Comparison (Fig 6):")
    fig_strategy_comparison(ot_records, split_a_records, split_b_records)
    
    print("\n4. Tier Breakdown (Fig 7):")
    fig_tier_breakdown(nt_records, ot_per_verse_records)
    
    print("\n5. Cross-Model Comparison (Fig 8):")
    fig_cross_model()
    
    # Print aggregate stats
    print_aggregate_stats(nt_records, ot_records, split_a_records, split_b_records)
    print()
    print("=== OT per-verse-combined (regular + split-as-mean) ===")
    print_aggregate_stats([], ot_per_verse_records, [], [])
    
    print(f"\nAll figures saved to: {FIGURES_DIR}")
    print("Done!")


if __name__ == '__main__':
    main()
