import csv
from collections import defaultdict

rows = list(csv.DictReader(open('crossval_results.csv')))
print(f'Total rows: {len(rows)}')

methods = {}
for r in rows:
    methods.setdefault(r['method'], []).append(r)

for m, rs in methods.items():
    print(f'\\n--- {m.upper()} ---')
    print(f'  Total: {len(rs)}')
    correct_raw = sum(1 for r in rs if r['predicted'] == r['actual'])
    print(f'  Raw accuracy: {correct_raw/len(rs)*100:.1f}% ({correct_raw}/{len(rs)})')
    accepted = [r for r in rs if r['accepted'] == 'True']
    correct_acc = sum(1 for r in rs if r['accepted'] == 'True' and r['predicted'] == r['actual'])
    print(f'  Coverage: {len(accepted)/len(rs)*100:.1f}% ({len(accepted)}/{len(rs)})')
    print(f'  Correct among accepted: {correct_acc/len(accepted)*100:.1f}% ({correct_acc}/{len(accepted)})')
    false_acc = sum(1 for r in rs if r['accepted'] == 'True' and r['predicted'] != r['actual'])
    print(f'  False accepts: {false_acc}')
    print(f'  False-accept rate: {false_acc/len(rs)*100:.1f}%')
    rejected = sum(1 for r in rs if r['accepted'] != 'True')
    print(f'  Rejected: {rejected} ({rejected/len(rs)*100:.1f}%)')
    correct_rejected = sum(1 for r in rs if r['accepted'] != 'True' and r['predicted'] == r['actual'])
    print(f'  Correct but rejected: {correct_rejected}')
    gaps = [float(r['gap']) for r in rs if r['gap']]
    if gaps:
        print(f'  Mean gap: {sum(gaps)/len(gaps):.6f}')
        print(f'  Min gap: {min(gaps):.6f}')
        print(f'  Max gap: {max(gaps):.6f}')
    for cls in ['pechay_plant', 'monggo_plant']:
        cls_rows = [r for r in rs if r['actual'] == cls]
        cls_correct = sum(1 for r in cls_rows if r['predicted'] == cls)
        print(f'  {cls}: {cls_correct}/{len(cls_rows)} correct ({cls_correct/len(cls_rows)*100:.1f}%)')

print('\\n=== Threshold Simulation (score=0.80 fixed) ===')
print(f"{'Margin':>8} {'Cov':>8} {'Acc':>8} {'FA':>6} {'FAR':>8} {'AccR':>8} {'PechCov':>8} {'MongCov':>8} {'PechAcc':>8} {'MongAcc':>8}")
for margin in (0.001, 0.002, 0.003, 0.004, 0.005, 0.0075, 0.010, 0.015, 0.020, 0.030, 0.050, 0.070):
    accepted = [r for r in rows if r['accepted'] == 'True' and float(r['gap']) >= margin]
    n = len(rows)
    cov = len(accepted) / n * 100 if n else 0
    correct_acc = [r for r in accepted if r['actual'] == r['predicted']]
    wrong_acc = [r for r in accepted if r['actual'] != r['predicted']]
    acc_rate = len(correct_acc) / len(accepted) * 100 if accepted else 0
    far = len(wrong_acc) / n * 100 if n else 0
    pechay = [r for r in rows if r['actual'] == 'pechay_plant']
    monggo = [r for r in rows if r['actual'] == 'monggo_plant']
    pechay_all_acc = [r for r in pechay if r['accepted'] == 'True' and float(r['gap']) >= margin]
    monggo_all_acc = [r for r in monggo if r['accepted'] == 'True' and float(r['gap']) >= margin]
    pechay_acc_correct = [r for r in pechay_all_acc if r['predicted'] == 'pechay_plant']
    monggo_acc_correct = [r for r in monggo_all_acc if r['predicted'] == 'monggo_plant']
    pech_cov = len(pechay_all_acc) / len(pechay) * 100 if pechay else 0
    mong_cov = len(monggo_all_acc) / len(monggo) * 100 if monggo else 0
    pech_acc_r = len(pechay_acc_correct) / len(pechay_all_acc) * 100 if pechay_all_acc else 0
    mong_acc_r = len(monggo_acc_correct) / len(monggo_all_acc) * 100 if monggo_all_acc else 0
    print(f"{margin:>8.3f} {cov:>7.1f}% {acc_rate:>7.1f}% {len(wrong_acc):>6} {far:>7.1f}% {acc_rate:>7.1f}% {pech_cov:>7.1f}% {mong_cov:>7.1f}% {pech_acc_r:>7.1f}% {mong_acc_r:>7.1f}%")

