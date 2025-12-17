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
    os.makedirs(os.path.join(report_dir, "graphs"), exist_ok=True)
    
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
    generate_graphs(data, os.path.join(report_dir, "graphs"))
    
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

def generate_html(original_path, data, report_dir, root_dir):
    # Calculate relative paths for HTML
    # We are in /root/report/, images are in /root/images
    
    # Sort data by quality descending
    data.sort(key=lambda x: (x['format'], -x['quality']))

    # Relative path to original image from report dir
    # original_path is absolute or relative to run script. 
    # Let's rely on the structure: root/images/img.ext
    # report is root/report/
    rel_orig = os.path.join("../images", os.path.basename(original_path))

    rows_html = ""
    for row in data:
        # adjust paths from CSV (which are relative to root) to be relative to report folder
        img_rel = os.path.join("..", row['relative_path'])
        diff_rel = os.path.join("..", row['diff_path'])
        
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