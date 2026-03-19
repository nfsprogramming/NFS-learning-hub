import os
import re

hub_dir = r"e:\NFS Learning Hub"
folders = [f for f in os.listdir(hub_dir) if os.path.isdir(os.path.join(hub_dir, f)) and not f.startswith('.')]

for folder in folders:
    html_path = os.path.join(hub_dir, folder, "index.html")
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Redirect Guard
    # It looks like this:
    # <!-- Redirect Guard -->
    # <script>
    #     if (!window.location.pathname.endsWith('/') && !window.location.pathname.endsWith('.html')) {
    #         window.location.replace(window.location.pathname + '/');
    #     }
    # </script>
    
    pattern = r'<!-- Redirect Guard -->\s*<script>.*?</script>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Fix paths to be absolutely correct for Vercel's root-relative clean URLs
    # If the folder is Web-Dev-For-Beginners-main
    # We want the script to be Web-Dev-For-Beginners-main/script.js
    
    # But wait, if they visit with index.html, it works already.
    # If they visit without it, it breaks.
    
    # Let's try to use the folder name in the path
    old_script = f'src="./script.js'
    new_script = f'src="/{folder}/script.js'
    content = content.replace(old_script, new_script)
    
    old_style = f'href="./styles.css'
    new_style = f'href="/{folder}/styles.css'
    content = content.replace(old_style, new_style)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Loop removed and Absolute subfolder paths fixed for {folder}")
