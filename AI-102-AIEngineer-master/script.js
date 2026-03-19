console.log("%c Microsoft Ai 102 Aiengineer | Official Microsoft Curriculum ", "background: #00f2ff; color: #0a0b10; font-weight: bold; padding: 4px; border-radius: 4px;");

const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';

let courseData = [];
let progress = JSON.parse(localStorage.getItem('course_progress_AI_102_AIEngineer')) || {};
let theoryNavigationStack = [];
function syncCourseBranding() {
    const headerTitle = document.getElementById('course-header-title');
    const logoText = document.querySelector('.logo-text');
    if (headerTitle && logoText) {
        logoText.innerText = headerTitle.innerText.trim();
    }
}

// Determine base path for fetches (directory of the current script)
const scriptPath = window.location.pathname;
const baseDir = scriptPath.substring(0, scriptPath.lastIndexOf('/') + 1);

async function loadData() {
    try {
        // Fetch lessons_data.json relative to the course folder, adding timestamp to avoid aggressive caching
        const response = await fetch(`lessons_data.json?v=${new Date().getTime()}`);
        if (!response.ok) throw new Error('Data not found');
        courseData = await response.json();
        renderDashboard();
        updateOverallProgress();

        // Handle initial path routing (from hash or state)
        if (window.location.hash) {
            const path = window.location.hash.substring(1);
            if (path) openReadme(path, false, true);
        }
    } catch (error) {
        console.error('Error loading course data:', error);
    }
}

function renderDashboard() {
    const grid = document.getElementById('lesson-grid');
    const sidebarNav = document.getElementById('sidebar-nav');
    if (!grid) return;
    
    grid.innerHTML = '';
    if (sidebarNav) sidebarNav.innerHTML = '';

    courseData.forEach((section, sIdx) => {
        const navSection = document.createElement('div');
        navSection.className = 'nav-section';
        navSection.innerHTML = `<div class="nav-title">${section.section}</div>`;

        section.lessons.forEach((lesson, lIdx) => {
            const lessonId = `L-${sIdx}-${lIdx}`;

            const navItem = document.createElement('div');
            navItem.className = 'nav-item';
            navItem.innerHTML = `<i class="fa-solid fa-file-lines"></i> ${lesson.title}`;
            navItem.onclick = () => {
                const element = document.getElementById(lessonId);
                if (element) element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            };
            navSection.appendChild(navItem);

            const card = document.createElement('div');
            card.className = `lesson-card ${progress[lessonId] ? 'completed' : ''}`;
            card.id = lessonId;
            card.style.animationDelay = `${(sIdx * 0.1) + (lIdx * 0.05)}s`;

            const notebookHtml = lesson.notebooks.map(nb => `
                <div class="notebook-item" onclick="openNotebook('${lesson.path}', '${nb}', '${lessonId}')">
                    <span><i class="fa-solid fa-code"></i> ${nb}</span>
                    <i class="fa-solid fa-chevron-right"></i>
                </div>
            `).join('');

            card.innerHTML = `
                <span class="section-tag">${section.section}</span>
                <div class="lesson-title">${lesson.title}</div>
                <div class="lesson-desc">Click to open the lesson theory or jump directly into the hands-on notebooks below.</div>
                <div class="lesson-footer">
                    <button class="btn btn-primary" onclick="openReadme('${lesson.path}')">Read Theory</button>
                    <button class="btn btn-outline" onclick="toggleComplete('${lessonId}')">
                        ${progress[lessonId] ? 'Mark Incomplete' : 'Mark Completed'}
                    </button>
                </div>
                ${lesson.notebooks.length > 0 ? `<div class="notebook-list">${notebookHtml}</div>` : ''}
                <div class="completed-mark" style="position: absolute; top: 1.5rem; right: 1.5rem;">
                    ${progress[lessonId] ? '<i class="fa-solid fa-check"></i>' : ''}
                </div>
            `;
            grid.appendChild(card);
        });
        if (sidebarNav) sidebarNav.appendChild(navSection);
    });
}

