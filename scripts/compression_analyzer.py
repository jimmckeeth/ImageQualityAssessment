import argparse
import os
import logging
import datetime
import shutil
from libs.compressor import run_compressions
from libs.analyzer import analyze_results
from libs.reporter import generate_report

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
    parser = argparse.ArgumentParser(description="Image Compression Analyzer")
    parser.add_argument("image", help="Path to the input image file")
    parser.add_argument("--steps", type=int, default=10, help="Number of quality steps (default 10)")
    parser.add_argument("--formats", nargs="+", default=["webp", "jpeg"], help="Formats to test (webp, jpeg, png)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger("Main")

    if not os.path.exists(args.image):
        logger.error(f"Input file not found: {args.image}")
        return

    # Create directory structure
    filename = os.path.basename(args.image)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = f"{name}_{timestamp}"
    
    dirs = {
        "root": base_dir,
        "images": os.path.join(base_dir, "images"),
        "diffs": os.path.join(base_dir, "diffs"),
        "data": os.path.join(base_dir, "data"),
        "report": os.path.join(base_dir, ".")
    }

    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    # Copy original for reference
    original_copy = os.path.join(dirs["images"], f"original{ext}")
    shutil.copy(args.image, original_copy)

    logger.info(f"Starting analysis for {args.image}")
    logger.info(f"Output directory: {base_dir}")

    # 1. Compress
    compressed_files = run_compressions(original_copy, dirs["images"], args.formats, args.steps)
    
    # 2. Analyze
    metrics_csv = analyze_results(original_copy, compressed_files, dirs["diffs"], dirs["data"])
    
    # 3. Report
    generate_report(original_copy, metrics_csv, dirs["report"], dirs["root"])

    logger.info("Processing complete.")

if __name__ == "__main__":
    main()