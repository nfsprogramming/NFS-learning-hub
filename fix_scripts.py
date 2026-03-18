import os

courses = [
    "Web-Dev-For-Beginners-main",
    "ML-For-Beginners-main",
    "Data-Science-For-Beginners-main",
    "generative-ai-for-beginners-main",
    "ai-agents-for-beginners-main",
    "IoT-For-Beginners-main",
    "responsible-ai-toolbox-main"
]

base_dir = r"e:\Microsoft Course"

def fix_scripts():
    for course_folder in courses:
        target_file = os.path.join(base_dir, course_folder, "script.js")
        if os.path.isfile(target_file):
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use unique localStorage key
            content = content.replace("ai_course_progress", f"course_progress_{course_folder.replace('-', '_')}")
            
            # Log message
            content = content.replace("NFS AI Masterclass", f"NFS {course_folder.replace('-', ' ')}")
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_scripts()
    print("Fixed scripts for unique progress tracking.")
