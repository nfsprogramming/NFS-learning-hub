import os
import re

hub_dir = r"e:\NFS Learning Hub"
folders = [f for f in os.listdir(hub_dir) if os.path.isdir(os.path.join(hub_dir, f)) and not f.startswith('.')]

for folder in folders:
    script_path = os.path.join(hub_dir, folder, "script.js")
    if not os.path.exists(script_path):
        continue
    
    # Generate a clean course name for branding and progress key
    course_id = folder.replace("-main", "").replace("-master", "").replace("-", "_")
    course_name_display = folder.replace("-main", "").replace("-master", "").replace("-", " ").title()
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Console Log
    content = re.sub(
        r'console.log\("%c Microsoft [^|]+ \| Official Microsoft Curriculum ",',
        f'console.log("%c Microsoft {course_name_display} | Official Microsoft Curriculum ",',
        content
    )
    
    # 2. Update localStorage key
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
    
    # 3. Update notebook repository if it's there
    # (Optional but good for correctness if it follows the pattern)
    if 'githubRepo =' in content:
         repo_match = re.search(r'const githubRepo = "microsoft/([^"]+)";', content)
         if repo_match:
             potential_repo = folder.lower().replace("-main", "").replace("-master", "")
             # Only update if it seems like a generic or placeholder repo
             if "ai-for-beginners" in repo_match.group(1).lower() and "ai" not in potential_repo:
                 content = content.replace(repo_match.group(0), f'const githubRepo = "microsoft/{potential_repo}";')

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Branding updated for {folder} (Key: {course_id})")

# Also fix index.html relative paths if needed
for folder in folders:
    html_path = os.path.join(hub_dir, folder, "index.html")
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Search for absolute script paths or ambiguous ones
    # The subagent said it loaded from root.
    # If the src="script.js" is used, ensuring it has ./ might help some environments.
    # Actually, let's check for <script src="...script.js">
    content = content.replace('src="script.js', 'src="./script.js')
    content = content.replace('href="styles.css', 'href="./styles.css')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Relativity fixed for {folder}")
