import os
import csv
import logging
import matplotlib.pyplot as plt
from libs.html_templates import HTML_HEAD, HTML_ROW, HTML_FOOTER

logger = logging.getLogger("Reporter")

def generate_report(original_image, csv_path, report_dir, root_dir):
    """
    Creates graphs and an HTML report.
    """
    # Ensure graph directory exists inside the report folder
    graph_dir = os.path.join(report_dir, "graphs")
    os.makedirs(graph_dir, exist_ok=True)
    
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric types
            row['quality'] = int(row['quality'])
            row['size_kb'] = float(row['size_kb'])
            row['PSNR'] = float(row['PSNR'])
            row['SSIM'] = float(row['SSIM'])
            data.append(row)

    # 1. Generate Graphs
    # We pass the graph_dir which is now correctly located
    generate_graphs(data, graph_dir)
    
    # 2. Generate HTML
    generate_html(original_image, data, report_dir, root_dir)

def generate_graphs(data, graph_dir):
    # Group by format
    formats = list(set(d['format'] for d in data))
    
    # Plot 1: Size vs Quality Setting
    plt.figure(figsize=(10, 6))
    for fmt in formats:
        subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x['quality'])
        qualities = [d['quality'] for d in subset]
        sizes = [d['size_kb'] for d in subset]
        plt.plot(qualities, sizes, marker='o', label=fmt)
    
    plt.title("File Size vs Quality Setting")
    plt.xlabel("Quality Setting (0-100)")
    plt.ylabel("Size (KB)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(graph_dir, "size_vs_quality.png"))
    plt.close()

    # Plot 2: SSIM vs Size (Efficiency)
    plt.figure(figsize=(10, 6))
    for fmt in formats:
        subset = sorted([d for d in data if d['format'] == fmt], key=lambda x: x['size_kb'])
        sizes = [d['size_kb'] for d in subset]
        ssim = [d['SSIM'] for d in subset]
        plt.plot(sizes, ssim, marker='o', label=fmt)

    plt.title("Visual Quality (SSIM) vs File Size")
    plt.xlabel("Size (KB)")
    plt.ylabel("SSIM (Higher is better)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(graph_dir, "ssim_vs_size.png"))
    plt.close()

def get_rel_path(target_path, start_path):
    """Safe wrapper for relpath that handles directory traversal"""
    try:
        rel = os.path.relpath(target_path, start_path)
        return rel
    except ValueError:
        return target_path

def generate_html(original_path, data, report_dir, root_dir):
    """
    Generates the HTML report.
    report_dir: Where index.html will be saved.
    root_dir: The base directory of the run (where images/ and diffs/ are).
    """
    
    # Sort data by quality descending
    data.sort(key=lambda x: (x['format'], -x['quality']))

    # Absolute paths for calculations
    abs_report_dir = os.path.abspath(report_dir)
    abs_root_dir = os.path.abspath(root_dir)
    
    rows_html = ""
    for row in data:
        # The CSV stores 'relative_path' from the project root (e.g. "images/file.webp")
        # We need to construct the full path, then find the relative path from the HTML file
        
        # 1. Image Path
        abs_img_path = os.path.join(abs_root_dir, row['relative_path'])
        img_rel = get_rel_path(abs_img_path, abs_report_dir)
        
        # 2. Diff Path
        # Handle cases where diff generation might have failed
        if row['diff_path']:
            abs_diff_path = os.path.join(abs_root_dir, row['diff_path'])
            diff_rel = get_rel_path(abs_diff_path, abs_report_dir)
        else:
            diff_rel = ""
        
        rows_html += HTML_ROW.format(
            filename=row['filename'],
            format=row['format'],
            quality=row['quality'],
            size=row['size_kb'],
            psnr=row['PSNR'],
            ssim=row['SSIM'],
            img_src=img_rel,
            diff_src=diff_rel
        )

    full_html = HTML_HEAD + rows_html + HTML_FOOTER
    
    with open(os.path.join(report_dir, "index.html"), "w") as f:
        f.write(full_html)