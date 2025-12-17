# **The Efficacy of Modern Image Compression: A Comprehensive Analysis of Algorithms, Formats, and Automated Quality Assessment**

## **1\. Introduction**

The efficient representation of visual information stands as one of the pillars of the modern digital ecosystem. As the volume of image data traversing global networks continues to grow exponentially—accounting for a significant plurality of total internet traffic—the engineering decisions governing image formats and compression parameters have transcended mere aesthetic preference to become critical determinants of user experience, bandwidth economics, and computational performance. The "trilemma" of digital imaging—balancing visual fidelity, file size, and encoding/decoding speed—requires a nuanced understanding that goes beyond the superficial knowledge that "JPEG is for photos" and "PNG is for graphics."

This report provides an exhaustive examination of the trade-offs inherent in the bitmap image landscape of 2025\. It dissects the theoretical underpinnings of entropy coding and psychovisual modeling that drive formats like JPEG, PNG, WebP, AVIF, and JPEG XL. It critically evaluates the methodologies used to assess image quality, contrasting traditional pixel-difference metrics with modern human visual system (HVS) proxies. Furthermore, it presents a bespoke automated framework—implemented in Python—designed to empirically measure these relationships, offering a practical tool for data-driven optimization.

## **2\. Theoretical Framework: The Physics and Mathematics of Image Compression**

To navigate the complex trade-offs between different image formats, one must first establish a robust understanding of the mechanisms by which digital images are reduced in size. Compression is fundamentally an exercise in information theory, specifically the identification and elimination of two distinct types of redundancy: statistical redundancy and perceptual redundancy.

### **2.1 Information Theory and Lossless Compression**

Lossless compression algorithms operate on the premise that the data contains statistical redundancy that can be eliminated without altering the underlying information. The theoretical limit of this compression is defined by the Shannon Entropy of the image, which quantifies the average amount of information produced by the source. If an image consists of a uniform blue field, its entropy is low, as the probability of the next pixel being blue is near certainty. Conversely, a photograph of high-frequency noise or static has high entropy, as the prediction of neighboring pixels is statistically difficult.

Formats such as PNG (Portable Network Graphics) rely on algorithms like Deflate, which combines LZ77 (Lempel-Ziv 1977\) and Huffman coding. LZ77 functions by replacing repeated occurrences of data with references to a single copy of that data existing earlier in the uncompressed data stream. For example, a repeating pattern of pixels in a graphic design element creates a "dictionary" entry, allowing subsequent occurrences to be represented by a short pointer rather than the full pixel data. However, the efficacy of lossless compression on continuous-tone photographs is strictly limited by the high entropy introduced by sensor noise and the chaotic nature of real-world light physics. In such cases, compression ratios rarely exceed 2:1 or 3:1, necessitating the use of lossy techniques for web delivery.

### **2.2 The Psychophysics of Lossy Compression**

Lossy compression achieves significantly higher ratios—often exceeding 20:1—by discarding information that the human eye is biologically less likely to perceive. This process exploits specific limitations of the Human Visual System (HVS), primarily the Contrast Sensitivity Function (CSF). The human eye is far more sensitive to variations in luminance (brightness) than to variations in chrominance (color). Furthermore, the eye demonstrates a reduced sensitivity to high-frequency information (fine details and sharp edges) compared to low-frequency information (broad shapes and gradients).

This biological reality underpins the technique of **Chroma Subsampling**, a staple of JPEG, WebP, and AVIF. By separating an image into Luma (Y) and Chroma (Cb/Cr or U/V) components, encoders can reduce the resolution of the color channels without a perceived loss of sharpness for most photographic content. The standard 4:2:0 subsampling scheme reduces color resolution by half both horizontally and vertically, effectively discarding 75% of the color data. While efficient for natural images, this technique creates visible artifacts in synthetic graphics, particularly where sharp transitions between contrasting colors occur (e.g., red text on a blue background), a phenomenon known as "chroma bleeding."

