/* ============================================
   AUTHENTICATION JAVASCRIPT - QR MENU
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Si l'utilisateur est déjà connecté, rediriger vers dashboard
    if (Utils.isLoggedIn()) {
        window.location.href = '/dashboard.html';
    }
});

// Gérer la connexion
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        Utils.showMessage('Tous les champs sont requis', 'error');
        return;
    }

    try {
        // Appel API de connexion
        const response = await Utils.apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                email,
                password,
            }),
        });

        // Stocker le token
        Utils.setToken(response.access_token);

        Utils.showMessage('Connexion réussie!', 'success', 1500);

        // Rediriger vers le dashboard après 1.5 secondes
        setTimeout(() => {
            window.location.href = '/dashboard.html';
        }, 1500);
    } catch (error) {
        console.error('[Auth] Login error:', error);
        Utils.showMessage('Email ou mot de passe incorrect', 'error');
    }
}

// Gérer l'inscription (à implémenter plus tard)
async function handleRegister(email, password, name) {
    try {
        const response = await Utils.apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                email,
                password,
                name,
            }),
        });

        // Stocker le token
        Utils.setToken(response.access_token);

        return response;
    } catch (error) {
        console.error('[Auth] Register error:', error);
        throw error;
    }
}

// Déconnexion
function logout() {
    Utils.removeToken();
    window.location.href = '/login.html';
}
