/* ============================================
   DASHBOARD JAVASCRIPT - QR MENU
   ============================================ */

const BACKEND_URL = API_URL.replace(/\/api\/?$/, '');

let currentCafe = null;
let categories = [];
let products = [];
let editingCategoryId = null;
let editingProductId = null;

function resolveImage(path) {
    if (!path) return '';
    return path.startsWith('http') ? path : `${BACKEND_URL}${path}`;
}

function displayName(value) {
    if (!value) return '';
    if (typeof value === 'object') return value.fr || value.en || value.ar || '';
    return value;
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Dashboard] Initialisation');

    if (!Utils.isLoggedIn()) {
        window.location.href = '/login.html';
        return;
    }

    loadUserData();

    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.classList.contains('logout')) return;
        link.addEventListener('click', handleNavigation);
    });

    document.getElementById('cafe-form')?.addEventListener('submit', handleCafeUpdate);
    document.getElementById('category-form')?.addEventListener('submit', handleCategorySubmit);
    document.getElementById('product-form')?.addEventListener('submit', handleProductSubmit);

    document.getElementById('cafe-logo')?.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const preview = document.getElementById('cafe-logo-preview');
        const placeholder = document.querySelector('.logo-placeholder');
        preview.src = URL.createObjectURL(file);
        preview.classList.remove('hidden');
        if (placeholder) placeholder.classList.add('hidden');
    });

    document.querySelector('.nav-link.logout')?.addEventListener('click', (e) => {
        e.preventDefault();
        Utils.removeToken();
        window.location.href = '/login.html';
    });
});

async function loadUserData() {
    try {
        currentCafe = await Utils.apiCall('/cafes/me');
        categories = await Utils.apiCall('/categories/');
        products = await Utils.apiCall('/products/');

        updateDashboardUI();
        loadQRCode();
    } catch (error) {
        console.error('[Dashboard] Erreur lors du chargement:', error);
        Utils.showMessage('Erreur lors du chargement des données', 'error');
    }
}

function updateDashboardUI() {
    const greeting = document.getElementById('user-greeting');
    if (greeting) greeting.textContent = `Bonjour ! Bienvenue sur ${currentCafe.name}`;

    const cafeName = document.getElementById('cafe-name');
    if (cafeName) cafeName.textContent = currentCafe.name;

    document.getElementById('product-count').textContent = products.length;
    document.getElementById('category-count').textContent = categories.length;

    const cafeNameInput = document.getElementById('cafe-name-input');
    if (cafeNameInput) cafeNameInput.value = currentCafe.name || '';

    const cafeDescription = document.getElementById('cafe-description');
    if (cafeDescription) cafeDescription.value = currentCafe.description || '';

    const cafeAddress = document.getElementById('cafe-address');
    if (cafeAddress) cafeAddress.value = currentCafe.address || '';

    const cafePhone = document.getElementById('cafe-phone');
    if (cafePhone) cafePhone.value = currentCafe.phone || '';

    const logoPreview = document.getElementById('cafe-logo-preview');
    const logoPlaceholder = document.querySelector('.logo-placeholder');
    if (currentCafe.logo && logoPreview) {
        logoPreview.src = resolveImage(currentCafe.logo);
        logoPreview.classList.remove('hidden');
        if (logoPlaceholder) logoPlaceholder.classList.add('hidden');
    }

    populateCategorySelect();
    renderCategoriesList();
    renderProductsList();
}

function populateCategorySelect() {
    const select = document.getElementById('product-category');
    if (!select) return;
    select.innerHTML = categories.map(cat => `<option value="${cat.id}">${displayName(cat.name)}</option>`).join('');
}