Another critical psychovisual concept is **Masking**, where the presence of one visual stimulus reduces the visibility of another. Texture masking allows encoders to hide quantization noise within complex textures, such as grass or asphalt, because the HVS is overwhelmed by the high-frequency detail. Luminance masking similarly suggests that noise is less visible in very bright or very dark areas compared to mid-tones. Modern encoders like JPEG XL and AVIF incorporate sophisticated models of these masking effects to allocate bits where they matter most to the viewer, rather than striving for mathematical precision across the entire frame.2

## **3\. Format Architectures: A Comparative Analysis**

The evolution of image formats traces a path from simple matrix storage to complex predictive coding derived from video compression technology.

### **3.1 JPEG (Joint Photographic Experts Group)**

**Architecture:** Block-based Discrete Cosine Transform (DCT).

The JPEG format, standardized in the early 1990s, remains the ubiquitous baseline for photographic compression. Its architecture relies on dividing the image into fixed $8 \\times 8$ pixel blocks. Each block undergoes a Discrete Cosine Transform, which converts spatial pixel data into frequency domain coefficients. The "DC" coefficient represents the average color of the block, while "AC" coefficients represent increasingly fine details.

The primary mechanism of loss in JPEG is **quantization**. The frequency coefficients are divided by values in a quantization matrix and rounded to the nearest integer. High-frequency coefficients are divided by larger numbers, often rounding them to zero. This effectively removes the fine detail that the eye is least likely to notice. The resulting sparse matrix is then entropy-coded using Huffman algorithms.

**Limitations:** The rigid $8 \\times 8$ grid structure is JPEG's Achilles' heel. At low bitrates, the boundaries between blocks become visible, creating "blocking artifacts." Furthermore, the inability to efficiently handle sharp edges without using excessive bits leads to "ringing artifacts" (Gibbs phenomenon) around text. Standard JPEG is also limited to 8-bit color depth, which can result in banding in smooth gradients, such as blue skies, and lacks support for alpha transparency.3

### **3.2 PNG (Portable Network Graphics)**

**Architecture:** Deflate (LZ77 \+ Huffman) with Predictive Filtering.

PNG was developed as a patent-free replacement for GIF, designed specifically for the lossless transmission of raster graphics. Unlike JPEG's frequency-domain approach, PNG operates in the spatial domain. Before compression, each scanline of the image is filtered. The encoder predicts the value of a pixel based on its neighbors (left, up, or diagonal) and encodes only the difference (residual) between the prediction and the actual value. Ideally, these residuals are small numbers close to zero, which compresses extremely well with Deflate.

**Strengths and Weaknesses:** PNG is the gold standard for line art, screenshots, and images with transparency. Because it preserves every pixel exactly, it avoids the ringing artifacts of JPEG. However, applying PNG to a photograph results in massive files because the "noise" of reality makes predictive filtering ineffective, leaving large residuals that Deflate cannot compress efficiently.1

### **3.3 WebP (Web Picture Format)**

**Architecture:** Derived from the VP8 video codec (Intra-frame coding).

Introduced by Google, WebP represented the first major attempt to bring video compression technologies to still images. WebP operates on macroblocks that can vary in size ($4 \\times 4$, $8 \\times 8$, $16 \\times 16$). Crucially, it employs **Intra-Prediction**, where the encoder predicts the content of a block based on previously decoded pixels in adjacent blocks. It supports multiple prediction modes (e.g., horizontal, vertical, DC).

**Nuance:** WebP supports both lossy and lossless modes.

- **Lossy WebP:** Uses predictive coding and quantization similar to VP8. It is strictly 8-bit and usually enforces 4:2:0 chroma subsampling, which can be detrimental to sharp iconographic elements.
- **Lossless WebP:** Uses a completely different algorithm involving spatial transformation, color indexing (palettes), and entropy coding, often outperforming PNG by 26% in size.

**Tools:** The primary tool, cwebp, offers sophisticated control. Parameters like \-sns (Spatial Noise Shaping) allow the user to control the amplitude of error allowed in different regions, effectively "shifting" bits to areas where artifacts would be most visible. The \-segments option divides the image into up to four partitions, each with different compression parameters, allowing for adaptive quantization.5

