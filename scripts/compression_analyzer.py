import argparse
import os
import logging
import datetime
import shutil
import json
from libs.compressor import run_compressions
from libs.analyzer import analyze_results
from libs.reporter import generate_report

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from json file or return defaults."""
    default_config = {
        "steps": 10,
        "formats": ["webp", "jpeg"],
        "report_root": ".",
        "verbosity": 0
    }
    
    # Check if config file exists relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_FILE)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
                default_config.update(file_config)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {CONFIG_FILE}. Using defaults.")
    
    return default_config

def setup_logging(verbosity):
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

def main():
    config = load_config()
    
    parser = argparse.ArgumentParser(description="Image Compression Analyzer")
    parser.add_argument("image", help="Path to the input image file")
    
    # Use config values as defaults
    parser.add_argument("--steps", type=int, default=config["steps"], 
                       help=f"Number of quality steps (default {config['steps']})")
    parser.add_argument("--formats", nargs="+", default=config["formats"], 
                       help=f"Formats to test (default {config['formats']})")
    parser.add_argument("--report-root", default=config["report_root"],
                       help=f"Root directory for reports (default '{config['report_root']}')")
    parser.add_argument("-v", "--verbose", action="count", default=config["verbosity"], 
                       help="Increase verbosity")
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger("Main")

    if not os.path.exists(args.image):
        logger.error(f"Input file not found: {args.image}")
        return

    # Determine Output Directory Name
    filename = os.path.basename(args.image)
    image_name_no_ext, ext = os.path.splitext(filename)
    
    # Base output path
    report_root = os.path.abspath(args.report_root)
    base_output_dir = os.path.join(report_root, image_name_no_ext)
    
    # If folder exists, append timestamp
    if os.path.exists(base_output_dir):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_output_dir = f"{base_output_dir}_{timestamp}"
    
    dirs = {
        "root": base_output_dir,
        "images": os.path.join(base_output_dir, "images"),
        "diffs": os.path.join(base_output_dir, "diffs"),
        "data": os.path.join(base_output_dir, "data"),
        "report": os.path.join(base_output_dir, ".") # Report at root of project folder
    }

    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    # Copy original using its ACTUAL filename, not "original.ext"
    # This ensures compressor generates "filename_qXX.webp" instead of "original_qXX.webp"
    original_copy = os.path.join(dirs["images"], filename)
    shutil.copy(args.image, original_copy)

    logger.info(f"Starting analysis for {args.image}")
    logger.info(f"Output directory: {base_output_dir}")

    # 1. Compress
    compressed_files = run_compressions(original_copy, dirs["images"], args.formats, args.steps)
    
    # 2. Analyze
    metrics_csv = analyze_results(original_copy, compressed_files, dirs["diffs"], dirs["data"])
    
    # 3. Report
    generate_report(original_copy, metrics_csv, dirs["report"], dirs["root"])

    logger.info("Processing complete.")

if __name__ == "__main__":
    main()