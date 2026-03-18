import os
import json
import re
from typing import Any, cast

def title_case(s):
    s = re.sub(r'^\d+-', '', s)
    s = s.replace('-', ' ').replace('_', ' ')
    return s.title()

def generate_lessons_data(course_dir):
    sections = {}
    exclude_dirs = {'.git', '.github', '.vscode', '.devcontainer', 'images', 'img', 'data', 'etc', 'examples', 'pdf', 'sketchnotes', 'translations', 'translated_images', 'solutions', 'start', 'quiz-app', 'slides'}

    for root, dirs, files in os.walk(course_dir):
        keep = [d for d in dirs if d not in exclude_dirs and not str(d).startswith('.')]
        dirs.clear()
        dirs.extend(keep)
        
        # Look for readme or index.md case-insensitively
        lower_files = [f.lower() for f in files]
        if 'readme.md' in lower_files or 'index.md' in lower_files:
            if root == course_dir: continue
            
            # Find the actual filename
            actual_readme = None
            for f in files:
                if f.lower() in ['readme.md', 'index.md']:
                    actual_readme = f
                    break
                    
            rel_path = os.path.relpath(root, course_dir).replace('\\', '/')
            parts = rel_path.split('/')
            if len(parts) >= 1:
                section_name = title_case(parts[0])
                if section_name not in sections: sections[section_name] = []
                notebooks = [f for f in files if f.endswith('.ipynb')]
                lesson_title = title_case(parts[-1])
                if lesson_title.lower() == "readme" or lesson_title.lower() == "module" or lesson_title.lower() == "index":
                    lesson_title = section_name
                sections[section_name].append({
                    "title": lesson_title,
                    "path": f"{rel_path}/{actual_readme}",
                    "notebooks": notebooks
                })
        
        # Also capture standalone numbered/named .md files (common in MSLearn repos)
        for f in files:
            if f.endswith('.md') and f.lower() not in ['readme.md', 'index.md']:
                if re.match(r'^\d+-', f) or 'Instructions' in str(root).split(os.sep):
                    rel_path = os.path.relpath(os.path.join(root, f), course_dir).replace('\\', '/')
                    section_name = title_case(os.path.basename(root)) if root != course_dir else 'General'
                    if section_name not in sections: sections[section_name] = []
                    
                    # Prevent duplicates if it's already somehow added
                    section_lessons: list[Any] = cast(list, sections[section_name])
                    if not any(l['path'] == rel_path for l in section_lessons):
                        section_lessons.append({
                            "title": title_case(f.replace('.md', '')),
                            "path": rel_path,
                            "notebooks": []
                        })

    lessons_data: list[dict[str, Any]] = []
    for sec in sorted(sections.keys()):
        lessons = sections[sec]
        if lessons:
            lessons.sort(key=lambda x: x['path'])
            lessons_data.append({"section": sec, "lessons": lessons})
            
    # Fallback to display the root README.md if there are absolutely no lesson files found
    if not lessons_data:
        readme_path = None
        for f in os.listdir(course_dir):
            if f.lower() in ['readme.md', 'index.md']:
                readme_path = f
                break
        if readme_path:
            lessons_data.append({
                "section": "Overview",
                "lessons": [{
                    "title": "Course Introduction",
                    "path": readme_path,
                    "notebooks": []
                }]
            })
            
    return lessons_data

if __name__ == "__main__":
    courses = [
        "Web-Dev-For-Beginners-main",
        "ML-For-Beginners-main",
        "Data-Science-For-Beginners-main",
        "generative-ai-for-beginners-main",
        "ai-agents-for-beginners-main",
        "IoT-For-Beginners-main",
        "responsible-ai-toolbox-main",
        "AI-102-AIEngineer-master",
        "AI-master",
        "Deploy-Your-AI-Application-In-Production-main",
        "mslearn-ai-studio-main",
        "mslearn-github-copilot-dev-main"
    ]
    base_dir = r"e:\Microsoft Course"
    for course in courses:
        course_path = os.path.join(base_dir, course)
        if os.path.isdir(course_path):
            print(f"Generating for {course}...")
            data = generate_lessons_data(course_path)
            with open(os.path.join(course_path, 'lessons_data.json'), 'w') as f:
                json.dump(data, f, indent=4)