### **3.4 AVIF (AV1 Image File Format)**

**Architecture:** AV1 Keyframes in an ISO Base Media File Format (HEIF) container.

AVIF is the still-image derivative of the royalty-free AV1 video codec. It represents a generational leap over JPEG and WebP. AVIF divides the image into a flexible grid of blocks ranging from $128 \\times 128$ down to $4 \\times 4$. It employs sophisticated prediction tools, including **CDEF (Constrained Directional Enhancement Filter)**, which smoothes blocking artifacts along detected edges without blurring the edge itself.

A defining feature of AVIF is **Film Grain Synthesis**. High-frequency noise is expensive to encode. AVIF can mathematically model the "grain" of an image, remove it during compression (saving massive space), and then instruct the decoder to re-synthesize distinct grain patterns during display. This preserves the perceptual "texture" of a photo at very low bitrates.

**Performance:** AVIF typically achieves 50% smaller file sizes than JPEG for similar visual quality and outperforms WebP in high-fidelity scenarios. It supports 10-bit and 12-bit color depths, making it ideal for HDR (High Dynamic Range) imagery using the Perceptual Quantizer (PQ) or Hybrid Log-Gamma (HLG) transfer functions.3

### **3.5 JPEG XL (Joint Photographic Experts Group XL)**

**Architecture:** Modular Mode and VarDCT (Variable-size DCT).

JPEG XL is unique in that it was designed specifically to replace legacy JPEG, rather than being adapted from a video codec. It features two primary modes:

1. **VarDCT:** A "modernized" JPEG that allows DCT block sizes to vary from $2 \\times 2$ up to $256 \\times 256$. This flexibility allows it to encode flat areas with massive blocks (saving data) and detailed areas with tiny blocks (preserving detail), eliminating the rigid grid artifacts of legacy JPEG.
2. **Modular Mode:** A specialized engine for lossless compression, splicing, and distinct features like splines and repeating patterns, often outperforming PNG.

**The Killer Feature:** JPEG XL can losslessly transcode existing JPEG files. It parses the DCT coefficients of a legacy JPEG and repacks them into the more efficient JPEG XL entropy coding structure, reducing file size by roughly 20% without altering a single pixel of image data. This reversibility is unique to JPEG XL. Furthermore, it uses the **XYB** color space, which is physiologically derived from the specific response curves of the human retina, ensuring that quantization errors are distributed in a way that is perceptually uniform.2

### **3.6 Comparative Summary Matrix**

| Feature                | JPEG             | PNG            | WebP           | AVIF              | JPEG XL                   |
| :--------------------- | :--------------- | :------------- | :------------- | :---------------- | :------------------------ |
| **Primary Algorithm**  | Fixed DCT        | Deflate (LZ77) | VP8 Prediction | AV1 Prediction    | VarDCT / Modular          |
| **Compression Type**   | Lossy            | Lossless       | Both           | Both              | Both                      |
| **Chroma Subsampling** | 4:2:0 (Standard) | 4:4:4          | 4:2:0 (Lossy)  | 4:2:0/4:2:2/4:4:4 | 4:4:4                     |
| **Bit Depth**          | 8-bit            | 8/16-bit       | 8-bit (Lossy)  | 8/10/12-bit       | up to 32-bit float        |
| **HDR Support**        | No               | Limited        | No             | Yes               | Yes                       |
| **Legacy Transcode**   | N/A              | N/A            | No             | No                | **_Lossless Reversible_** |
| **Generation**         | 1992             | 1996           | 2010           | 2019              | 2021                      |

## **4\. Image Quality Assessment (IQA): Beyond Pixel Differences**

Evaluating the "quality" of a compressed image is a notoriously difficult engineering problem. If a compression algorithm removes 80% of the raw data, the definition of quality relies entirely on whether the removed data was "invisible" to the viewer.

### **4.1 Subjective vs. Objective Metrics**

