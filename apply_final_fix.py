import os
import re

hub_dir = r"e:\NFS Learning Hub"
folders = [f for f in os.listdir(hub_dir) if os.path.isdir(os.path.join(hub_dir, f)) and not f.startswith('.')]

# JS Redirect Guard to force trailing slash on Vercel
redirect_script = """
    <script>
        if (!window.location.pathname.endsWith('/') && !window.location.pathname.endsWith('.html')) {
            window.location.replace(window.location.pathname + '/');
        }
    </script>
"""

for folder in folders:
    html_path = os.path.join(hub_dir, folder, "index.html")
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Insert Redirect Guard after <head>
    if '<!-- Redirect Guard -->' not in content:
        if '<head>' in content:
            content = content.replace('<head>', '<head>\n    <!-- Redirect Guard -->' + redirect_script)
    
    # 2. Ensure relative paths (use prefix ./ to be more specific)
    # Search for script.js and styles.css
    content = content.replace('src="script.js', 'src="./script.js')
    content = content.replace('href="styles.css', 'href="./styles.css?v=3.0') # Cache bust styles too
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Relativity & Guard fixed for {folder}")

# branding fix (re-run just in case)
for folder in folders:
    script_path = os.path.join(hub_dir, folder, "script.js")
    if not os.path.exists(script_path):
        continue
    
    course_id = folder.replace("-main", "").replace("-master", "").replace("-", "_")
    course_name_display = folder.replace("-main", "").replace("-master", "").replace("-", " ").title()
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update localStorage keys
    content = re.sub(
        r"localStorage.getItem\('course_progress_[^']+'\)",
        f"localStorage.getItem('course_progress_{course_id}')",
        content
    )
    content = re.sub(
        r"localStorage.setItem\('course_progress_[^']+',",
        f"localStorage.setItem('course_progress_{course_id}',",
        content
    )
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Branding verified for {folder}")
