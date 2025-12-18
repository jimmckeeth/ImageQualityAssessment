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
        base_upper = base.upper() 
        if base_upper not in metric_groups:
            metric_groups[base_upper] = []
        metric_groups[base_upper].append(col)

    # Helper to generate both light and dark versions
    def make_charts(x_key, y_key, title, xlabel, ylabel, filename_base, group_cols=None):
        # Light Mode (Default)
        create_chart_variant(
            data, formats, x_key, y_key, title, xlabel, ylabel, 
            os.path.join(graph_dir, f"{filename_base}.svg"),
            dark_mode=False, group_cols=group_cols
        )
        # Dark Mode
        create_chart_variant(
            data, formats, x_key, y_key, title, xlabel, ylabel, 
            os.path.join(graph_dir, f"{filename_base}_dark.svg"),
            dark_mode=True, group_cols=group_cols
        )

    # 1. Size vs Quality
    make_charts("quality", "size_kb", "Quality Setting vs File Size", "Quality", "Size (KB)", "size_vs_quality")

    # 2. Metric Groups
    for group_name, cols in metric_groups.items():
        # Efficiency
        main_col = next((c for c in cols if c.upper() == group_name), None)
        if main_col:
            make_charts("size_kb", main_col, f"{group_name} Efficiency (vs Size)", "Size (KB)", group_name, f"{group_name}_efficiency")
        
        # Channels
        make_charts("quality", None, f"{group_name} Detail (Channels)", "Quality", group_name, f"{group_name}_channels", group_cols=cols)

def create_chart_variant(data, formats, x_key, y_key, title, xlabel, ylabel, path, dark_mode=False, group_cols=None):
    # Style Config
    bg_color = '#2d3748' if dark_mode else '#ffffff'
    text_color = '#e2e8f0' if dark_mode else '#1a202c'
    grid_color = '#4a5568' if dark_mode else '#e2e8f0'
    
    plt.figure(figsize=(12, 6))
    
    # Set global style context
    with plt.rc_context({
        'axes.facecolor': bg_color,
        'figure.facecolor': bg_color,
        'text.color': text_color,
        'axes.labelcolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        'axes.edgecolor': grid_color
    }):
        if group_cols:
            # Multi-channel chart
            create_multi_metric_plot(data, formats, x_key, group_cols)
        else:
            # Single metric plot
            for fmt in formats:
                subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x[x_key])
                x_vals = [d[x_key] for d in subset]
                y_vals = [d.get(y_key, 0) for d in subset]
                plt.plot(x_vals, y_vals, marker='o', label=fmt)

        plt.title(title, color=text_color)
        plt.xlabel(xlabel, color=text_color)
        plt.ylabel(ylabel, color=text_color)
        plt.grid(True, which="both", linestyle='--', alpha=0.5, color=grid_color)
        
        # Legend styling
        legend = plt.legend()
        frame = legend.get_frame()
        frame.set_facecolor(bg_color)
        frame.set_edgecolor(grid_color)
        for text in legend.get_texts():
            text.set_color(text_color)

        plt.tight_layout()
        plt.savefig(path, format='svg', transparent=False)
        plt.close()

def create_multi_metric_plot(data, formats, x_key, y_keys):
    styles = {'Red': 'r', 'Green': 'g', 'Blue': 'b', 'Alpha': 'c', 'All': 'gray'}
    linestyles = {'webp': '-', 'jpeg': '--', 'png': ':'}
    
    for fmt in formats:
        subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x[x_key])
        x_vals = [d[x_key] for d in subset]
        
        for y_key in y_keys:
            parts = y_key.split('-')
            channel = parts[1] if len(parts) > 1 else "All"
            
            # Map "gray" to white in dark mode for visibility if needed, but let's stick to 'gray' or 'cyan'
            color = styles.get(channel, 'gray')
            ls = linestyles.get(fmt, '-')
            
            y_vals = [d.get(y_key, 0) for d in subset]
            label = f"{fmt} {channel}"
            
            plt.plot(x_vals, y_vals, marker='.', linestyle=ls, color=color, label=label, alpha=0.8)


def get_rel_path(target_path, start_path):
    try:
        return os.path.relpath(target_path, start_path)
    except ValueError:
        return target_path

def generate_html(original_path, data, report_dir, root_dir, metric_cols):
    data.sort(key=lambda x: (x['format'], -x['quality']))
    abs_report_dir = os.path.abspath(report_dir)
    abs_root_dir = os.path.abspath(root_dir)
    
    metric_names = sorted(list(set([m.split('-')[0].upper() for m in metric_cols])))
    
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
    # Add Size vs Quality (Light and Dark)
    graphs_html += f"""
    <div class="graph-box">
        <h3>Size vs Quality</h3>
        <img src="graphs/size_vs_quality.svg" data-dark-src="graphs/size_vs_quality_dark.svg" data-caption="Chart: File Size vs Quality Setting">
    </div>"""
    
    for m in metric_names:
        graphs_html += f"""
        <div class="graph-box">
            <h3>{m} Efficiency</h3>
            <img src="graphs/{m}_efficiency.svg" data-dark-src="graphs/{m}_efficiency_dark.svg" data-caption="Chart: {m} Efficiency (vs Size)">
        </div>"""
        graphs_html += f"""
        <div class="graph-box">
            <h3>{m} Channels</h3>
            <img src="graphs/{m}_channels.svg" data-dark-src="graphs/{m}_channels_dark.svg" data-caption="Chart: {m} Channel Breakdown">
        </div>"""

    rows_html = ""
    for idx, row in enumerate(data):
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
        for k, v in row.items():
            k_upper = k.split('-')[0].upper()
            if k_upper in metric_names and isinstance(v, (int, float)):
                if '-' not in k:
                    metrics_html += f"<strong>{k.upper()}:</strong> {v:.2f} "

        try:
            rows_html += HTML_ROW.format(
                index=idx, # Passed for JS row tracking
                filename=row['filename'],
                format=row['format'],
                quality=row['quality'],
                size=row['size_kb'],
                details=details_str,
                metrics=metrics_html,
                img_src=img_rel,
                diff_src=diff_rel
            )
        except KeyError as e:
            logger.error(f"HTML Template mismatch: Missing key {e}")
            rows_html += f"<div style='color:red'>Template Error: Missing {e}</div>"

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