print('\\n=== Method Agreement ===')
by_sample = defaultdict(dict)
for row in rows:
    key = (row['actual'], row['path'])
    by_sample[key][row['method']] = row
all_agree = 0
all_correct = 0
all_wrong = 0
ill_only_correct_when_full_wrong = 0
combined_worse_than_ill = 0
for key, methods in by_sample.items():
    actual = key[0]
    preds = {m: r['predicted'] for m, r in methods.items()}
    all_preds = list(preds.values())
    if len(set(all_preds)) == 1:
        all_agree += 1
        if all_preds[0] == actual:
            all_correct += 1
        else:
            all_wrong += 1
    if methods['full_card']['predicted'] != actual and methods['illustration_only']['predicted'] == actual:
        ill_only_correct_when_full_wrong += 1
    if methods['combined']['predicted'] != actual and methods['illustration_only']['predicted'] == actual:
        combined_worse_than_ill += 1
n_samples = len(by_sample)
print(f'  All methods agree: {all_agree}/{n_samples} ({all_agree/n_samples*100:.1f}%)')
print(f'    All correct: {all_correct}, All wrong: {all_wrong}')
print(f'  Ill-only correct when full-card wrong: {ill_only_correct_when_full_wrong}')
print(f'  Combined worse than ill-only: {combined_worse_than_ill}')

print('\\n=== Consistently Misclassified (all 3 methods wrong) ===')
all_wrong = []
for key, methods in by_sample.items():
    if all(r['predicted'] != key[0] for r in methods.values()):
        all_wrong.append(key)
print(f'  Samples misclassified by ALL methods: {len(all_wrong)}')
for actual, path in all_wrong[:15]:
    fname = path.split('\\\\')[-1] if '\\\\' in path else path.split('/')[-1]
    print(f'    {actual}: {fname}')

all_correct_all = []
for key, methods in by_sample.items():
    if all(r['predicted'] == key[0] for r in methods.values()):
        all_correct_all.append(key)
print(f'\\n  Samples correctly classified by ALL methods: {len(all_correct_all)}')

print('\\n=== ALL MISCLASSIFICATIONS ===')
for r in sorted(rows, key=lambda x: (x['actual'], x['method'])):
    if r['predicted'] != r['actual']:
        fname = r['fold'].split('\\\\')[-1] if '\\\\' in r['fold'] else r['fold'].split('/')[-1]
        print(f"  {r['actual']} -> {r['predicted']} | score={r['score']} | gap={r['gap']} | accepted={r['accepted']} | {r['method']} | {fname}")
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

