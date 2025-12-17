# ==============================================================================
# Script Name: reporter.py
# Description: Helper module for generating HTML reports and graphs.
#              Uses Matplotlib for SVG charting.
# Note:        This is a library file. Do not run directly.
# ==============================================================================

import os
import csv
import logging
import json
import sys
import matplotlib.pyplot as plt

try:
    from libs.html_templates import HTML_HEAD, HTML_ROW, HTML_FOOTER
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from libs.html_templates import HTML_HEAD, HTML_ROW, HTML_FOOTER

logger = logging.getLogger("Reporter")

METRIC_INFO = {
    "PSNR": {
        "name": "Peak Signal-to-Noise Ratio",
        "desc": "Approximation to human perception of reconstruction quality. Higher is better.",
        "link": "https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio"
    },
    "SSIM": {
        "name": "Structural Similarity",
        "desc": "Perceptual metric that quantifies image quality degradation caused by processing. Higher is better (Max 1.0).",
        "link": "https://en.wikipedia.org/wiki/Structural_similarity"
    },
    "RMSE": {
        "name": "Root Mean Squared Error",
        "desc": "Measure of the differences between values predicted by a model or an estimator and the values observed. Lower is better.",
        "link": "https://en.wikipedia.org/wiki/Root-mean-square_deviation"
    },
    "MAE": {
        "name": "Mean Absolute Error",
        "desc": "Average of absolute errors between the original and compressed image. Lower is better.",
        "link": "https://en.wikipedia.org/wiki/Mean_absolute_error"
    },
    "NCC": {
        "name": "Normalized Cross Correlation",
        "desc": "Measure of similarity of two waveforms as a function of a time-lag applied to one of them. Closer to 1.0 is better.",
        "link": "https://en.wikipedia.org/wiki/Cross-correlation"
    }
}

def generate_report(original_image, csv_path, report_dir, root_dir):
    graph_dir = os.path.join(report_dir, "graphs")
    os.makedirs(graph_dir, exist_ok=True)
    
    data = []
    headers = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            for key in row:
                if key not in ['filename', 'format', 'params', 'relative_path', 'diff_path', 'details']:
                    try:
                        row[key] = float(row[key])
                    except ValueError:
                        pass 
            row['quality'] = int(row['quality'])
            data.append(row)

    metric_cols = [h for h in headers if h not in [
        'filename', 'format', 'quality', 'params', 'relative_path', 'diff_path', 'details', 'size_kb'
    ]]
    
    generate_graphs(data, graph_dir, metric_cols)
    generate_html(original_image, data, report_dir, root_dir, metric_cols)

def generate_graphs(data, graph_dir, metric_cols):
    formats = list(set(d['format'] for d in data))
    
    metric_groups = {}
    for col in metric_cols:
        base = col.split('-')[0]
        if base not in metric_groups:
            metric_groups[base] = []
        metric_groups[base].append(col)

    create_chart(
        data, formats, "quality", "size_kb", 
        "Quality Setting vs File Size", "Quality", "Size (KB)", 
        os.path.join(graph_dir, "size_vs_quality.svg")
    )

    for group_name, cols in metric_groups.items():
        if group_name in cols:
            create_chart(
                data, formats, "size_kb", group_name,
                f"{group_name} Efficiency (vs Size)", "Size (KB)", group_name,
                os.path.join(graph_dir, f"{group_name}_efficiency.svg")
            )
        
        create_multi_metric_chart(
            data, formats, "quality", cols,
            f"{group_name} Detail (Channels)", "Quality", group_name,
            os.path.join(graph_dir, f"{group_name}_channels.svg")
        )

def create_chart(data, formats, x_key, y_key, title, xlabel, ylabel, path):
    plt.figure(figsize=(12, 6))
    for fmt in formats:
        subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x[x_key])
        x_vals = [d[x_key] for d in subset]
        y_vals = [d[y_key] for d in subset]
        plt.plot(x_vals, y_vals, marker='o', label=fmt)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, format='svg')
    plt.close()

