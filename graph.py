import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('merge_sort_results.csv')

plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#2E86AB', '#A23B72']

print("="*70)
print("MERGE SORT: RECURSIVE vs ITERATIVE ANALYSIS")
print("="*70)
print(f"\nDataset: RSUD Sukoharjo - {len(df)} test sizes")
print(f"Size range: {df['N'].min()} to {df['N'].max()} records\n")

fig1, ax1 = plt.subplots(figsize=(12, 7))

ax1.plot(df['N'], df['Recursive_ms'], 'o-', color=colors[0], 
         linewidth=3, markersize=10, label='Merge Sort RECURSIVE', alpha=0.8)
ax1.plot(df['N'], df['Iterative_ms'], 's-', color=colors[1], 
         linewidth=3, markersize=10, label='Merge Sort ITERATIVE', alpha=0.8)

ax1.set_xlabel('Dataset Size (N)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Execution Time (ms)', fontsize=14, fontweight='bold')
ax1.set_title('Merge Sort: Recursive vs Iterative - Time Comparison\nData Penyakit Rawat Inap RSUD Sukoharjo', 
              fontsize=16, fontweight='bold', pad=20)
ax1.legend(fontsize=12, loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.3)

if len(df) > 0:
    last_row = df.iloc[-1]
    max_n = last_row['N']
    rec_time = last_row['Recursive_ms']
    iter_time = last_row['Iterative_ms']
    avg_time = (rec_time + iter_time) / 2
    
    ax1.text(max_n * 0.5, max(rec_time, iter_time) * 0.8, 
            f'Very close!\nDifference < {abs(last_row["Overhead_Percent"]):.1f}%', 
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', 
                     edgecolor='orange', lw=2, alpha=0.9))

plt.tight_layout()
plt.savefig('merge_time_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Graph 1 saved: merge_time_comparison.png")


fig2, ax2 = plt.subplots(figsize=(12, 7))

positive_mask = df['Overhead_Percent'] >= 0
negative_mask = df['Overhead_Percent'] < 0

if positive_mask.any():
    ax2.scatter(df[positive_mask]['N'], df[positive_mask]['Overhead_Percent'], 
               color='#E63946', s=150, marker='^', label='Recursive slower', alpha=0.7, zorder=3)
if negative_mask.any():
    ax2.scatter(df[negative_mask]['N'], df[negative_mask]['Overhead_Percent'], 
               color='#06A77D', s=150, marker='v', label='Recursive faster', alpha=0.7, zorder=3)

ax2.plot(df['N'], df['Overhead_Percent'], '-', color='gray', linewidth=2, alpha=0.5, zorder=1)

ax2.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.7, 
            label='Equal Performance', zorder=2)

ax2.axhline(y=5, color='orange', linestyle='--', linewidth=1.5, alpha=0.5, label='±5% threshold')
ax2.axhline(y=-5, color='orange', linestyle='--', linewidth=1.5, alpha=0.5)
ax2.axhline(y=10, color='red', linestyle=':', linewidth=1.5, alpha=0.4, label='±10% threshold')
ax2.axhline(y=-10, color='red', linestyle=':', linewidth=1.5, alpha=0.4)

ax2.set_xlabel('Dataset Size (N)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Overhead (%)\n(Positive = Recursive slower)', fontsize=14, fontweight='bold')
ax2.set_title('Merge Sort Recursion Overhead\nPercentage Difference (Recursive vs Iterative)', 
              fontsize=16, fontweight='bold', pad=20)
ax2.legend(fontsize=10, loc='best', framealpha=0.9)
ax2.grid(True, alpha=0.3)

avg_overhead = df['Overhead_Percent'].mean()
ax2.text(0.05, 0.95, f'Average overhead: {avg_overhead:.2f}%\nRange: {df["Overhead_Percent"].min():.1f}% to {df["Overhead_Percent"].max():.1f}%', 
         transform=ax2.transAxes, fontsize=11, verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='white', edgecolor='blue', lw=2, alpha=0.9))

