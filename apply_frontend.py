import os
import shutil

courses = {
    "AI-For-Beginners": "AI for Beginners",
    "Web-Dev-For-Beginners-main": "Web Development for Beginners",
    "ML-For-Beginners-main": "Machine Learning for Beginners",
    "Data-Science-For-Beginners-main": "Data Science for Beginners",
    "generative-ai-for-beginners-main": "Generative AI for Beginners",
    "ai-agents-for-beginners-main": "AI Agents for Beginners",
    "IoT-For-Beginners-main": "IoT for Beginners",
    "responsible-ai-toolbox-main": "Responsible AI Toolbox",
    "AI-102-AIEngineer-master": "AI-102 AI Engineer Labs",
    "AI-master": "Microsoft AI Architectures",
    "Deploy-Your-AI-Application-In-Production-main": "AI Deployment (MLOps)",
    "mslearn-ai-studio-main": "Azure AI Studio Exercises",
    "mslearn-github-copilot-dev-main": "GitHub Copilot for Developers"
}

base_dir = r"e:\Microsoft Course"
# Source is always AI-For-Beginners which is the template
source_dir = os.path.join(base_dir, "AI-For-Beginners")

def apply_frontend():
    for course_folder, course_title in courses.items():
        target_dir = os.path.join(base_dir, course_folder)
        if not os.path.isdir(target_dir): continue
        
        # 1. Copy fresh template files
        if course_folder != "AI-For-Beginners":
            print(f"Applying files to {course_folder}...")
            for filename in ["index.html", "script.js", "styles.css"]:
                shutil.copy2(os.path.join(source_dir, filename), os.path.join(target_dir, filename))
        
        # 2. Patch index.html with specific course metadata
        target_index = os.path.join(target_dir, "index.html")
        with open(target_index, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Robust replacement using ID containers if possible, but currently we use text
        # We know source file has these exact strings:
        import re
        content = re.sub(r'<title>.*?</title>', f'<title>Microsoft {course_title} | Learning Portal</title>', content)
        content = content.replace('<div class="logo-text">Course Hub</div>', f'<div class="logo-text">{course_title}</div>')
        content = re.sub(r'<h1 id="course-header-title">.*?</h1>', f'<h1 id="course-header-title">{course_title}</h1>', content)
        content = re.sub(r'<p id="course-header-desc">.*?</p>', f'<p id="course-header-desc">Official curriculum for {course_title}.</p>', content)
        
        with open(target_index, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # 3. Patch script.js for local storage isolation
        target_script = os.path.join(target_dir, "script.js")
        with open(target_script, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Replace the storage key
        safe_key = course_folder.replace('-', '_').lower()
        js_content = js_content.replace('ai_course_progress', f'progress_{safe_key}')
        
        # Replace console log
        js_content = js_content.replace('Microsoft Official Curriculum | Powered by NFS Hub', f'Microsoft {course_title} | Curated by NFS Hub')
        
        with open(target_script, 'w', encoding='utf-8') as f:
            f.write(js_content)

if __name__ == "__main__":
    apply_frontend()
    print("Clean Microsoft-branded frontend applied with correct per-course metadata.")
