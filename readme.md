# Image Compression Analyzer

A Python toolset to generate, measure, and visualize image compression trade-offs between formats (WebP, JPEG) using `cwebp` and ImageMagick.

## Prerequisites

1. **Python 3.8+**

2. **ImageMagick**: Must be installed and accessible via command line (`magick`).

3. **WebP Tools**: `cwebp` must be accessible via command line.

4. **Python Libraries**: `matplotlib`.

## Installation

### Windows

1. Run `scripts/installs/install-windows.ps1` in PowerShell.

   * This automates Python, ImageMagick, and WebP installation via Winget/Direct Download.

### Linux (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install webp imagemagick python3-pip
pip3 install matplotlib

```

### macOS

```bash
brew install webp imagemagick
pip3 install matplotlib

```

### Docker

If you prefer not to install dependencies locally, you can use the included Dockerfile.

1. **Build the Image:**

   ```bash
   docker build -t img-analyzer -f scripts/installs/dockerfile .
   
   ```

2. **Run the Analyzer:**
   Map your local folder containing images to `/analysis` inside the container.

   ```bash
   # Linux/Mac
   docker run --rm -v $(pwd):/analysis img-analyzer your-image.jpg --formats webp jpeg
   
   # Windows (PowerShell)
   docker run --rm -v ${PWD}:/analysis img-analyzer your-image.jpg --formats webp jpeg
   
   ```

## Usage

1. Place your source image in the project folder (e.g., `photo.jpg`).

2. Run the analyzer:

```bash
python scripts/compression_analyzer.py photo.jpg --steps 10 --formats webp jpeg

```

3. The script will create a folder named `photo` (or `photo_<timestamp>`).

4. Open `photo/index.html` to view the results.

## Output Structure

* `/images`: Contains all generated compressed images.

* `/diffs`: Contains visual difference maps.

* `/data`: Contains raw CSV metrics (including per-channel analysis).

* `/graphs`: Contains SVG charts of the metrics.

* `index.html`: The interactive report.