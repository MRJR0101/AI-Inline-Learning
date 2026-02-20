# error_tracking.py
# Track your own AI error reduction using the AI Inline Learning pattern
# Run this against your results.csv to measure effectiveness

import csv
from collections import defaultdict
from datetime import datetime


RESULTS_FILE = 'results.csv'


def load_results(filepath):
    rows = []
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['occurred'] = row['occurred'].strip().lower() == 'true'
            row['session_date'] = datetime.strptime(row['session_date'], '%Y-%m-%d')
            rows.append(row)
    return rows


def calculate_reduction(rows):
    # Find the first occurrence of each error type
    # Then measure recurrence rate before vs after inline warning was added

    error_types = defaultdict(list)
    for row in rows:
        error_types[row['error_type']].append(row)

    results = []
    for error_type, events in error_types.items():
        events_sorted = sorted(events, key=lambda x: x['session_date'])

        # Find first time it did NOT occur (warning was in place)
        warning_added_index = None
        for i, e in enumerate(events_sorted):
            if not e['occurred']:
                warning_added_index = i
                break

        if warning_added_index is None:
            # Warning never added
            before_errors = sum(1 for e in events_sorted if e['occurred'])
            after_errors = 0
            after_total = 0
        else:
            before = events_sorted[:warning_added_index]
            after = events_sorted[warning_added_index:]
            before_errors = sum(1 for e in before if e['occurred'])
            after_errors = sum(1 for e in after if e['occurred'])
            after_total = len(after)

        before_total = warning_added_index if warning_added_index else len(events_sorted)

        results.append({
            'error_type': error_type,
            'before_errors': before_errors,
            'before_sessions': before_total,
            'after_errors': after_errors,
            'after_sessions': after_total,
        })

    return results


def print_report(results):
    total_before = sum(r['before_errors'] for r in results)
    total_after = sum(r['after_errors'] for r in results)
    total_sessions = sum(r['before_sessions'] + r['after_sessions'] for r in results)

    print('=' * 60)
    print('AI INLINE LEARNING - ERROR REDUCTION REPORT')
    print('=' * 60)

    for r in sorted(results, key=lambda x: x['before_errors'], reverse=True):
        before_rate = (r['before_errors'] / r['before_sessions'] * 100) if r['before_sessions'] else 0
        after_rate = (r['after_errors'] / r['after_sessions'] * 100) if r['after_sessions'] else 0
        reduction = before_rate - after_rate

        print(f"\n  {r['error_type']}")
        print(f"    Before warning: {r['before_errors']}/{r['before_sessions']} ({before_rate:.0f}% error rate)")
        print(f"    After warning:  {r['after_errors']}/{r['after_sessions']} ({after_rate:.0f}% error rate)")
        print(f"    Reduction:      {reduction:.0f} percentage points")

    print('\n' + '=' * 60)
    overall = ((total_before - total_after) / total_before * 100) if total_before else 0
    print(f'OVERALL: {total_before} errors before -> {total_after} errors after')
    print(f'REDUCTION: {overall:.1f}%')
    print(f'SESSIONS TRACKED: {total_sessions}')
    print('=' * 60)


if __name__ == '__main__':
    rows = load_results(RESULTS_FILE)
    results = calculate_reduction(rows)
    print_report(results)
