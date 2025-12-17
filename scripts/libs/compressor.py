import subprocess
import os
import logging

logger = logging.getLogger("Compressor")

def run_compressions(input_path, output_dir, formats, steps):
    """
    Generates compressed versions of the image.
    Returns a list of dictionaries containing file paths and metadata.
    """
    generated_files = []
    
    step_size = 100 // steps
    qualities = list(range(step_size, 101, step_size))
    # Ensure 0 is included if desired, or start at low quality
    if 0 not in qualities:
        qualities.insert(0, 5) # 0 is often too destructive, 5 is a good low bound

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    for fmt in formats:
        fmt = fmt.lower()
        
        if fmt == "webp":
            # WebP Loop
            for q in qualities:
                output_name = f"{base_name}_q{q}.webp"
                output_path = os.path.join(output_dir, output_name)
                
                cmd = ["cwebp", "-q", str(q), input_path, "-o", output_path]
                
                logger.info(f"Compressing WebP: Quality {q}")
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    generated_files.append({
                        "path": output_path,
                        "format": "webp",
                        "quality": q,
                        "params": f"-q {q}"
                    })
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to compress {output_name}: {e}")

            # WebP Lossless
            output_name = f"{base_name}_lossless.webp"
            output_path = os.path.join(output_dir, output_name)
            cmd = ["cwebp", "-lossless", input_path, "-o", output_path]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                generated_files.append({
                    "path": output_path,
                    "format": "webp",
                    "quality": 100,
                    "params": "-lossless"
                })
            except Exception as e:
                logger.error(f"WebP lossless failed: {e}")

        elif fmt in ["jpg", "jpeg"]:
            # JPEG Loop (using ImageMagick)
            for q in qualities:
                output_name = f"{base_name}_q{q}.jpg"
                output_path = os.path.join(output_dir, output_name)
                
                # Magick command
                cmd = ["magick", input_path, "-quality", str(q), output_path]
                
                logger.info(f"Compressing JPEG: Quality {q}")
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    generated_files.append({
                        "path": output_path,
                        "format": "jpeg",
                        "quality": q,
                        "params": f"-quality {q}"
                    })
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to compress {output_name}: {e}")

    return generated_files