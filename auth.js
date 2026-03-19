import { auth, db } from './firebase.js';
import { 
    GoogleAuthProvider, 
    signInWithPopup, 
    signOut, 
    onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/10.7.2/firebase-auth.js";
import { 
    doc, 
    setDoc, 
    getDoc, 
    updateDoc 
} from "https://www.gstatic.com/firebasejs/10.7.2/firebase-firestore.js";

const provider = new GoogleAuthProvider();

// DOM Elements
const loginBtn = document.querySelector('.btn-premium'); // We'll repurpose or add a new login button
const navActions = document.querySelector('.nav-actions');

// Update UI based on Auth State
onAuthStateChanged(auth, async (user) => {
    if (user) {
        console.log("Logged in as:", user.displayName);
        updateUIForUser(user);
        loadUserProgress(user.uid);
    } else {
        console.log("Logged out");
        updateUIForGuest();
    }
});

function updateUIForUser(user) {
    const navActions = document.querySelector('.nav-actions');
    navActions.innerHTML = `
        <button class="btn-gold" onclick="openPremiumModal()">Premium Pro</button>
        <div class="user-profile" id="user-profile-btn" onclick="toggleLogoutMenu(event)">
            <img src="${user.photoURL}" alt="Profile">
            <span>${user.displayName.split(' ')[0]}</span>
        </div>
        <div id="logout-menu">
            <div style="padding: 10px 15px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 5px;">
                <div style="color: #fff; font-size: 0.85rem; font-weight: 700;">${user.displayName}</div>
                <div style="color: #64748b; font-size: 0.75rem;">${user.email}</div>
            </div>
            <button class="logout-item" onclick="viewProgress()">
                <i class="fa-solid fa-chart-line" style="color:#00f2ff;"></i> My Progress
            </button>
            <button class="logout-item" onclick="openPremiumModal()">
                <i class="fa-solid fa-certificate" style="color:#ffc107;"></i> My Certificates
            </button>
            <button class="logout-item danger" onclick="handleLogout()">
                <i class="fa-solid fa-right-from-bracket"></i> Logout
            </button>
        </div>
    `;
}

function updateUIForGuest() {
    const navActions = document.querySelector('.nav-actions');
    navActions.innerHTML = `
        <button class="btn-gold" onclick="openPremiumModal()">Premium Pro</button>
        <button class="btn-white" onclick="handleLogin()" title="Login to save progress">
            <i class="fa-brands fa-google"></i> Sign in
        </button>
    `;
}

window.handleLogin = async () => {
    try {
        await signInWithPopup(auth, provider);
    } catch (error) {
        console.error("Login Error:", error);
    }
};

window.handleLogout = async () => {
    try {
        await signOut(auth);
    } catch (error) {
        console.error("Logout Error:", error);
    }
};

window.toggleLogoutMenu = (e) => {
    if (e) e.stopPropagation();
    const menu = document.getElementById('logout-menu');
    if (menu) menu.classList.toggle('show');
};

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    const menu = document.getElementById('logout-menu');
    const profileBtn = document.getElementById('user-profile-btn');
    if (menu && menu.classList.contains('show') && !menu.contains(e.target) && !profileBtn.contains(e.target)) {
        menu.classList.remove('show');
    }
});

window.toggleSearch = () => {
    const bar = document.getElementById('search-bar');
    bar.classList.toggle('active');
    if (bar.classList.contains('active')) {
        document.getElementById('search-input').focus();
    }
};

window.filterCourses = (query) => {
    const q = query.toLowerCase();
    document.querySelectorAll('.course-card').forEach(card => {
        const name = card.querySelector('.course-name').textContent.toLowerCase();
        const info = card.querySelector('.course-info').textContent.toLowerCase();
        if (name.includes(q) || info.includes(q)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
};

window.showComingSoon = (feature) => {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-clock-rotate-left"></i> ${feature} Coming Soon!`;
    container.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 3s
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3000);
};

window.viewProgress = () => {
    document.querySelector('.course-section').scrollIntoView({ behavior: 'smooth' });
    const menu = document.getElementById('logout-menu');
    if (menu) menu.classList.remove('show');
};

// Progress management
async function loadUserProgress(uid) {
    const docRef = doc(db, "users", uid);
    const docSnap = await getDoc(docRef);
    
    if (docSnap.exists()) {
        const progress = docSnap.data().progress || {};
        applyProgressToUI(progress);
    }
}

function applyProgressToUI(progress) {
    // Find course cards and mark them as completed if they are in the database
    document.querySelectorAll('.course-card').forEach(card => {
        const courseName = card.querySelector('.course-name').textContent;
        if (progress[courseName] === 'Completed') {
            if (!card.querySelector('.status-badge')) {
                const badge = document.createElement('div');
                badge.className = 'status-badge';
                badge.textContent = 'Completed';
                card.appendChild(badge);
                card.classList.add('active');
            }
        }
    });
}

// Function to save progress (can be called from individual course pages later)
window.saveCourseProgress = async (courseName, status) => {
    const user = auth.currentUser;
    if (!user) return;

    const docRef = doc(db, "users", user.uid);
    try {
        await setDoc(docRef, {
            progress: {
                [courseName]: status
            }
        }, { merge: true });
        console.log("Progress saved for:", courseName);
    } catch (e) {
        console.error("Error saving progress:", e);
    }
};