def create_multi_metric_chart(data, formats, x_key, y_keys, title, xlabel, ylabel, path):
    plt.figure(figsize=(12, 6))
    
    styles = {'Red': 'r', 'Green': 'g', 'Blue': 'b', 'Alpha': 'c', 'All': 'k'}
    linestyles = {'webp': '-', 'jpeg': '--', 'png': ':'}
    
    for fmt in formats:
        subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x[x_key])
        x_vals = [d[x_key] for d in subset]
        
        for y_key in y_keys:
            channel = y_key.split('-')[1] if '-' in y_key else "All"
            color = styles.get(channel, 'k')
            ls = linestyles.get(fmt, '-')
            
            y_vals = [d.get(y_key, 0) for d in subset]
            label = f"{fmt} {channel}"
            
            plt.plot(x_vals, y_vals, marker='.', linestyle=ls, color=color, label=label, alpha=0.8)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(path, format='svg')
    plt.close()

def get_rel_path(target_path, start_path):
    try:
        return os.path.relpath(target_path, start_path)
    except ValueError:
        return target_path

def generate_html(original_path, data, report_dir, root_dir, metric_cols):
    data.sort(key=lambda x: (x['format'], -x['quality']))
    abs_report_dir = os.path.abspath(report_dir)
    abs_root_dir = os.path.abspath(root_dir)
    
    metric_names = sorted(list(set([m.split('-')[0] for m in metric_cols])))
    
    explanations_html = ""
    for m in metric_names:
        info = METRIC_INFO.get(m, {"name": m, "desc": "No description available.", "link": "#"})
        explanations_html += f"""
        <div class="metric-card">
            <h4>{info['name']} ({m})</h4>
            <p>{info['desc']}</p>
            <a href="{info['link']}" target="_blank">Learn More &rarr;</a>
        </div>
        """

    graphs_html = ""
    graphs_html += f'<div class="graph-box"><h3>Size vs Quality</h3><img src="graphs/size_vs_quality.svg" data-caption="Chart: File Size vs Quality Setting"></div>'
    
    for m in metric_names:
        graphs_html += f'<div class="graph-box"><h3>{m} Efficiency</h3><img src="graphs/{m}_efficiency.svg" data-caption="Chart: {m} Efficiency (vs Size)"></div>'
        graphs_html += f'<div class="graph-box"><h3>{m} Channels</h3><img src="graphs/{m}_channels.svg" data-caption="Chart: {m} Channel Breakdown"></div>'

    rows_html = ""
    for row in data:
        abs_img_path = os.path.join(abs_root_dir, row['relative_path'])
        img_rel = get_rel_path(abs_img_path, abs_report_dir)
        
        diff_rel = ""
        if row['diff_path']:
            abs_diff_path = os.path.join(abs_root_dir, row['diff_path'])
            diff_rel = get_rel_path(abs_diff_path, abs_report_dir)
        
        try:
            details_obj = json.loads(row.get('details', '{}'))
            details_str = f"{details_obj.get('width','?')}x{details_obj.get('height','?')} {details_obj.get('colorspace','')} {details_obj.get('depth','')}bit"
        except:
            details_str = "N/A"

        metrics_html = ""
        for m in metric_names:
            val = row.get(m, 0)
            metrics_html += f"<strong>{m}:</strong> {val:.2f} "

        rows_html += HTML_ROW.format(
            filename=row['filename'],
            format=row['format'],
            quality=row['quality'],
            size=row['size_kb'],
            details=details_str,
            metrics=metrics_html,
            img_src=img_rel,
            diff_src=diff_rel
        )

    summary_html = f"""
    <div class="summary-box">
        <h3>Report Summary</h3>
        <p><strong>Input Image:</strong> {os.path.basename(original_path)}</p>
        <p><strong>Total Variants:</strong> {len(data)}</p>
        <p><strong>Formats Tested:</strong> {', '.join(set(d['format'] for d in data))}</p>
        <p><strong>Metrics Captured:</strong> {', '.join(metric_names)}</p>
    </div>
    """

    full_html = HTML_HEAD.format(
        summary=summary_html, 
        metric_explanations=explanations_html, 
        graphs=graphs_html
    ) + rows_html + HTML_FOOTER
    
    with open(os.path.join(report_dir, "index.html"), "w") as f:
        f.write(full_html)

if __name__ == "__main__":
    print("\n[!] This is a library file and cannot be run directly.")
    print(f"    Please run the main script instead:\n")
    print(f"    python scripts/compression_analyzer.py <image_path>\n")
    sys.exit(1)