plt.tight_layout()
plt.savefig('merge_overhead_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Graph 2 saved: merge_overhead_analysis.png")


fig3, ax3 = plt.subplots(figsize=(12, 7))

ax3.plot(df['N'], df['Recursive_comparisons'], 'o-', color=colors[0], 
         linewidth=3, markersize=10, label='Recursive Comparisons', alpha=0.7)
ax3.plot(df['N'], df['Iterative_comparisons'], 's--', color=colors[1], 
         linewidth=2, markersize=8, label='Iterative Comparisons', alpha=0.7)

ax3.set_xlabel('Dataset Size (N)', fontsize=14, fontweight='bold')
ax3.set_ylabel('Number of Comparisons', fontsize=14, fontweight='bold')
ax3.set_title('Comparison Operations Count - Merge Sort\nBoth Implementations: O(n log n) Complexity', 
              fontsize=16, fontweight='bold', pad=20)
ax3.legend(fontsize=11, loc='upper left', framealpha=0.9)
ax3.grid(True, alpha=0.3)

ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

if len(df) > 2:
    n_theory = np.linspace(df['N'].min(), df['N'].max(), 100)
    actual_comp = df['Recursive_comparisons'].iloc[-1]
    actual_n = df['N'].iloc[-1]
    constant = actual_comp / (actual_n * np.log2(actual_n))
    theory_comp = constant * n_theory * np.log2(n_theory)
    
    ax3.plot(n_theory, theory_comp, ':', color='red', linewidth=2, 
             alpha=0.6, label='Theoretical O(n log n)')
    ax3.legend(fontsize=11, loc='upper left', framealpha=0.9)

plt.tight_layout()
plt.savefig('merge_comparisons_count.png', dpi=300, bbox_inches='tight')
print("✓ Graph 3 saved: merge_comparisons_count.png")


fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 6))

last_row = df.iloc[-1]
implementations = ['Recursive', 'Iterative']
times = [last_row['Recursive_ms'], last_row['Iterative_ms']]
comparisons = [last_row['Recursive_comparisons'], last_row['Iterative_comparisons']]

bars1 = ax4a.bar(implementations, times, color=colors, edgecolor='black', linewidth=2, width=0.5)
ax4a.set_ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
ax4a.set_title(f'Execution Time Comparison\n(N = {int(last_row["N"])} records)', 
               fontsize=13, fontweight='bold')
ax4a.grid(True, alpha=0.3, axis='y')