function renderCategoriesList() {
    const container = document.getElementById('categories-list');
    if (!container) return;
    if (categories.length === 0) {
        container.innerHTML = '<p class="empty-hint">Aucune catégorie pour le moment.</p>';
        return;
    }
    container.innerHTML = categories.map(cat => `
        <div class="card">
            <h3>${displayName(cat.name)}</h3>
            <button class="btn-secondary" onclick="editCategory(${cat.id})">Modifier</button>
            <button class="btn-secondary" style="color:#c0392b;" onclick="deleteCategory(${cat.id})">Supprimer</button>
        </div>
    `).join('');
}

function renderProductCard(p, category) {
    const catName = category ? displayName(category.name) : '—';
    return `
        <div class="card">
            ${p.image ? `<img src="${resolveImage(p.image)}" alt="${displayName(p.name)}">` : ''}
            <h3>${displayName(p.name)}</h3>
            <p>${catName} · ${Utils.formatPrice(p.price)} · ${p.available ? 'Disponible' : 'Indisponible'}</p>
            <button class="btn-secondary" onclick="editProduct(${p.id})">Modifier</button>
            <button class="btn-secondary" style="color:#c0392b;" onclick="deleteProduct(${p.id})">Supprimer</button>
        </div>
    `;
}

function renderProductsList() {
    const container = document.getElementById('products-list');
    if (!container) return;
    if (products.length === 0) {
        container.innerHTML = '<p class="empty-hint">Aucun produit pour le moment.</p>';
        return;
    }

    const groups = new Map();
    categories.forEach(cat => groups.set(cat.id, { category: cat, items: [] }));
    const orphans = [];

    products.forEach(p => {
        if (groups.has(p.category_id)) {
            groups.get(p.category_id).items.push(p);
        } else {
            orphans.push(p);
        }
    });

    let html = '';

    groups.forEach(group => {
        if (group.items.length === 0) return;
        html += `
        <div class="product-group">
            <h3 class="product-group-title">${displayName(group.category.name)} <span class="product-group-count">(${group.items.length})</span></h3>
            <div class="products-grid">
                ${group.items.map(p => renderProductCard(p, group.category)).join('')}
            </div>
        </div>
        `;
    });

    if (orphans.length > 0) {
        html += `
        <div class="product-group">
            <h3 class="product-group-title">Sans catégorie <span class="product-group-count">(${orphans.length})</span></h3>
            <div class="products-grid">
                ${orphans.map(p => renderProductCard(p, null)).join('')}
            </div>
        </div>
        `;
    }

    container.innerHTML = html || '<p class="empty-hint">Aucun produit pour le moment.</p>';
}

function handleNavigation(e) {
    e.preventDefault();
    const link = e.currentTarget;
    const href = link.getAttribute('href');
    if (!href) return;

    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelectorAll('.section').forEach(section => section.classList.remove('active'));

    document.querySelectorAll(`.nav-link[href="${href}"]`).forEach(l => l.classList.add('active'));
    const section = document.getElementById(`${href.substring(1)}-section`);
    if (section) section.classList.add('active');
}

async function handleCafeUpdate(e) {
    e.preventDefault();

    const payload = {
        name: document.getElementById('cafe-name-input').value,
        description: document.getElementById('cafe-description').value,
        address: document.getElementById('cafe-address').value,
        phone: document.getElementById('cafe-phone').value,
    };

    try {
        currentCafe = await Utils.apiCall('/cafes/me', {
            method: 'PUT',
            body: JSON.stringify(payload),
        });

        const logoFile = document.getElementById('cafe-logo')?.files[0];
        if (logoFile) {
            currentCafe = await uploadFile(`/cafes/me/logo`, logoFile);
        }

        updateDashboardUI();
        Utils.showMessage('Café mis à jour avec succès', 'success');
    } catch (error) {
        console.error('[Dashboard] Erreur:', error);
        Utils.showMessage('Erreur lors de la mise à jour', 'error');
    }
}

