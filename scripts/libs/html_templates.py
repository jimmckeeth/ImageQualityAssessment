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
        :root {{
            --bg-body: #f5f5f5;
            --bg-container: #ffffff;
            --text-main: #1a202c;
            --text-muted: #4a5568;
            --border-color: #e2e8f0;
            --nav-bg: #2d3748;
            --nav-text: #e2e8f0;
            --summary-bg: #ebf8ff;
            --summary-border: #4299e1;
            --card-bg: #f7fafc;
            --card-border: #e2e8f0;
            --meta-bg: #f7fafc;
            --meta-border: #cbd5e0;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-body: #1a202c;
                --bg-container: #2d3748;
                --text-main: #f7fafc;
                --text-muted: #a0aec0;
                --border-color: #4a5568;
                --nav-bg: #171923;
                --nav-text: #e2e8f0;
                --summary-bg: #2c5282;
                --summary-border: #63b3ed;
                --card-bg: #2d3748;
                --card-border: #4a5568;
                --meta-bg: #4a5568;
                --meta-border: #718096;
            }}
            img {{ opacity: 0.9; }}
        }}

        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; background: var(--bg-body); color: var(--text-main); padding-top: 60px; transition: background 0.3s, color 0.3s; }}
        
        /* Navigation */
        .navbar {{ position: fixed; top: 0; width: 100%; background: var(--nav-bg); color: var(--nav-text); padding: 15px 20px; z-index: 1000; display: flex; gap: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
        .navbar a {{ color: var(--nav-text); text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }}
        .navbar a:hover {{ color: white; text-decoration: none; }}
        
        .container {{ max-width: 1400px; margin: 20px auto; background: var(--bg-container); padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: var(--text-main); border-bottom: 2px solid var(--border-color); padding-bottom: 12px; margin-top: 40px; }}
        h1 {{ margin-top: 0; }}
        
        /* Summary & Metrics Info */
        .summary-box {{ background: var(--summary-bg); padding: 20px; border-radius: 6px; margin-bottom: 30px; border-left: 5px solid var(--summary-border); }}
        .metric-explanations {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 40px; }}
        .metric-card {{ background: var(--card-bg); padding: 15px; border-radius: 6px; border: 1px solid var(--card-border); font-size: 0.9em; color: var(--text-main); }}
        .metric-card h4 {{ margin: 0 0 5px 0; color: var(--text-main); }}
        .metric-card a {{ color: #3182ce; text-decoration: none; font-size: 0.85em; }}
        .metric-card a:hover {{ text-decoration: underline; }}
        
        /* Graphs - Full Width */
        .metrics-grid {{ display: grid; grid-template-columns: 1fr; gap: 40px; margin-bottom: 60px; }}
        .graph-box {{ text-align: center; border: 1px solid var(--border-color); padding: 20px; border-radius: 8px; background: var(--bg-container); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .graph-box h3 {{ margin-top: 0; color: var(--text-muted); font-size: 1.2rem; }}
        .graph-box picture, .graph-box img {{ width: 100%; height: auto; max-height: 600px; object-fit: contain; cursor: zoom-in; }}
        
        /* Comparisons */
        .comparison-row {{ display: flex; flex-wrap: wrap; gap: 30px; padding: 30px 0; border-bottom: 1px solid var(--border-color); align-items: flex-start; }}
        .img-card {{ flex: 1; min-width: 45%; }}
        .img-card img {{ width: 100%; border-radius: 6px; border: 1px solid var(--border-color); background: #edf2f7; cursor: zoom-in; transition: transform 0.2s; }}
        .img-card img:hover {{ border-color: #a0aec0; }}
        
        .meta {{ background: var(--meta-bg); padding: 12px; border-radius: 6px; margin-bottom: 12px; font-size: 0.95em; line-height: 1.6; border-left: 4px solid var(--meta-border); color: var(--text-main); }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: white; margin-right: 8px; text-transform: uppercase; letter-spacing: 0.05em; }}
        .badge-webp {{ background-color: #48bb78; }}
        .badge-jpeg {{ background-color: #4299e1; }}
        .badge-png {{ background-color: #ed8936; }}
        .badge-avif {{ background-color: #9f7aea; }}
        
        /* Lightbox Generic */
        .lightbox {{ display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; overflow: hidden; background-color: rgba(0,0,0,0.95); justify-content: center; align-items: center; flex-direction: column; }}
        .lightbox-content {{ max-width: 95%; max-height: 85vh; object-fit: contain; animation: zoom 0.3s; }}
        .lightbox-caption {{ color: white; margin-top: 15px; font-size: 1.1rem; text-align: center; background: rgba(0,0,0,0.5); padding: 5px 15px; border-radius: 20px; }}
        .lightbox-close {{ position: absolute; top: 20px; right: 30px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; transition: 0.3s; z-index: 2001; }}
        .lightbox-close:hover {{ color: #bbb; }}
        
        /* Lightbox Nav Buttons */
        .lightbox-nav {{ position: absolute; top: 50%; padding: 16px; margin-top: -50px; color: white; font-weight: bold; font-size: 30px; cursor: pointer; border-radius: 3px; user-select: none; background: rgba(0,0,0,0.3); transition: 0.3s; z-index: 2001; }}
        .lightbox-nav:hover {{ background: rgba(0,0,0,0.8); }}
        .prev {{ left: 20px; }}
        .next {{ right: 20px; }}
        .up {{ top: 60px; left: 50%; transform: translateX(-50%); margin-top: 0; padding: 10px 30px; }}
        .down {{ top: auto; bottom: 60px; left: 50%; transform: translateX(-50%); margin-top: 0; padding: 10px 30px; }}

        @keyframes zoom {{ from {{transform:scale(0.9)}} to {{transform:scale(1)}} }}
        
        @media print {{
            .navbar, .lightbox {{ display: none; }}
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
        <div class="comparison-row" data-index="{index}">
            <div class="img-card">
                <div class="meta">
                    <span class="badge badge-{format}">{format}</span> 
                    <strong>{filename}</strong><br>
                    Settings: Q{quality} | Size: {size} KB <br>
                    Details: {details}
                </div>
                <img src="{img_src}" class="lb-trigger-img" data-type="img" data-row="{index}" loading="lazy" title="Click to inspect">
            </div>
            <div class="img-card">
                <div class="meta">
                    <strong>Difference Analysis</strong><br>
                    {metrics}
                </div>
                <img src="{diff_src}" class="lb-trigger-img" data-type="diff" data-row="{index}" loading="lazy" title="Click to inspect">
            </div>
        </div>
"""

HTML_FOOTER = """
    </div>

    <!-- Lightbox 1: Charts -->
    <div id="lb-charts" class="lightbox">
        <span class="lightbox-close" onclick="closeLb('charts')">&times;</span>
        <img class="lightbox-content" id="lb-charts-img">
        <div class="lightbox-caption" id="lb-charts-caption"></div>
        <a class="lightbox-nav prev" onclick="navCharts(-1)">&#10094;</a>
        <a class="lightbox-nav next" onclick="navCharts(1)">&#10095;</a>
    </div>

    <!-- Lightbox 2: Images/Diffs -->
    <div id="lb-imgs" class="lightbox">
        <span class="lightbox-close" onclick="closeLb('imgs')">&times;</span>
        
        <div style="position: relative; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
            <img class="lightbox-content" id="lb-imgs-img">
            
            <!-- Navigation UI Hints -->
            <a class="lightbox-nav prev" onclick="navImgs(-1, 0)" title="Previous Row (Left)">&#10094;</a>
            <a class="lightbox-nav next" onclick="navImgs(1, 0)" title="Next Row (Right)">&#10095;</a>
            <a class="lightbox-nav up" onclick="navImgs(0, -1)" title="Toggle View (Up)">&#9650; Image/Diff</a>
            <a class="lightbox-nav down" onclick="navImgs(0, 1)" title="Toggle View (Down)">&#9660; Image/Diff</a>
        </div>
        
        <div class="lightbox-caption" id="lb-imgs-caption"></div>
    </div>

    <script>
        // --- DATA COLLECTION ---
        // Charts
        const chartImgs = Array.from(document.querySelectorAll('.graph-box img'));
        let chartIdx = 0;

        // Comparison Rows (Structured Data)
        // We scan the rows to build a 2D-like structure: [row_index][0=img, 1=diff]
        const compRows = Array.from(document.querySelectorAll('.comparison-row'));
        const rowData = compRows.map(row => {
            const imgs = row.querySelectorAll('img.lb-trigger-img');
            return {
                img: imgs[0],  // The compressed image
                diff: imgs[1], // The difference map
                meta: row.querySelector('.meta').innerText.split('\\n')[0] // Basic title
            };
        });
        
        let curRow = 0;
        let curView = 0; // 0 = Image, 1 = Diff

        // --- CHART LIGHTBOX FUNCTIONS ---
        function openCharts(index) {
            chartIdx = index;
            const img = chartImgs[chartIdx];
            // Handle Dark Mode Source Switching if available
            
            const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            let src = img.src;
            if (isDark && img.dataset.darkSrc) {
                src = img.dataset.darkSrc;
            }

            document.getElementById('lb-charts-img').src = src;
            document.getElementById('lb-charts-caption').innerText = img.dataset.caption || "Chart";
            document.getElementById('lb-charts').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function navCharts(dir) {
            chartIdx += dir;
            if (chartIdx < 0) chartIdx = chartImgs.length - 1;
            if (chartIdx >= chartImgs.length) chartIdx = 0;
            openCharts(chartIdx);
        }

        // --- IMAGE LIGHTBOX FUNCTIONS ---
        function openImgs(rowIndex, viewIndex) {
            curRow = parseInt(rowIndex);
            curView = parseInt(viewIndex);
            updateImgView();
            document.getElementById('lb-imgs').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }

        function updateImgView() {
            if (curRow < 0) curRow = rowData.length - 1;
            if (curRow >= rowData.length) curRow = 0;
            
            // Toggle view (0 or 1)
            if (curView < 0) curView = 1; 
            if (curView > 1) curView = 0;

            const data = rowData[curRow];
            const targetImg = curView === 0 ? data.img : data.diff;
            const typeLabel = curView === 0 ? "Compressed Image" : "Difference Map";

            document.getElementById('lb-imgs-img').src = targetImg.src;
            document.getElementById('lb-imgs-caption').innerText = `[${curRow+1}/${rowData.length}] ${data.meta} - ${typeLabel}`;
        }

        function navImgs(rowDir, viewDir) {
            if (rowDir !== 0) {
                curRow += rowDir;
            }
            if (viewDir !== 0) {
                curView += viewDir;
            }
            updateImgView();
        }

        // --- SHARED UTILS ---
        function closeLb(id) {
            document.getElementById('lb-' + id).style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        // --- EVENT BINDING ---
        // Bind Charts
        chartImgs.forEach((img, idx) => {
            img.addEventListener('click', () => openCharts(idx));
        });

        // Bind Images
        rowData.forEach((data, rIdx) => {
            data.img.addEventListener('click', () => openImgs(rIdx, 0));
            data.diff.addEventListener('click', () => openImgs(rIdx, 1));
        });

        // Keyboard Logic
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('lb-charts').style.display === 'flex') {
                if (e.key === 'ArrowLeft') navCharts(-1);
                if (e.key === 'ArrowRight') navCharts(1);
                if (e.key === 'Escape') closeLb('charts');
            }
            else if (document.getElementById('lb-imgs').style.display === 'flex') {
                if (e.key === 'ArrowLeft') navImgs(-1, 0); // Prev Image
                if (e.key === 'ArrowRight') navImgs(1, 0); // Next Image
                if (e.key === 'ArrowUp') navImgs(0, -1);   // Toggle Type
                if (e.key === 'ArrowDown') navImgs(0, 1);  // Toggle Type
                if (e.key === 'Escape') closeLb('imgs');
            }
        });

        // Close on click outside
        document.querySelectorAll('.lightbox').forEach(lb => {
            lb.addEventListener('click', (e) => {
                if (e.target === lb) {
                    lb.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            });
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