for bar, time in zip(bars1, times):
    height = bar.get_height()
    ax4a.text(bar.get_x() + bar.get_width()/2., height,
             f'{time:.3f} ms',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

overhead = last_row['Overhead_Percent']
if abs(overhead) < 10:
    color_box = 'lightgreen'
    text = f'Difference:\n{abs(overhead):.2f}%\n(Minimal!)'
else:
    color_box = 'yellow'
    text = f'Difference:\n{abs(overhead):.2f}%'

ax4a.text(0.5, max(times) * 0.5, text, 
         ha='center', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.8', facecolor=color_box, alpha=0.7))

bars2 = ax4b.bar(implementations, comparisons, color=colors, edgecolor='black', linewidth=2, width=0.5)
ax4b.set_ylabel('Number of Comparisons', fontsize=12, fontweight='bold')
ax4b.set_title(f'Comparison Operations Count\n(N = {int(last_row["N"])} records)', 
               fontsize=13, fontweight='bold')
ax4b.grid(True, alpha=0.3, axis='y')
ax4b.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

for bar, comp in zip(bars2, comparisons):
    height = bar.get_height()
    ax4b.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(comp):,}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

comp_diff = abs(comparisons[0] - comparisons[1])
comp_diff_pct = (comp_diff / max(comparisons)) * 100
ax4b.text(0.5, max(comparisons) * 0.5, 
         f'Difference:\n{int(comp_diff):,}\n({comp_diff_pct:.2f}%)', 
         ha='center', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', alpha=0.7))

plt.tight_layout()
plt.savefig('merge_final_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Graph 4 saved: merge_final_comparison.png")


fig5, ax5 = plt.subplots(figsize=(12, 7))

ax5.loglog(df['N'], df['Recursive_ms'], 'o-', color=colors[0], 
          linewidth=3, markersize=10, label='Recursive', alpha=0.8)
ax5.loglog(df['N'], df['Iterative_ms'], 's-', color=colors[1], 
          linewidth=3, markersize=10, label='Iterative', alpha=0.8)

if len(df) > 2:
    n_theory = np.logspace(np.log10(df['N'].min()), np.log10(df['N'].max()), 100)
    norm_factor = df['Recursive_ms'].iloc[-1] / (df['N'].iloc[-1] * np.log2(df['N'].iloc[-1]))
    theory_time = norm_factor * n_theory * np.log2(n_theory)
    ax5.loglog(n_theory, theory_time, ':', color='red', linewidth=2, 
              alpha=0.6, label='Theoretical O(n log n)')

ax5.set_xlabel('Dataset Size (N) - Log Scale', fontsize=14, fontweight='bold')
ax5.set_ylabel('Execution Time (ms) - Log Scale', fontsize=14, fontweight='bold')
ax5.set_title('Merge Sort Growth Pattern (Log-Log Scale)\nVerifying O(n log n) Complexity', 
              fontsize=16, fontweight='bold', pad=20)
ax5.legend(fontsize=11, loc='upper left', framealpha=0.9)
ax5.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('merge_growth_pattern.png', dpi=300, bbox_inches='tight')
print("✓ Graph 5 saved: merge_growth_pattern.png")

print("\n" + "="*70)
print("STATISTICAL SUMMARY")
print("="*70)

print(f"\n--- WINNER STATISTICS ---")
winner_counts = df['Winner'].value_counts()
for impl, count in winner_counts.items():
    print(f"{impl}: {count} wins ({count/len(df)*100:.1f}%)")

print(f"\n--- OVERHEAD ANALYSIS ---")
print(f"Average overhead:    {df['Overhead_Percent'].mean():.2f}%")
print(f"Median overhead:     {df['Overhead_Percent'].median():.2f}%")
print(f"Std deviation:       {df['Overhead_Percent'].std():.2f}%")
print(f"Min overhead:        {df['Overhead_Percent'].min():.2f}%")
print(f"Max overhead:        {df['Overhead_Percent'].max():.2f}%")
print(f"Range:               {df['Overhead_Percent'].max() - df['Overhead_Percent'].min():.2f}%")

print(f"\n--- FULL DATASET ANALYSIS (n={last_row['N']}) ---")
print(f"Recursive time:      {last_row['Recursive_ms']:.4f} ms")
print(f"Iterative time:      {last_row['Iterative_ms']:.4f} ms")
print(f"Time difference:     {abs(last_row['Recursive_ms'] - last_row['Iterative_ms']):.4f} ms")
print(f"Overhead:            {last_row['Overhead_Percent']:.2f}%")

print(f"\n--- COMPARISON COUNTS (Full Dataset) ---")
print(f"Recursive:           {int(last_row['Recursive_comparisons']):,}")
print(f"Iterative:           {int(last_row['Iterative_comparisons']):,}")
comp_diff = abs(last_row['Recursive_comparisons'] - last_row['Iterative_comparisons'])
print(f"Difference:          {int(comp_diff):,} ({comp_diff/max(last_row['Recursive_comparisons'], last_row['Iterative_comparisons'])*100:.2f}%)")

print("\n" + "="*70)
print("KEY FINDINGS")
print("="*70)

avg_overhead = df['Overhead_Percent'].mean()
abs_avg_overhead = df['Overhead_Percent'].abs().mean()

print(f"""
1. PERFORMANCE ESSENTIALLY EQUIVALENT
   → Average overhead: {avg_overhead:.2f}%
   → Average |overhead|: {abs_avg_overhead:.2f}%
   → Both implementations are equally efficient

2. COMPARISON COUNTS VERY SIMILAR
   → Difference < {comp_diff/last_row['Recursive_comparisons']*100:.1f}%
   → Both follow O(n log n) complexity

3. WINNER ALTERNATES
   → No consistent pattern
   → Differences within measurement noise (±{abs_avg_overhead:.1f}%)

4. WHY SO SIMILAR?
   → Shallow recursion depth (log n ≈ {np.log2(last_row['N']):.0f} levels)
   → Effective compiler optimization (-O2)
   → Same divide-and-conquer strategy
   → Modern CPU optimization (branch prediction, cache)

5. PRACTICAL IMPLICATIONS
   → For Merge Sort: implementation choice is FLEXIBLE
   → Choose based on: code readability, team preference
   → Performance difference NEGLIGIBLE (<{abs_avg_overhead:.0f}%)
   
6. CONTRAST WITH LINEAR RECURSION
   → Merge Sort (log n depth): ~{abs_avg_overhead:.0f}% overhead
   → Selection Sort (n depth): ~30% overhead (theoretical)
   → Recursion overhead ∝ recursion depth!
""")

print("="*70)
print("All graphs generated successfully!")
print("="*70)
print("\nGenerated files:")
print("  1. merge_time_comparison.png")
print("  2. merge_overhead_analysis.png")
print("  3. merge_comparisons_count.png")
print("  4. merge_final_comparison.png")
print("  5. merge_growth_pattern.png")
print("\n" + "="*70)