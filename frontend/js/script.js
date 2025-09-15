const API_URL = 'http://127.0.0.1:5000';
const token = localStorage.getItem('jwt_token');

// --- DIAGNÓSTICO 1: Ver o token assim que o script carrega ---
console.log("Token lido do localStorage:", token);


// Estado do aplicativo
const appState = {
    consumed: 0,
    goal: 2000,
    streak: 0,
    best_streak: 0,
};

function protectPage() {
    if (!token) {
        window.location.href = 'login.html';
    }
}

async function fetchUserData() {
    try {
        const headers = {
            'Authorization': `Bearer ${token}`
        };

        // --- DIAGNÓSTICO 2: Ver os cabeçalhos antes de enviar a requisição ---
        console.log("Enviando requisição para /api/data com os seguintes headers:", headers);

        const response = await fetch(`${API_URL}/api/data`, { headers });
        
        if (!response.ok) {
            if (response.status === 401) logout();
            throw new Error('Falha ao buscar dados');
        }
        const data = await response.json();
        Object.assign(appState, data);
        updateUI();
    } catch (error) {
        console.error("Erro em fetchUserData:", error);
    }
}

async function saveUserData() {
    try {
        await fetch(`${API_URL}/api/data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(appState)
        });
    } catch (error) {
        console.error("Erro ao salvar dados:", error);
    }
}

function updateUI() {
    document.getElementById('consumed').textContent = appState.consumed;
    document.getElementById('goalDisplay').textContent = appState.goal;
    document.getElementById('streak').textContent = appState.streak;
    document.getElementById('bestStreak').textContent = appState.best_streak;
    updateProgressRing();
}

function updateProgressRing() {
    const ring = document.getElementById('progress-ring-fill');
    const radius = ring.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    ring.style.strokeDasharray = `${circumference} ${circumference}`;
    const progress = Math.min(appState.consumed / appState.goal, 1);
    const offset = circumference - progress * circumference;
    ring.style.strokeDashoffset = offset;
}

function addWater(amount) {
    appState.consumed += amount;
    updateUI();
    saveUserData();
}

function logout() {
    localStorage.removeItem('jwt_token');
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    protectPage();
    
    const logoutBtn = document.getElementById('logout-btn');
    const addWaterBtn = document.getElementById('add-water-btn');
    const modal = document.getElementById('add-water-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const modalActions = document.querySelector(".modal-actions");
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings-btn');
    const saveSettingsBtn = document.getElementById('save-settings-btn');
    const goalInput = document.getElementById('goal-input');

    logoutBtn.addEventListener('click', logout);
    addWaterBtn.addEventListener('click', () => modal.classList.add('visible'));
    closeModalBtn.addEventListener('click', () => modal.classList.remove('visible'));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('visible');
    });
    modalActions.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') {
            const amount = parseInt(e.target.dataset.amount);
            addWater(amount);
            modal.classList.remove('visible');
        }
    });

    settingsBtn.addEventListener('click', () => {
    goalInput.value = appState.goal; // Preenche o input com a meta atual
    settingsModal.classList.add('visible');
    });
    closeSettingsBtn.addEventListener('click', () => settingsModal.classList.remove('visible'));
    saveSettingsBtn.addEventListener('click', () => {
        const newGoal = parseInt(goalInput.value);
        if (newGoal > 0) {
            appState.goal = newGoal;
            updateUI();
            saveUserData(); // Salva o novo estado, incluindo a nova meta
            settingsModal.classList.remove('visible');
        }
    });

    fetchUserData();
});