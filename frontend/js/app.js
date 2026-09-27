/* ============================================
   MAIN APP JAVASCRIPT - QR MENU
   ============================================ */

// Configuration API
const API_URL = 'http://192.168.1.15:8000/api';

// Utilities
const Utils = {
    // Afficher un message temporaire
    showMessage(message, type = 'success', duration = 3000) {
        const messageEl = document.getElementById('auth-message');
        if (!messageEl) return;

        messageEl.textContent = message;
        messageEl.className = `message ${type} show`;
        messageEl.style.display = 'block';

        if (duration > 0) {
            setTimeout(() => {
                messageEl.classList.remove('show');
                messageEl.style.display = 'none';
            }, duration);
        }
    },

    // Vérifier si l'utilisateur est connecté
    isLoggedIn() {
        return !!localStorage.getItem('token');
    },

    // Obtenir le token JWT
    getToken() {
        return localStorage.getItem('token');
    },

    // Stocker le token JWT
    setToken(token) {
        localStorage.setItem('token', token);
    },

    // Supprimer le token JWT
    removeToken() {
        localStorage.removeItem('token');
    },

    // Effectuer une requête API
    async apiCall(endpoint, options = {}) {
        const url = `${API_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        // Ajouter le token d'authentification si disponible
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            ...options,
            headers,
        });

        if (!response.ok) {
            if (response.status === 401) {
                // Token invalide, déconnecter l'utilisateur
                this.removeToken();
                window.location.href = '/login.html';
            }
            throw new Error(`API Error: ${response.statusText}`);
        }

        return response.json();
    },

    // Formater un prix en DT
    formatPrice(price) {
        return `${parseFloat(price).toFixed(3)} DT`;
    },

    // Créer un slug à partir d'une chaîne
    createSlug(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_]+/g, '-')
            .replace(/^-+|-+$/g, '');
    },
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    console.log('[App] Initialisation de QR Menu');

    // Vérifier la connexion
    if (Utils.isLoggedIn()) {
        console.log('[App] Utilisateur connecté');
    } else {
        console.log('[App] Utilisateur non connecté');
    }
});

// Gestion des erreurs globales
window.addEventListener('error', (event) => {
    console.error('[Error]', event.error);
    Utils.showMessage('Une erreur est survenue', 'error');
});