function openCategoryModal(category = null) {
    editingCategoryId = category ? category.id : null;
    document.querySelector('#category-modal h3').textContent = category ? 'Modifier la catégorie' : 'Ajouter une catégorie';

    document.getElementById('category-name-fr').value = category ? (category.name.fr || '') : '';
    document.getElementById('category-name-en').value = category ? (category.name.en || '') : '';
    document.getElementById('category-name-ar').value = category ? (category.name.ar || '') : '';

    document.getElementById('category-modal').classList.remove('hidden');
}

function closeCategoryModal() {
    document.getElementById('category-modal').classList.add('hidden');
    document.getElementById('category-form').reset();
    editingCategoryId = null;
}

function editCategory(id) {
    const category = categories.find(c => c.id === id);
    if (category) openCategoryModal(category);
}

async function deleteCategory(id) {
    if (!confirm('Supprimer cette catégorie et tous ses produits ?')) return;
    try {
        await Utils.apiCall(`/categories/${id}`, { method: 'DELETE' });
        categories = categories.filter(c => c.id !== id);
        products = products.filter(p => p.category_id !== id);
        updateDashboardUI();
        Utils.showMessage('Catégorie supprimée', 'success');
    } catch (error) {
        console.error('[Dashboard] Erreur:', error);
        Utils.showMessage('Erreur lors de la suppression', 'error');
    }
}

async function handleCategorySubmit(e) {
    e.preventDefault();

    const fr = document.getElementById('category-name-fr').value.trim();
    const en = document.getElementById('category-name-en').value.trim();
    const ar = document.getElementById('category-name-ar').value.trim();

    if (!fr) {
        Utils.showMessage('Le nom en français est obligatoire', 'error');
        return;
    }

    const name = { fr, en: en || null, ar: ar || null };

    try {
        if (editingCategoryId) {
            const updated = await Utils.apiCall(`/categories/${editingCategoryId}`, {
                method: 'PUT',
                body: JSON.stringify({ name }),
            });
            categories = categories.map(c => c.id === editingCategoryId ? updated : c);
            Utils.showMessage('Catégorie modifiée', 'success');
        } else {
            const created = await Utils.apiCall('/categories/', {
                method: 'POST',
                body: JSON.stringify({ name, position: categories.length }),
            });
            categories.push(created);
            Utils.showMessage('Catégorie ajoutée', 'success');
        }
        updateDashboardUI();
        closeCategoryModal();
    } catch (error) {
        console.error('[Dashboard] Erreur:', error);
        Utils.showMessage('Erreur lors de l\'enregistrement', 'error');
    }
}

function openProductModal(product = null) {
    editingProductId = product ? product.id : null;
    document.querySelector('#product-modal h3').textContent = product ? 'Modifier le produit' : 'Ajouter un produit';
    populateCategorySelect();

    document.getElementById('product-name-fr').value = product ? (product.name.fr || '') : '';
    document.getElementById('product-name-en').value = product ? (product.name.en || '') : '';
    document.getElementById('product-name-ar').value = product ? (product.name.ar || '') : '';

    document.getElementById('product-category').value = product ? product.category_id : (categories[0]?.id || '');

    const desc = product && product.description ? product.description : {};
    document.getElementById('product-description-fr').value = desc.fr || '';
    document.getElementById('product-description-en').value = desc.en || '';
    document.getElementById('product-description-ar').value = desc.ar || '';

    document.getElementById('product-price').value = product ? product.price : '';
    const availableCheckbox = document.getElementById('product-available');
    if (availableCheckbox) availableCheckbox.checked = product ? product.available : true;

    document.getElementById('product-modal').classList.remove('hidden');
}

function closeProductModal() {
    document.getElementById('product-modal').classList.add('hidden');
    document.getElementById('product-form').reset();
    editingProductId = null;
}

function editProduct(id) {
    const product = products.find(p => p.id === id);
    if (product) openProductModal(product);
}