# ============================================================
# THRESHOLD SIMULATION
# ============================================================
print('\\n=== Threshold Simulation (score=0.80 fixed) ===')
print(f"{'Margin':>8} {'Cov':>8} {'Acc':>8} {'FA':>6} {'FAR':>8} {'AccR':>8} {'PechCov':>8} {'MongCov':>8} {'PechAcc':>8} {'MongAcc':>8}")
for margin in (0.001, 0.002, 0.003, 0.004, 0.005, 0.0075, 0.010, 0.015, 0.020, 0.030, 0.050, 0.070):
    accepted = [r for r in rows if r['accepted'] == 'True' and float(r['gap']) >= margin]
    n = len(rows)
    cov = len(accepted) / n * 100 if n else 0
    correct_acc = [r for r in accepted if r['actual'] == r['predicted']]
    wrong_acc = [r for r in accepted if r['actual'] != r['predicted']]
    acc_rate = len(correct_acc) / len(accepted) * 100 if accepted else 0
    far = len(wrong_acc) / n * 100 if n else 0
    pechay = [r for r in rows if r['actual'] == 'pechay_plant']
    monggo = [r for r in rows if r['actual'] == 'monggo_plant']
    pechay_all_acc = [r for r in pechay if r['accepted'] == 'True' and float(r['gap']) >= margin]
    monggo_all_acc = [r for r in monggo if r['accepted'] == 'True' and float(r['gap']) >= margin]
    pechay_acc_correct = [r for r in pechay_all_acc if r['predicted'] == 'pechay_plant']
    monggo_acc_correct = [r for r in monggo_all_acc if r['predicted'] == 'monggo_plant']
    pech_cov = len(pechay_all_acc) / len(pechay) * 100 if pechay else 0
    mong_cov = len(monggo_all_acc) / len(monggo) * 100 if monggo else 0
    pech_acc_r = len(pechay_acc_correct) / len(pechay_all_acc) * 100 if pechay_all_acc else 0
    mong_acc_r = len(monggo_acc_correct) / len(monggo_all_acc) * 100 if monggo_all_acc else 0
    print(f"{margin:>8.3f} {cov:>7.1f}% {acc_rate:>7.1f}% {len(wrong_acc):>6} {far:>7.1f}% {acc_rate:>7.1f}% {pech_cov:>7.1f}% {mong_cov:>7.1f}% {pech_acc_r:>7.1f}% {mong_acc_r:>7.1f}%")

# ============================================================
# METHOD COMPARISON
# ============================================================
print('\\n=== Method Agreement ===')
from collections import defaultdict
by_sample = defaultdict(dict)
for row in rows:
    key = (row['actual'], row['path'])
    by_sample[key][row['method']] = row
all_agree = 0
all_correct = 0
all_wrong = 0
ill_only_correct_when_full_wrong = 0
combined_worse_than_ill = 0
for key, methods in by_sample.items():
    actual = key[0]
    preds = {m: r['predicted'] for m, r in methods.items()}
    all_preds = list(preds.values())
    if len(set(all_preds)) == 1:
        all_agree += 1
        if all_preds[0] == actual:
            all_correct += 1
        else:
            all_wrong += 1
    if methods['full_card']['predicted'] != actual and methods['illustration_only']['predicted'] == actual:
        ill_only_correct_when_full_wrong += 1
    if methods['combined']['predicted'] != actual and methods['illustration_only']['predicted'] == actual:
        combined_worse_than_ill += 1
n_samples = len(by_sample)
print(f'  All methods agree: {all_agree}/{n_samples} ({all_agree/n_samples*100:.1f}%)')
print(f'    All correct: {all_correct}, All wrong: {all_wrong}')
print(f'  Ill-only correct when full-card wrong: {ill_only_correct_when_full_wrong}')
print(f'  Combined worse than ill-only: {combined_worse_than_ill}')

# ============================================================
# MISCLASSIFIED BY ALL METHODS
# ============================================================
print('\\n=== Consistently Misclassified (all 3 methods wrong) ===')
all_wrong = []
for key, methods in by_sample.items():
    if all(r['predicted'] != key[0] for r in methods.values()):
        all_wrong.append(key)
print(f'  Samples misclassified by ALL methods: {len(all_wrong)}')
for actual, path in all_wrong[:15]:
    fname = path.split('\\\\')[-1] if '\\\\' in path else path.split('/')[-1]
    print(f'    {actual}: {fname}')

all_correct = []
for key, methods in by_sample.items():
    if all(r['predicted'] == key[0] for r in methods.values()):
        all_correct.append(key)
print(f'\\n  Samples correctly classified by ALL methods: {len(all_correct)}')
    if r['predicted'] != r['actual']:
        print(f"  {r['actual']} -> {r['predicted']} | score={r['score']} | gap={r['gap']} | accepted={r['accepted']} | {r['method']} | {r['fold'].split(chr(92))[-1]}")