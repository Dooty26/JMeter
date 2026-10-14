import csv
import numpy as np

def analyze(filename):
    print(f"=== {filename} ===")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        labels = {}
        for r in reader:
            lbl = r['label']
            if lbl not in labels:
                labels[lbl] = {'count': 0, 'errors': 0, 'elapsed': [], 'bytes': [], 'sent': []}
            labels[lbl]['count'] += 1
            if r['success'] != 'true':
                labels[lbl]['errors'] += 1
            labels[lbl]['elapsed'].append(int(r['elapsed']))
            labels[lbl]['bytes'].append(int(r.get('bytes', 0)))
            labels[lbl]['sent'].append(int(r.get('sentBytes', 0)))

        all_elapsed = []
        total_count = 0
        total_err = 0
        print(f"{'Label':<45} | {'# Samples':<9} | {'Average (ms)':<12} | {'Min (ms)':<8} | {'Max (ms)':<8} | {'Error %':<8}")
        print("-" * 105)
        for lbl, d in labels.items():
            el = d['elapsed']
            all_elapsed.extend(el)
            cnt = d['count']
            err = d['errors']
            total_count += cnt
            total_err += err
            avg = np.mean(el)
            err_pct = (err / cnt) * 100
            print(f"{lbl:<45} | {cnt:<9} | {avg:<12.2f} | {min(el):<8} | {max(el):<8} | {err_pct:<7.2f}%")
        
        total_avg = np.mean(all_elapsed)
        total_err_pct = (total_err / total_count) * 100
        print("-" * 105)
        print(f"{'TOTAL':<45} | {total_count:<9} | {total_avg:<12.2f} | {min(all_elapsed):<8} | {max(all_elapsed):<8} | {total_err_pct:<7.2f}%")
        print("\n")

if __name__ == '__main__':
    analyze('web_results.jtl')
    analyze('api_load_100.jtl')
    analyze('api_stress_1000.jtl')
    analyze('vnexpress_results.jtl')