async function deleteProduct(id) {
    if (!confirm('Supprimer ce produit ?')) return;
    try {
        await Utils.apiCall(`/products/${id}`, { method: 'DELETE' });
        products = products.filter(p => p.id !== id);
        updateDashboardUI();
        Utils.showMessage('Produit supprimé', 'success');
    } catch (error) {
        console.error('[Dashboard] Erreur:', error);
        Utils.showMessage('Erreur lors de la suppression', 'error');
    }
}

async function handleProductSubmit(e) {
    e.preventDefault();

    const nameFr = document.getElementById('product-name-fr').value.trim();
    const nameEn = document.getElementById('product-name-en').value.trim();
    const nameAr = document.getElementById('product-name-ar').value.trim();
    const categoryId = document.getElementById('product-category').value;
    const descFr = document.getElementById('product-description-fr').value.trim();
    const descEn = document.getElementById('product-description-en').value.trim();
    const descAr = document.getElementById('product-description-ar').value.trim();
    const price = document.getElementById('product-price').value;
    const available = document.getElementById('product-available')?.checked ?? true;
    const imageFile = document.getElementById('product-image')?.files[0];

    const missing = [];
    if (!nameFr) missing.push('nom (français)');
    if (!nameEn) missing.push('nom (anglais)');
    if (!nameAr) missing.push('nom (arabe)');
    if (!categoryId) missing.push('catégorie');
    if (!descFr) missing.push('description (français)');
    if (!descEn) missing.push('description (anglais)');
    if (!descAr) missing.push('description (arabe)');
    if (!price) missing.push('prix');
    if (!editingProductId && !imageFile) missing.push('image');

    if (missing.length > 0) {
        Utils.showMessage(`Champs obligatoires manquants : ${missing.join(', ')}`, 'error');
        return;
    }

    const payload = {
        name: { fr: nameFr, en: nameEn, ar: nameAr },
        description: { fr: descFr, en: descEn, ar: descAr },
        category_id: parseInt(categoryId),
        price: parseFloat(price),
        available,
    };

    try {
        let product;
        if (editingProductId) {
            product = await Utils.apiCall(`/products/${editingProductId}`, {
                method: 'PUT',
                body: JSON.stringify(payload),
            });
        } else {
            product = await Utils.apiCall('/products/', {
                method: 'POST',
                body: JSON.stringify(payload),
            });
        }

        if (imageFile) {
            product = await uploadFile(`/products/${product.id}/image`, imageFile);
        }

        if (editingProductId) {
            products = products.map(p => p.id === product.id ? product : p);
            Utils.showMessage('Produit modifié', 'success');
        } else {
            products.push(product);
            Utils.showMessage('Produit ajouté', 'success');
        }

        updateDashboardUI();
        closeProductModal();
    } catch (error) {
        console.error('[Dashboard] Erreur:', error);
        Utils.showMessage('Erreur lors de l\'enregistrement', 'error');
    }
}

async function uploadFile(endpoint, file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${Utils.getToken()}` },
        body: formData,
    });

    if (!response.ok) throw new Error(`Upload échoué: ${response.statusText}`);
    return response.json();
}

async function loadQRCode() {
    try {
        const response = await fetch(`${API_URL}/qrcodes/me`, {
            headers: { 'Authorization': `Bearer ${Utils.getToken()}` },
        });
        if (!response.ok) throw new Error('QR code indisponible');

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        window.__qrBlobUrl = url;

        const img = document.getElementById('qr-image');
        if (img) img.src = url;
    } catch (error) {
        console.error('[Dashboard] Erreur QR code:', error);
    }
}

function downloadQR() {
    if (!window.__qrBlobUrl) {
        Utils.showMessage('QR code non chargé', 'error');
        return;
    }
    const a = document.createElement('a');
    a.href = window.__qrBlobUrl;
    a.download = `qrcode-${currentCafe?.slug || 'menu'}.png`;
    document.body.appendChild(a);
    a.click();
    a.remove();
}