**Subjective Assessment** involves human observers rating images under controlled conditions (Mean Opinion Score \- MOS). While this is the "ground truth," it is slow, expensive, and unscalable for automated pipelines. Consequently, researchers rely on **Objective Metrics**—algorithms that attempt to predict human perception.

### **4.2 Pixel-Based Metrics: MSE and PSNR**

**Mean Squared Error (MSE)** calculates the average of the squared intensity differences between the reference and distorted image pixels. **Peak Signal-to-Noise Ratio (PSNR)** is a logarithmic representation of MSE expressed in decibels (dB).

While computationally cheap and mathematically easy to optimize for, PSNR is fundamentally flawed as a perceptual metric. It is "blind" to structure. A slight spatial shift of an image (e.g., moving the whole image one pixel to the right) results in a catastrophic MSE/PSNR score, even though the image looks identical to a human. Conversely, severe blocking artifacts or "blur" might result in a high PSNR because the blurry pixels are mathematically "close" to the sharp originals, even if the visual experience is degraded.9

### **4.3 Structural Metrics: SSIM and MS-SSIM**

**Structural Similarity (SSIM)** was developed to address the failings of PSNR. Instead of pixel differences, it compares images based on three components: Luminance, Contrast, and Structure. It operates on local windows (typically $11 \\times 11$ pixels), assessing whether local patterns (edges, textures) have been preserved.

**Multi-Scale SSIM (MS-SSIM)** extends this by calculating SSIM at multiple resolutions. This is critical because the visibility of artifacts depends on viewing distance. An artifact visible at 1:1 zoom might disappear when the image is downscaled for a mobile screen. MS-SSIM weights the structural fidelity across these scales to provide a more robust score.10

### **4.4 Psychovisual Metrics: Butteraugli and SSIMULACRA2**

The state-of-the-art in 2025 involves metrics that explicitly model the biology of the eye.

- **Butteraugli:** Developed by Google for the Guetzli JPEG encoder and JPEG XL. It works in the XYB color space and models the density of retinal photoreceptors. It is particularly sensitive to "psychovisual" differences, punishing artifacts that trigger specific neural responses (like color banding) more than random noise. It outputs a "distance" score where lower is better.12
- **SSIMULACRA2:** Developed by the creators of JPEG XL, this metric aggregates structural similarity across multiple scales but does so in the perceptually linear XYB color space. It is tuned against a massive database of human subjective ratings, making it one of the highest-correlating metrics available for modern codecs.14

**Implications for Optimization:** When automating compression, one must choose the metric that aligns with the goal. Optimizing for PSNR often yields blurry images. Optimizing for Butteraugli or SSIMULACRA2 tends to yield images that retain texture and sharpness, even if the "mathematical" error is higher.

## **5\. Automated Analysis Framework**

To demonstrate these theoretical concepts in a practical environment, we have designed a comprehensive Python-based analysis tool. This framework automates the generation of a compression matrix, varying formats, quality settings, and effort parameters, and then subjects the output to rigorous metric evaluation.

### **5.1 Methodology and Toolchain**

The script leverages a hybrid toolchain to maximize control and compatibility:

1. **Format Encoders:**
   - **cwebp:** Used directly for WebP compression. This allows access to specific advanced flags like \-sns (Spatial Noise Shaping), \-pass (analysis passes), and \-hint (content type hints), which are often obscured by generic wrappers.
   - **ImageMagick (v7):** Used as the primary orchestration engine for converting to JPEG, PNG, AVIF, and JPEG XL. ImageMagick 7 is strictly required for its High Dynamic Range (HDRI) internal processing, ensuring that metric calculations are not clipped to 8-bit precision before comparison.
   - **Delegates:** The system relies on ImageMagick being compiled with specific delegate libraries: libheif (for AVIF), libjxl (for JPEG XL), and libjpeg-turbo.
