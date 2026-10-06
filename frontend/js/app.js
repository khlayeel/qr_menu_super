/* ============================================
   MAIN APP JAVASCRIPT - QR MENU
   Utilitaires partagés par toutes les pages (login, dashboard, menu client)
   ============================================ */

const Utils = {
    /**
     * Affiche une notification ("toast") en haut à droite de l'écran pour
     * confirmer chaque action de l'admin (ajout, modification, suppression...).
     * type : 'success' | 'error' | 'info'
     */
    showMessage(message, type = 'info', duration = 4000) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const icons = {
            success: '<svg viewBox="0 0 24 24" fill="none"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
            error: '<svg viewBox="0 0 24 24" fill="none"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
            info: '<svg viewBox="0 0 24 24" fill="none"><path d="M12 8v5M12 16h.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/></svg>',
        };

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <span class="toast-text">${message}</span>
            <button type="button" class="toast-close" aria-label="Fermer">&times;</button>
        `;

        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('toast-visible'));

        const remove = () => {
            toast.classList.remove('toast-visible');
            toast.addEventListener('transitionend', () => toast.remove(), { once: true });
        };

        const timer = duration > 0 ? setTimeout(remove, duration) : null;
        toast.querySelector('.toast-close').addEventListener('click', () => {
            if (timer) clearTimeout(timer);
            remove();
        });
    },

    // Formater un prix en DT
    formatPrice(price) {
        return `${parseFloat(price).toFixed(3)} DT`;
    },

    // Créer un slug à partir d'une chaîne (ex: nom de café -> URL du menu)
    createSlug(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[̀-ͯ]/g, '')
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_]+/g, '-')
            .replace(/^-+|-+$/g, '');
    },
};