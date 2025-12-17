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
        .navbar {{ position: fixed; top: 0; width: 100%; background: #333; color: white; padding: 15px 20px; z-index: 1000; display: flex; gap: 20px; }}
        .navbar a {{ color: white; text-decoration: none; font-weight: bold; }}
        .navbar a:hover {{ text-decoration: underline; }}
        
        .container {{ max-width: 1400px; margin: 20px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        
        .summary-box {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 30px; border-left: 5px solid #2196F3; }}
        
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 30px; margin-bottom: 50px; }}
        .graph-box {{ text-align: center; border: 1px solid #eee; padding: 15px; border-radius: 4px; background: white; }}
        .graph-box img {{ width: 100%; height: auto; }}
        
        .comparison-row {{ display: flex; flex-wrap: wrap; gap: 20px; padding: 30px 0; border-bottom: 1px solid #eee; }}
        .img-card {{ flex: 1; min-width: 45%; }}
        .img-card img {{ width: 100%; border-radius: 4px; border: 1px solid #ddd; background: #eee; }}
        
        .meta {{ background: #f8f9fa; padding: 10px; border-radius: 4px; margin-bottom: 10px; font-size: 0.95em; line-height: 1.5; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 0.85em; font-weight: bold; color: white; margin-right: 5px; }}
        .badge-webp {{ background-color: #4CAF50; }}
        .badge-jpeg {{ background-color: #2196F3; }}
        .badge-png {{ background-color: #FF9800; }}
        
        @media print {{
            .navbar {{ display: none; }}
            body {{ padding-top: 0; }}
            .graph-box {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#top">Top</a>
        <a href="#summary">Summary</a>
        <a href="#graphs">Graphs</a>
        <a href="#comparisons">Comparisons</a>
    </nav>

    <div class="container" id="top">
        <h1>Image Compression Analysis</h1>
        
        <div id="summary">
            {summary}
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
                <img src="{img_src}" loading="lazy" title="Compressed Image">
            </div>
            <div class="img-card">
                <div class="meta">
                    <strong>Difference Analysis</strong><br>
                    {metrics}
                </div>
                <img src="{diff_src}" loading="lazy" title="Difference Map">
            </div>
        </div>
"""

HTML_FOOTER = """
    </div>
</body>
</html>
"""

# ==============================================================================
# Execution Guard
# ==============================================================================
if __name__ == "__main__":
    print("\n[!] This is a library file and cannot be run directly.")
    print(f"    Please run the main script instead:\n")
    print(f"    python scripts/compression_analyzer.py <image_path>\n")
    sys.exit(1)