2. Metric Calculation:  
   The script utilizes the magick compare utility to generate:
   - **AE (Absolute Error):** A count of pixels that differ between the source and destination. This is used to generate a "Difference Map" image, highlighting exactly where artifacts are occurring.
   - **RMSE (Root Mean Squared Error):** Provides a standard mathematical baseline.
   - **SSIM (Structural Similarity):** Provides a perceptual baseline.
   - _Note: While Butteraugli and SSIMULACRA2 are superior, their integration requires specific standalone binaries often not present in standard environments. The script focuses on the universally available ImageMagick metrics to ensure portability, while the logic is extensible to call external binaries if present._
3. Reporting and Visualization:  
   The automation generates a self-contained HTML report. This report moves beyond static tables by integrating:
   - **Interactive Comparison:** A JavaScript-based "swipe" slider allowing the user to scrub between the Original and Compressed versions in real-time.
   - **Difference Maps:** High-contrast visualizations of the error signal.
   - **Data Plots:** Scatter plots (generated via Matplotlib) correlating File Size (KB) against Quality Metrics (SSIM/PSNR), visualizing the "Pareto frontier" of efficiency for each format.

### **5.2 Folder Structure and Artifact Management**

To maintain scientific rigor, the script creates a new, timestamped workspace for every run (e.g., input_image_20251217_120000). Within this workspace:

- /images: Stores the generated compressed assets.
- /diffs: Stores the visualization maps of compression errors.
- /data: Stores the raw CSV data for the metrics.
- report.html: The final interactive document.

This structure ensures that multiple experimental runs (e.g., testing different cwebp preset sensitivities) can be conducted without overwriting previous data.

## **6\. Python Automation Script**

The following script encapsulates the research methodology. It includes robust argument parsing, dependency checking for ImageMagick 7, and a modular architecture for handling different encoder parameters.

In the scripts folder the `image-quality-assessment.py` is the main entry point for compressing and analyzing an image. The simplest usage is:

```pwsh
python image-quality-assessment.py myimage.png
```

It will create a folder based on the image name and timestamp with all the generated images, data and a report on that image.

## **7\. Installation and Implementation Guide**

To effectively utilize the analysis script, a robust environment capable of handling modern codecs (AVIF, JPEG XL) is required. Standard operating system package managers often ship outdated versions of ImageMagick that lack the necessary delegate libraries.

### **7.1 Prerequisites**

- **Python 3.8+**
- **ImageMagick 7.1+** (compiled with HDRI support and delegates: libheif, libjxl, libwebp, libjpeg-turbo).
- **cwebp** (part of the webp package).

### **7.2 Windows Installation**

