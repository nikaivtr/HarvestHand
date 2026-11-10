import csv

rows = list(csv.DictReader(open('crossval_results.csv')))
print(f'Total rows: {len(rows)}')

methods = {}
for r in rows:
    methods.setdefault(r['method'], []).append(r)

for m, rs in methods.items():
    print(f'\n--- {m.upper()} ---')
    print(f'  Total: {len(rs)}')
    correct_raw = sum(1 for r in rs if r['predicted'] == r['actual'])
    print(f'  Raw accuracy: {correct_raw/len(rs)*100:.1f}% ({correct_raw}/{len(rs)})')
    accepted = [r for r in rs if r['accepted']]
    correct_acc = sum(1 for r in rs if r['accepted'] and r['predicted'] == r['actual'])
    print(f'  Coverage: {len(accepted)/len(rs)*100:.1f}% ({len(accepted)}/{len(rs)})')
    print(f'  Correct among accepted: {correct_acc/len(accepted)*100:.1f}% ({correct_acc}/{len(accepted)})')
    false_acc = sum(1 for r in rs if r['accepted'] and r['predicted'] != r['actual'])
    print(f'  False accepts: {false_acc}')
    print(f'  False-accept rate: {false_acc/len(rs)*100:.1f}%')
    rejected = sum(1 for r in rs if not r['accepted'])
    print(f'  Rejected: {rejected} ({rejected/len(rs)*100:.1f}%)')
    correct_rejected = sum(1 for r in rs if not r['accepted'] and r['predicted'] == r['actual'])
    print(f'  Correct but rejected: {correct_rejected}')
    
    gaps = [float(r['gap']) for r in rs if r['gap'] is not None]
    if gaps:
        print(f'  Mean gap: {sum(gaps)/len(gaps):.6f}')
        print(f'  Min gap: {min(gaps):.6f}')
        print(f'  Max gap: {max(gaps):.6f}')
    
    for cls in ['pechay_plant', 'monggo_plant']:
        cls_rows = [r for r in rs if r['actual'] == cls]
        cls_correct = sum(1 for r in cls_rows if r['predicted'] == cls)
        print(f'  {cls}: {cls_correct}/{len(cls_rows)} correct ({cls_correct/len(cls_rows)*100:.1f}%)')

# Misclassified by all methods
print('\n=== MISCLASSIFIED BY ALL METHODS ===')
from collections import defaultdict
misclassified = {}
for r in rows:
    if r['predicted'] != r['actual']:
        misclassified.setdefault(r['path'], set()).add(r['method'])
for path, methods_set in misclassified.items():
    if len(methods_set) == 3:
        print(f'  {path.split(chr(92))[-1]}')

# Misclassified by any method
print('\n=== ALL MISCLASSIFICATIONS ===')
for r in sorted(rows, key=lambda x: (x['actual'], x['method'])):
    if r['predicted'] != r['actual']:
        print(f"  {r['actual']} -> {r['predicted']} | score={r['score']} | gap={r['gap']} | accepted={r['accepted']} | {r['method']} | {r['fold'].split(chr(92))[-1]}")