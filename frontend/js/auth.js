const API_URL = 'http://127.0.0.1:5000'; // O endereço do nosso backend

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            handleAuth(`${API_URL}/login`, { email, password });
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            handleAuth(`${API_URL}/register`, { email, password });
        });
    }
});

async function handleAuth(url, body) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.textContent = ''; // Limpa erros antigos

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Ocorreu um erro.');
        }

        if (data.access_token) {
            // Login bem-sucedido
            localStorage.setItem('jwt_token', data.access_token);
            window.location.href = 'index.html'; // Redireciona para o app principal
        } else {
            // Registro bem-sucedido
            alert(data.message);
            window.location.href = 'login.html'; // Redireciona para a página de login
        }

    } catch (error) {
        errorMessageElement.textContent = error.message;
    }
}