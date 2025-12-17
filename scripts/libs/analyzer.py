# ==============================================================================
# Script Name: analyzer.py
# Description: Helper module for measuring image quality.
#              Wraps ImageMagick 'compare' and 'identify' tools.
# Note:        This is a library file. Do not run directly.
# ==============================================================================

import subprocess
import os
import logging
import csv
import re
import json
import sys

logger = logging.getLogger("Analyzer")

def get_image_details(path):
    """
    Uses ImageMagick identify to get image attributes.
    """
    try:
        # Get basic info: Width, Height, BitDepth, Colorspace, Format
        cmd = [
            "magick", "identify", 
            "-format", 
            '{"width": %w, "height": %h, "depth": %z, "colorspace": "%[colorspace]", "format": "%m"}',
            path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception as e:
        logger.error(f"Failed to identify {path}: {e}")
        return "{}"

def parse_magick_output(output, metric_name):
    """
    Parses verbose output from magick compare to get per-channel metrics.
    Returns a dict like {'PSNR': 40.2, 'PSNR_Red': 40.1, ...}
    """
    data = {}
    lines = output.splitlines()
    for line in lines:
        line = line.strip()
        if ':' not in line or "Channel distortion" in line or "Image:" in line:
            continue
            
        parts = line.split(':')
        channel = parts[0].strip().title() # Red, Green, Blue, All, Alpha
        value_str = parts[1].strip().split(' ')[0] # Get number before any ()
        
        try:
            if 'inf' in value_str.lower():
                val = 999.0
            elif 'nan' in value_str.lower():
                val = 0.0
            else:
                val = float(value_str)
            
            # Key generation: "PSNR" (for All) or "PSNR-Red"
            if channel.lower() == 'all':
                key = metric_name
            else:
                key = f"{metric_name}-{channel}"
            
            data[key] = val
        except ValueError:
            continue
            
    return data

def analyze_results(original_path, generated_files, diff_dir, data_dir):
    """
    Compares generated images against original using ImageMagick.
    Generates difference images and a CSV of metrics.
    """
    metrics_map = {
        "MAE": "MAE",       
        "RMSE": "RMSE",     
        "PSNR": "PSNR",     
        "SSIM": "SSIM",     
        "NCC": "NCC"        
    }

    csv_path = os.path.join(data_dir, "metrics.csv")
    
    all_rows = []
    all_keys = set([
        "filename", "format", "quality", "params", 
        "size_kb", "relative_path", "diff_path", "details"
    ])

    for item in generated_files:
        comp_path = item['path']
        filename = os.path.basename(comp_path)
        
        logger.info(f"Analyzing {filename}...")
        
        row = {
            "filename": filename,
            "format": item['format'],
            "quality": item['quality'],
            "params": item['params'],
            "size_kb": round(os.path.getsize(comp_path) / 1024, 2),
            "relative_path": os.path.relpath(comp_path, os.path.dirname(data_dir)),
            "details": get_image_details(comp_path)
        }

        # 1. Generate Difference Image (Visual)
        diff_name = f"diff_{filename}"
        diff_path = os.path.join(diff_dir, diff_name)
        
        diff_cmd = [
            "magick", "compare", 
            "-metric", "AE", 
            "-fuzz", "5%",      
            original_path, comp_path, 
            "-compose", "src",  
            diff_path
        ]
        
        try:
            subprocess.run(diff_cmd, capture_output=True)
            row["diff_path"] = os.path.relpath(diff_path, os.path.dirname(data_dir))
        except Exception as e:
            logger.error(f"Error creating diff image for {filename}: {e}")
            row["diff_path"] = ""

        # 2. Collect Numeric Metrics (Verbose)
        for metric_name, metric_arg in metrics_map.items():
            cmd = ["magick", "compare", "-verbose", "-metric", metric_arg, original_path, comp_path, "null:"]
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
                metric_data = parse_magick_output(res.stderr, metric_name)
                
                if not metric_data:
                    val_str = res.stderr.strip().split(' ')[0]
                    if "inf" in val_str.lower(): val = 999.0
                    else: val = float(val_str) if val_str else 0.0
                    metric_data = {metric_name: val}
                
                row.update(metric_data)
                all_keys.update(metric_data.keys())
                
            except Exception as e:
                logger.warning(f"Failed to calc {metric_name} for {filename}: {e}")

        all_rows.append(row)

    # Write CSV
    standard_fields = ["filename", "format", "quality", "params", "size_kb", "relative_path", "diff_path", "details"]
    metric_fields = sorted([k for k in all_keys if k not in standard_fields])
    fieldnames = standard_fields + metric_fields

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
            
    return csv_path

# ==============================================================================
# Execution Guard
# ==============================================================================
if __name__ == "__main__":
    print("\n[!] This is a library file and cannot be run directly.")
    print(f"    Please run the main script instead:\n")
    print(f"    python scripts/compression_analyzer.py <image_path>\n")
    sys.exit(1)