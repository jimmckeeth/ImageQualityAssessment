import subprocess
import os
import logging
import csv
import json

logger = logging.getLogger("Analyzer")

def get_file_size_kb(path):
    return os.path.getsize(path) / 1024

def analyze_results(original_path, generated_files, diff_dir, data_dir):
    """
    Compares generated images against original using ImageMagick.
    Generates difference images and a CSV of metrics.
    """
    results = []
    
    # Define metrics to capture
    # Key is name in CSV, Value is ImageMagick metric argument
    metrics_map = {
        "MAE": "MAE",       # Mean Absolute Error
        "RMSE": "RMSE",     # Root Mean Squared Error
        "PSNR": "PSNR",     # Peak Signal-to-Noise Ratio
        "SSIM": "SSIM",     # Structural Similarity
        "NCC": "NCC"        # Normalized Cross Correlation
    }

    csv_path = os.path.join(data_dir, "metrics.csv")
    
    # Prepare CSV headers
    fieldnames = ["filename", "format", "quality", "params", "size_kb", "relative_path", "diff_path"] + list(metrics_map.keys())

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in generated_files:
            comp_path = item['path']
            filename = os.path.basename(comp_path)
            
            logger.info(f"Analyzing {filename}...")
            
            row = {
                "filename": filename,
                "format": item['format'],
                "quality": item['quality'],
                "params": item['params'],
                "size_kb": round(get_file_size_kb(comp_path), 2),
                "relative_path": os.path.relpath(comp_path, os.path.dirname(data_dir)), # Relative to root dir for HTML
            }

            # 1. Generate Difference Image (Visual)
            # using 'magick compare' with -compose src
            diff_name = f"diff_{filename}"
            diff_path = os.path.join(diff_dir, diff_name)
            
            # Use 'ae' (Absolute Error) for visual diff usually, or just default compare
            diff_cmd = [
                "magick", "compare", 
                "-metric", "AE", 
                "-fuzz", "5%",      # Ignore minor noise for visual diff
                original_path, comp_path, 
                "-compose", "src",  # Highlight differences
                diff_path
            ]
            
            try:
                # Compare writes metric to stderr, image to last arg
                subprocess.run(diff_cmd, capture_output=True)
                row["diff_path"] = os.path.relpath(diff_path, os.path.dirname(data_dir))
            except Exception as e:
                logger.error(f"Error creating diff image for {filename}: {e}")
                row["diff_path"] = ""

            # 2. Collect Numeric Metrics
            # Note: For efficiency we could do this in fewer calls, but distinct calls ensure parsing reliability
            for metric_name, metric_arg in metrics_map.items():
                cmd = ["magick", "compare", "-metric", metric_arg, original_path, comp_path, "null:"]
                
                try:
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    # ImageMagick outputs metric to stderr
                    val_str = res.stderr.strip()
                    
                    # Handle "inf" for PSNR on identical images
                    if "inf" in val_str.lower():
                        val = 999.0 # Cap infinity for graphing
                    else:
                        # Sometimes output is like "0.98 (0.01)" -> take first part
                        val = float(val_str.split(' ')[0])
                    
                    row[metric_name] = val
                except Exception as e:
                    logger.warning(f"Failed to calc {metric_name} for {filename}: {e}")
                    row[metric_name] = 0

            results.append(row)
            writer.writerow(row)
            
    return csv_path