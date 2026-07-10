# -*- coding: utf-8 -*-
"""
Extended predicted-window prime generator
----------------------------------------
Extends the successful predicted-window experiment to larger limits.
Tests whether the 100% coverage persists at 10,000, 20,000, and 50,000.

Also records the first failure point if it appears.
"""

import os
from collections import Counter
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

OUT = "output"
os.makedirs(OUT, exist_ok=True)


def predicted_window(scale):
    lo = max(1, int(round(0.1108 * scale - 5.34)))
    hi = max(lo + 5, int(round(0.3955 * scale + 7.54)))
    return lo, hi


def k_values_for_scale(scale):
    if scale <= 100:
        return [2]
    if scale <= 200:
        return [2, 3]
    if scale <= 300:
        return [2, 3, 4]
    if scale <= 400:
        return [2, 3, 4, 5]
    if scale <= 800:
        return [2, 3, 4, 5, 6]
    if scale <= 5000:
        return [2, 3, 4, 5, 6, 7]
    if scale <= 20000:
        return [2, 3, 4, 5, 6, 7, 8]
    return [2, 3, 4, 5, 6, 7, 8, 9]


def score_candidate(x, current_max, scale):
    return abs(x - current_max) + 0.15 * abs(x - scale)


def generate(limit, seed=(1, 2, 3), require_odd_result=True):
    actual = list(sp.primerange(2, limit + 1))
    generated = sorted(set(seed))
    k_usage = Counter()
    b_usage = Counter()
    witness = {}

    while True:
        current_max = max(generated)
        scale = current_max
        lo, hi = predicted_window(scale)
        k_vals = sorted(k_values_for_scale(scale), key=lambda k: (-k_usage[k], k))
        b_pool = [x for x in generated if lo <= x <= hi]
        if not b_pool:
            b_pool = [x for x in generated if x >= lo]
        if not b_pool:
            b_pool = [1, 2, 3]
        b_pool = sorted(set(b_pool), key=lambda b: (-b_usage[b], score_candidate(b, current_max, scale), b))

        best = None
        best_score = None
        best_expr = None
        for a in generated:
            if a < lo:
                continue
            for b in b_pool:
                for k in k_vals:
                    for op in (+1, -1):
                        cand = a * k + op * b
                        if cand <= current_max or cand < 2 or cand > limit:
                            continue
                        if require_odd_result and cand > 2 and cand % 2 == 0:
                            continue
                        if sp.isprime(cand) and cand not in generated:
                            sc = score_candidate(cand, current_max, scale)
                            if best_score is None or sc < best_score:
                                best = cand
                                best_score = sc
                                best_expr = (a, k, '+' if op == 1 else '-', b, lo, hi)
        if best is None:
            break

        generated = sorted(set(generated + [best]))
        witness[best] = best_expr
        a, k, op, b, lo, hi = best_expr
        k_usage[k] += 1
        b_usage[b] += 1

    gen_primes = sorted([x for x in generated if x >= 2 and sp.isprime(x)])
    missing = sorted(set(actual) - set(gen_primes))
    first_failure = missing[0] if missing else None

    return {
        'limit': limit,
        'actual_count': len(actual),
        'generated_count': len(gen_primes),
        'success_rate': 100 * len(set(actual) & set(gen_primes)) / len(actual),
        'missing_count': len(missing),
        'first_failure': first_failure,
        'first_missing': missing[:10],
        'k_usage': dict(k_usage),
        'top_b_usage': dict(Counter(b_usage).most_common(10)),
        'witness': witness,
    }


limits = [1000, 5000, 10000, 20000, 50000]
rows = []
last_result = None
for lim in limits:
    res = generate(lim)
    last_result = res
    rows.append({
        'limit': lim,
        'actual_count': res['actual_count'],
        'generated_count': res['generated_count'],
        'success_rate': res['success_rate'],
        'missing_count': res['missing_count'],
        'first_failure': res['first_failure'],
        'first_missing': ','.join(map(str, res['first_missing'])),
        'k_usage': str(res['k_usage']),
    })

summary = pd.DataFrame(rows)
summary.to_csv(os.path.join(OUT, 'predicted_window_extended_summary.csv'), index=False)

plt.figure(figsize=(10, 6))
plt.plot(summary['limit'], summary['success_rate'], 'o-', lw=2, color='darkgreen')
plt.xscale('log')
plt.xlabel('Limit (log scale)')
plt.ylabel('Success rate (%)')
plt.title('Extended predicted-window prime coverage')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'predicted_window_extended_coverage.png'), dpi=160)

if last_result is not None:
    witness_rows = []
    for p, expr in sorted(last_result['witness'].items()):
        a, k, op, b, lo, hi = expr
        witness_rows.append({'prime': p, 'a': a, 'k': k, 'op': op, 'b': b, 'window_lo': lo, 'window_hi': hi, 'expression': f'{a}*{k}{op}{b}'})
    pd.DataFrame(witness_rows).to_csv(os.path.join(OUT, 'predicted_window_extended_witnesses_last_limit.csv'), index=False)

print(summary.to_string(index=False))
print('\nLast-limit usage summary:')
print(last_result['k_usage'])
print(last_result['top_b_usage'])
