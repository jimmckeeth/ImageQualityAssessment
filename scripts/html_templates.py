HTML_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compression Analysis Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; }
        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 40px; }
        .graph-box { text-align: center; border: 1px solid #eee; padding: 10px; border-radius: 4px; }
        .graph-box img { max-width: 100%; height: auto; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; position: sticky; top: 0; }
        
        .comparison-row { display: flex; flex-wrap: wrap; gap: 20px; padding: 20px 0; border-bottom: 1px solid #eee; }
        .img-card { flex: 1; min-width: 300px; }
        .img-card img { width: 100%; border-radius: 4px; border: 1px solid #ddd; background: #eee; }
        .meta { font-size: 0.9em; color: #666; margin-bottom: 5px; }
        .diff-overlay { position: relative; }
        .badge { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; font-weight: bold; color: white; }
        .badge-webp { background-color: #4CAF50; }
        .badge-jpeg { background-color: #2196F3; }
        
        @media print {
            .no-print { display: none; }
            body { background: white; }
            .container { box-shadow: none; max-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Compression Analysis</h1>
        
        <div class="metrics-grid">
            <div class="graph-box">
                <h3>Size vs Quality Setting</h3>
                <img src="graphs/size_vs_quality.png" alt="Size Graph">
            </div>
            <div class="graph-box">
                <h3>Efficiency (SSIM vs Size)</h3>
                <img src="graphs/ssim_vs_size.png" alt="Efficiency Graph">
            </div>
        </div>

        <h2>Detailed Comparisons</h2>
"""

HTML_ROW = """
        <div class="comparison-row">
            <div class="img-card">
                <div class="meta">
                    <span class="badge badge-{format}">{format}</span> 
                    <strong>{filename}</strong><br>
                    Settings: Q{quality} | Size: {size} KB
                </div>
                <img src="{img_src}" loading="lazy" title="Compressed Image">
            </div>
            <div class="img-card">
                <div class="meta">
                    <strong>Difference Map</strong><br>
                    PSNR: {psnr:.2f} | SSIM: {ssim:.4f}
                </div>
                <img src="{diff_src}" loading="lazy" title="Difference Map (Highlights changes)">
            </div>
        </div>
"""

HTML_FOOTER = """
    </div>
</body>
</html>
"""