const API_URL = 'http://127.0.0.1:5000';
const token = localStorage.getItem('jwt_token');

// Protege a página
if (!token) {
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    fetchStatistics();
});

async function fetchStatistics() {
    try {
        const response = await fetch(`${API_URL}/api/statistics`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Falha ao buscar estatísticas');
        }

        const stats = await response.json();
        updateStatsUI(stats);

    } catch (error) {
        console.error("Erro:", error);
    }
}

function updateStatsUI(stats) {
    document.getElementById('total-consumed').textContent = stats.lifetime_consumed;
    document.getElementById('avg-daily').textContent = stats.average_daily_consumption;
    document.getElementById('days-on-app').textContent = stats.days_since_registration;
    document.getElementById('best-streak-stats').textContent = stats.best_streak;
}