# **Image Compression Analyzer**

***Note:*** *This is still a work in progress. Things are changing rapidly, so what works today may break tomorrow. Use at your own risk.*

A tools to generate, measure, and visualize image compression trade-offs between formats (WebP, JPEG) using cwebp and ImageMagick.

## Prerequisites

1. **Python 3.8+**  
2. **ImageMagick**: Must be installed and accessible via command line (magick).  
3. **WebP Tools**: cwebp must be accessible via command line.  
4. **Python Libraries**: matplotlib (for graphing).

## Installation

### Linux (Debian/Ubuntu)

```bash
sudo apt-get update  
sudo apt-get install webp imagemagick python3-pip  
pip3 install matplotlib
```

### macOS

```shell
brew install webp imagemagick  
pip3 install matplotlib
```

### Windows

```pwsh
winget install python
1. Install Python from python.org.  
2. Install **ImageMagick** (check "Install legacy utilities (e.g. convert)" or ensure magick is in PATH).  
3. Download **libwebp** binaries for Windows and add the bin folder to your system PATH.  
4. Run `pip install matplotlib`.

## Usage

1. Place your source image in the project folder (e.g., photo.jpg).  
2. Run the analyzer:

```pwsh
python compression\_analyzer.py photo.jpg \--steps 10 \--formats webp jpeg
```

3. The script will create a folder named photo\_\<timestamp\>.  
4. Open photo\_\<timestamp\>/report/index.html to view the results.

## Output Structure

* /images: Contains all generated compressed images.  
* /diffs: Contains visual difference maps created by ImageMagick.  
* /data: Contains raw CSV metrics.  
* /report: Contains the HTML report and graphs.

## Troubleshooting

* **"magick not found"**: Ensure ImageMagick is in your system PATH. On Linux, legacy versions might use convert instead of magick. This script assumes the modern magick command.  
* **"cwebp not found"**: Ensure the folder containing cwebp.exe (Windows) or binary (Linux/Mac) is in your PATH.