1. **Install ImageMagick:**
   - Visit the([https://imagemagick.org/script/download.php\#windows](https://imagemagick.org/script/download.php#windows)).
   - Download the **ImageMagick-7.1.x-Q16-HDRI-x64-dll.exe** version. HDRI is essential for accurate metric calculation.
   - **Crucial Step:** During installation, check the box **"Add application directory to your system path"**.
2. **Install WebP Tools:**
   - Download libwebp binaries for Windows from the([https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html](https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html)).
   - Extract the bin folder and add it to your System PATH environment variable so cwebp can be called from the command line.
3. **Install Python Dependencies:**  
   PowerShell  
   pip install matplotlib

### **7.3 macOS Installation**

Homebrew is the standard package manager, but ensure you are installing the latest versions.

Bash

\# Update Homebrew  
brew update

\# Install ImageMagick with support for modern formats  
brew install imagemagick

\# Install WebP tools specifically  
brew install webp

\# Install Python libraries  
pip3 install matplotlib

_Note:_ Verify installation by running magick \-version. You should see heic (AVIF) and jxl listed in the "Delegates" section.

### **7.4 Linux Installation (Ubuntu/Debian)**

Most apt repositories contain outdated ImageMagick versions (v6) or v7 versions lacking libjxl. Compiling from source is recommended for research purposes.

**Step 1: Install Build Dependencies and Delegates**

Bash

sudo apt-get update  
sudo apt-get install build-essential cmake git wget \\  
 libpng-dev libjpeg-dev libtiff-dev libwebp-dev \\  
 libheif-dev libde265-dev

**Step 2: Install libjxl (if not in repo)**

Bash

sudo apt-get install libjxl-dev

**Step 3: Compile ImageMagick 7**

Bash

wget <https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-30.tar.gz>  
tar xzf 7.1.1-30.tar.gz  
cd ImageMagick-7.1.1-30  
./configure \--with-modules \--with-heic=yes \--with-jxl=yes \--with-webp=yes  
make \-j$(nproc)  
sudo make install  
sudo ldconfig

### **7.5 Google Colab / Docker Environment**

For reproducible research, a Docker container is the ideal delivery mechanism.

**Dockerfile:**

Dockerfile

FROM python:3.9\-slim-bullseye

\# Install system dependencies and build tools  
RUN apt-get update && apt-get install \-y \\  
 wget build-essential cmake git \\  
 libjpeg-dev libpng-dev libtiff-dev \\  
 libwebp-dev webp libheif-dev libjxl-dev

\# Compile ImageMagick 7 Source  
RUN wget <https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-30.tar.gz> && \\  
 tar xzf 7.1.1-30.tar.gz && \\  
 cd ImageMagick-7.1.1-30 && \\  
 ./configure \--with-heic=yes \--with-jxl=yes \--with-webp=yes && \\  
 make \-j4 && make install && ldconfig

\# Install Python plotting lib  
RUN pip install matplotlib

\# Set up working directory  
WORKDIR /analysis  
COPY compression_analyzer.py.

ENTRYPOINT \["python", "compression_analyzer.py"\]

## **8\. Conclusions and Future Outlook**

The analysis of the current bitmap landscape reveals a distinct fragmentation based on use case, driven by the varying strengths of the underlying algorithms:

1. **For Photographic Web Delivery:** **AVIF** currently offers the best trade-off for low-bandwidth scenarios (mobile 4G/5G). Its use of grain synthesis and edge-aware filtering allows it to maintain structural coherence at bitrates where JPEG breaks down into blocks and WebP loses texture detail.
2. **For Archival and High Fidelity:** **JPEG XL** is mathematically and functionally superior. Its unique ability to losslessly transcode legacy JPEGs without generation loss makes it the only viable candidate for migrating vast existing archives. Furthermore, its VarDCT implementation retains fine detail better than AVIF at high quality settings.
3. **For Compatibility:** **WebP** remains the safest general-purpose fallback. While its compression efficiency is beginning to lag behind AVIF and JXL, its widespread browser support and fast decoding make it a reliable workhorse.

The future of image compression is moving away from pixel-perfect reconstruction (PSNR-focused) toward perceptual reconstruction (texture synthesis). This shift necessitates a corresponding evolution in how we validate quality—moving from simple "diff maps" to complex psychovisual models like SSIMULACRA2. The Python toolchain provided in this report offers a foundational step for organizations to empirically validate these trade-offs on their specific image datasets, ensuring that the relentless pursuit of smaller file sizes does not come at the cost of the visual experience.

---

**References within text:**.1

#### **Works cited**

1. How to Serve Images in Next-Gen Formats: An In-Depth Guide | DebugBear, accessed December 17, 2025, [https://www.debugbear.com/blog/image-formats](https://www.debugbear.com/blog/image-formats)
2. Advanced Image Formats and When to Use Them: WebP, AVIF, HEIC, and JPEG XL, accessed December 17, 2025, [https://cloudinary.com/blog/advanced-image-formats-and-when-to-use-them](https://cloudinary.com/blog/advanced-image-formats-and-when-to-use-them)
3. \[Article\] Web Image Formats \- A quick comparison of PNG, JPG, WebP, & AVIF, accessed December 17, 2025, [https://valkyrieskies.ie/tech/articles/webimageformats.html](https://valkyrieskies.ie/tech/articles/webimageformats.html)
4. Comparison of graphics file formats \- Wikipedia, accessed December 17, 2025, [https://en.wikipedia.org/wiki/Comparison_of_graphics_file_formats](https://en.wikipedia.org/wiki/Comparison_of_graphics_file_formats)
5. cwebp | WebP \- Google for Developers, accessed December 17, 2025, [https://developers.google.com/speed/webp/docs/cwebp](https://developers.google.com/speed/webp/docs/cwebp)
6. Image file type and format guide \- Media \- MDN Web Docs \- Mozilla, accessed December 17, 2025, [https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)
7. Benchmarking JPEG XL image compression \- Infoscience, accessed December 17, 2025, [https://infoscience.epfl.ch/bitstreams/f3ec0054-ca42-497f-afbd-46d997bd948d/download](https://infoscience.epfl.ch/bitstreams/f3ec0054-ca42-497f-afbd-46d997bd948d/download)
8. Welcome to the LIVE Public-Domain Subjective Image Quality Database \- Laboratory for Image and Video Engineering, accessed December 17, 2025, [https://live.ece.utexas.edu/research/quality/subjective.htm](https://live.ece.utexas.edu/research/quality/subjective.htm)
9. Evaluation of Objective Image Quality Metrics for High-Fidelity Image Compression \- arXiv, accessed December 17, 2025, [https://arxiv.org/html/2509.13150v1](https://arxiv.org/html/2509.13150v1)
10. Subjective Assessment of Objective Image Quality Metrics Range Guaranteeing Visually Lossless Compression \- MDPI, accessed December 17, 2025, [https://www.mdpi.com/1424-8220/23/3/1297](https://www.mdpi.com/1424-8220/23/3/1297)
11. Making Sense of PSNR, SSIM, VMAF \- Visionular, accessed December 17, 2025, [https://visionular.ai/vmaf-ssim-psnr-quality-metrics/](https://visionular.ai/vmaf-ssim-psnr-quality-metrics/)
12. Guetzli \- Wikipedia, accessed December 17, 2025, [https://en.wikipedia.org/wiki/Guetzli](https://en.wikipedia.org/wiki/Guetzli)
13. butteraugli estimates the psychovisual difference between two images \- GitHub, accessed December 17, 2025, [https://github.com/google/butteraugli](https://github.com/google/butteraugli)
14. Butteraugli \- Codec Wiki, accessed December 17, 2025, [https://wiki.x266.mov/docs/metrics/butteraugli](https://wiki.x266.mov/docs/metrics/butteraugli)
15. cloudinary/ssimulacra2: SSIMULACRA 2\. Perceptual metric. \- GitHub, accessed December 17, 2025, [https://github.com/cloudinary/ssimulacra2](https://github.com/cloudinary/ssimulacra2)
16. Full-Reference Quality Metrics: VMAF, PSNR and SSIM \- TestDevLab, accessed December 17, 2025, [https://www.testdevlab.com/blog/full-reference-quality-metrics-vmaf-psnr-and-ssim](https://www.testdevlab.com/blog/full-reference-quality-metrics-vmaf-psnr-and-ssim)
17. Porting to ImageMagick Version 7, accessed December 17, 2025, [https://imagemagick.org/script/porting.php](https://imagemagick.org/script/porting.php)
18. Imagemagick support for AVIF images \- Ask Ubuntu, accessed December 17, 2025, [https://askubuntu.com/questions/1542974/imagemagick-support-for-avif-images](https://askubuntu.com/questions/1542974/imagemagick-support-for-avif-images)
19. imagemagick \- Homebrew Formulae, accessed December 17, 2025, [https://formulae.brew.sh/formula/imagemagick?default?from=gyagbbb3](https://formulae.brew.sh/formula/imagemagick?default?from=gyagbbb3)
20. Image Comparison Slider \- how to make it scalable? \- Stack Overflow, accessed December 17, 2025, [https://stackoverflow.com/questions/70056741/image-comparison-slider-how-to-make-it-scalable](https://stackoverflow.com/questions/70056741/image-comparison-slider-how-to-make-it-scalable)
21. Dics: Definitive Image Comparison Slider \- GitHub, accessed December 17, 2025, [https://github.com/abelcabezaroman/definitive-image-comparison-slider](https://github.com/abelcabezaroman/definitive-image-comparison-slider)