async function openReadme(path, isBackNavigation = false, isInitialRoute = false) {
    const viewer = document.getElementById('theory-viewer');
    const body = document.getElementById('theory-body');
    const title = document.getElementById('theory-title');
    const backBtn = document.getElementById('theory-back');
    if (!viewer || !body || !title) return;
    
    // Manage navigation stack
    if (!isBackNavigation) {
        if (theoryNavigationStack[theoryNavigationStack.length - 1] !== path) {
            theoryNavigationStack.push(path);
            if (!isInitialRoute) {
                window.location.hash = path;
            }
        }
    }
    
    // Show modal
    viewer.style.display = 'flex';
    // Force DOM reflow to ensure transition works
    void viewer.offsetWidth;
    viewer.classList.add('active');
    
    body.innerHTML = '<div style="text-align:center; padding: 50px;"><i class="fa-solid fa-circle-notch fa-spin fa-2x"></i><p style="margin-top:20px; font-weight:700;">Loading Content...</p></div>';

    try {
        let markdown = '';
        
        const cleanPath = path.startsWith('/') ? path.substring(1) : path;
        const fullPath = cleanPath.endsWith('.md') ? cleanPath : `${cleanPath}/README.md`;
        
        const lastSlash = fullPath.lastIndexOf('/');
        const folderPath = lastSlash !== -1 ? fullPath.substring(0, lastSlash) : '';

        // Try local fetch first (relative to course folder)
        try {
            const response = await fetch(`${fullPath}?v=${new Date().getTime()}`);
            if (response.ok) {
                markdown = await response.text();
            }
        } catch (e) {
            console.log("Local fetch failed, trying fallback...");
        }

        // Fix image paths
        const basePath = folderPath ? `${folderPath}/` : '';

        if (!markdown || markdown.trim().startsWith('<!DOCTYPE') || markdown.trim().startsWith('<html')) {
             throw new Error('Lesson content not found. This might be a placeholder module.');
        }

        // Basic Markdown render (replace image paths)
        markdown = markdown.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (match, alt, imgPath) => {
            if (imgPath.startsWith('http')) return match;
            return `![${alt}](${basePath}${imgPath})`;
        });

        const cleanHtml = DOMPurify.sanitize(marked.parse(markdown));
        body.innerHTML = cleanHtml;
        title.innerText = path.split('/').pop().replace(/-/g, ' ').replace('.md', '');

        // Render Mermaid Diagrams if present
        const mermaidBlocks = body.querySelectorAll('code.language-mermaid');
        if (mermaidBlocks.length > 0) {
            mermaidBlocks.forEach(block => {
                const pre = block.parentElement;
                const div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                pre.replaceWith(div);
            });
            if (window.mermaid) {
                window.mermaid.run({ querySelector: '.mermaid' }).catch(e => console.error("Mermaid parsing error", e));
            }
        }

    } catch (error) {
        body.innerHTML = `<div style="color:var(--accent); text-align:center; padding: 50px;">
            <i class="fa-solid fa-triangle-exclamation fa-3x"></i>
            <h3 style="margin-top:1.5rem">Error Loading Content</h3>
            <p>${error.message}</p>
        </div>`;
    }
}

function closeTheory() {
    const viewer = document.getElementById('theory-viewer');
    viewer.classList.remove('active');
    setTimeout(() => { 
        viewer.style.display = 'none'; 
        theoryNavigationStack = [];
        window.location.hash = '';
    }, 300);
}

function toggleComplete(lessonId) {
    progress[lessonId] = !progress[lessonId];
    localStorage.setItem('course_progress_AI_102_AIEngineer', JSON.stringify(progress));
    renderDashboard();
    updateOverallProgress();
}

function updateOverallProgress() {
    const totalLessons = courseData.reduce((acc, section) => acc + section.lessons.length, 0);
    const completedLessons = Object.values(progress).filter(v => v).length;
    const percentage = totalLessons > 0 ? (completedLessons / totalLessons) * 100 : 0;

    const barFill = document.getElementById('progress-fill');
    const textOut = document.getElementById('progress-text');
    if (barFill) barFill.style.width = `${percentage}%`;
    if (textOut) textOut.innerText = `${completedLessons}/${totalLessons} Completed`;
}

window.onload = () => {
    syncCourseBranding();
    loadData();
};




function openNotebook(lessonPath, notebookName, lessonId) {
    // Base Colab redirect
    const githubRepo = "microsoft/ai-for-beginners"; // Fallback repo
    const branch = "main";
    let cleanPath = lessonPath.startsWith('/') ? lessonPath.substring(1) : lessonPath;
    const fullPath = `${cleanPath}/${notebookName}`;
    const colabUrl = `https://colab.research.google.com/github/${githubRepo}/blob/${branch}/${fullPath}`;
    window.open(colabUrl, '_blank');
}
