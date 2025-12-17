# ==============================================================================
# Script Name: html_templates.py
# Description: Contains static HTML strings and CSS for the report generation.
# Note:        This is a library file. Do not run directly.
# ==============================================================================

import sys

HTML_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compression Analysis Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: #f5f5f5; padding-top: 60px; }}
        
        /* Navigation */
        .navbar {{ position: fixed; top: 0; width: 100%; background: #2d3748; color: white; padding: 15px 20px; z-index: 1000; display: flex; gap: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .navbar a {{ color: #e2e8f0; text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }}
        .navbar a:hover {{ color: white; text-decoration: none; }}
        
        .container {{ max-width: 1400px; margin: 20px auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        h1, h2 {{ color: #1a202c; border-bottom: 2px solid #edf2f7; padding-bottom: 12px; margin-top: 40px; }}
        h1 {{ margin-top: 0; }}
        
        /* Summary & Metrics Info */
        .summary-box {{ background: #ebf8ff; padding: 20px; border-radius: 6px; margin-bottom: 30px; border-left: 5px solid #4299e1; }}
        .metric-explanations {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 40px; }}
        .metric-card {{ background: #f7fafc; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.9em; }}
        .metric-card h4 {{ margin: 0 0 5px 0; color: #2d3748; }}
        .metric-card a {{ color: #3182ce; text-decoration: none; font-size: 0.85em; }}
        .metric-card a:hover {{ text-decoration: underline; }}
        
        /* Graphs - Full Width */
        .metrics-grid {{ display: grid; grid-template-columns: 1fr; gap: 40px; margin-bottom: 60px; }}
        .graph-box {{ text-align: center; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .graph-box h3 {{ margin-top: 0; color: #4a5568; font-size: 1.2rem; }}
        .graph-box img {{ width: 100%; height: auto; max-height: 600px; object-fit: contain; cursor: zoom-in; }}
        
        /* Comparisons */
        .comparison-row {{ display: flex; flex-wrap: wrap; gap: 30px; padding: 30px 0; border-bottom: 1px solid #edf2f7; align-items: flex-start; }}
        .img-card {{ flex: 1; min-width: 45%; }}
        .img-card img {{ width: 100%; border-radius: 6px; border: 1px solid #cbd5e0; background: #edf2f7; cursor: zoom-in; transition: transform 0.2s; }}
        .img-card img:hover {{ border-color: #a0aec0; }}
        
        .meta {{ background: #f7fafc; padding: 12px; border-radius: 6px; margin-bottom: 12px; font-size: 0.95em; line-height: 1.6; border-left: 4px solid #cbd5e0; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: white; margin-right: 8px; text-transform: uppercase; letter-spacing: 0.05em; }}
        .badge-webp {{ background-color: #48bb78; }}
        .badge-jpeg {{ background-color: #4299e1; }}
        .badge-png {{ background-color: #ed8936; }}
        .badge-avif {{ background-color: #9f7aea; }}
        
        /* Lightbox */
        #lightbox {{ display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; overflow: hidden; background-color: rgba(0,0,0,0.9); justify-content: center; align-items: center; }}
        .lightbox-content {{ max-width: 95%; max-height: 90vh; object-fit: contain; animation: zoom 0.3s; }}
        .lightbox-caption {{ position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: white; background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 20px; text-align: center; max-width: 80%; }}
        .lightbox-close {{ position: absolute; top: 20px; right: 30px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; transition: 0.3s; }}
        .lightbox-close:hover {{ color: #bbb; }}
        .lightbox-nav {{ position: absolute; top: 50%; width: auto; padding: 16px; margin-top: -50px; color: white; font-weight: bold; font-size: 30px; cursor: pointer; border-radius: 0 3px 3px 0; user-select: none; background: rgba(0,0,0,0.3); transition: 0.3s; }}
        .lightbox-nav:hover {{ background: rgba(0,0,0,0.8); }}
        .prev {{ left: 0; border-radius: 0 3px 3px 0; }}
        .next {{ right: 0; border-radius: 3px 0 0 3px; }}

        @keyframes zoom {{ from {{transform:scale(0.9)}} to {{transform:scale(1)}} }}
        
        @media print {{
            .navbar, #lightbox {{ display: none; }}
            body {{ padding-top: 0; }}
            .graph-box {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#top">Top</a>
        <a href="#summary">Summary</a>
        <a href="#metrics-info">Metrics</a>
        <a href="#graphs">Graphs</a>
        <a href="#comparisons">Comparisons</a>
    </nav>

    <div class="container" id="top">
        <h1>Image Compression Analysis</h1>
        
        <div id="summary">
            {summary}
        </div>

        <h2 id="metrics-info">Metric Definitions</h2>
        <div class="metric-explanations">
            {metric_explanations}
        </div>
        
        <h2 id="graphs">Performance Visualization</h2>
        <div class="metrics-grid">
            {graphs}
        </div>

        <h2 id="comparisons">Visual Inspection</h2>
"""

HTML_ROW = """
        <div class="comparison-row">
            <div class="img-card">
                <div class="meta">
                    <span class="badge badge-{format}">{format}</span> 
                    <strong>{filename}</strong><br>
                    Settings: Q{quality} | Size: {size} KB <br>
                    Details: {details}
                </div>
                <img src="{img_src}" class="lightbox-trigger" data-caption="{filename} (Q{quality})" loading="lazy" title="Click to expand">
            </div>
            <div class="img-card">
                <div class="meta">
                    <strong>Difference Analysis</strong><br>
                    {metrics}
                </div>
                <img src="{diff_src}" class="lightbox-trigger" data-caption="Diff Map: {filename}" loading="lazy" title="Click to expand">
            </div>
        </div>
"""

HTML_FOOTER = """
    </div>

    <!-- Lightbox Modal -->
    <div id="lightbox">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img">
        <div class="lightbox-caption" id="lightbox-caption"></div>
        <a class="lightbox-nav prev" onclick="changeSlide(-1)">&#10094;</a>
        <a class="lightbox-nav next" onclick="changeSlide(1)">&#10095;</a>
    </div>

    <script>
        // Lightbox Logic
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        const lightboxCaption = document.getElementById('lightbox-caption');
        let currentIndex = 0;
        
        // Collect all navigable images (graphs + comparison images)
        const images = Array.from(document.querySelectorAll('.graph-box img, .img-card img'));

        function openLightbox(index) {
            currentIndex = index;
            const img = images[currentIndex];
            
            // Set source
            lightboxImg.src = img.src;
            
            // Determine caption
            let caption = img.getAttribute('data-caption');
            if (!caption) {
                // Fallback for graphs: try previous sibling header
                const header = img.previousElementSibling;
                if (header && header.tagName === 'H3') {
                    caption = header.textContent;
                } else {
                    caption = "Image View";
                }
            }
            lightboxCaption.textContent = caption + ` (${currentIndex + 1}/${images.length})`;
            
            lightbox.style.display = "flex";
            document.body.style.overflow = "hidden"; // Prevent scrolling
        }

        function closeLightbox() {
            lightbox.style.display = "none";
            document.body.style.overflow = "auto";
        }

        function changeSlide(n) {
            currentIndex += n;
            if (currentIndex >= images.length) currentIndex = 0;
            if (currentIndex < 0) currentIndex = images.length - 1;
            openLightbox(currentIndex);
        }

        // Event Listeners
        images.forEach((img, index) => {
            img.style.cursor = 'zoom-in';
            img.addEventListener('click', () => openLightbox(index));
        });

        document.querySelector('.lightbox-close').addEventListener('click', closeLightbox);

        // Click outside to close
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });

        // Keyboard Controls
        document.addEventListener('keydown', (e) => {
            if (lightbox.style.display === "flex") {
                if (e.key === "ArrowLeft") changeSlide(-1);
                if (e.key === "ArrowRight") changeSlide(1);
                if (e.key === "Escape") closeLightbox();
            }
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n[!] This is a library file and cannot be run directly.")
    print(f"    Please run the main script instead:\n")
    print(f"    python scripts/compression_analyzer.py <image_path>\n")
    sys.exit(1)