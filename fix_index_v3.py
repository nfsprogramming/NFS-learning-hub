import os
import re

def fix_index_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'index.html':
                path = os.path.join(root, file)
                if root == directory or root == '.':
                    continue
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Bump CSS version to v=3.0 for all modules
                new_content = re.sub(r'styles\.css\?v=[0-9.]+', 'styles.css?v=3.0', content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {path} to v=3.0")

if __name__ == "__main__":
    fix_index_files(".")
