/* static/js/panier.js — Script de gestion du panier client AJAX */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToCart(itemId, quantite = 1) {
    const csrftoken = getCookie('csrftoken');
    
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            item_id: itemId,
            quantite: quantite,
            action: 'add'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mettre à jour le badge du panier
            const badges = document.querySelectorAll('.cart-badge');
            badges.forEach(b => b.textContent = data.cart_count);
            
            // Feedback visuel rapide
        } else {
            alert("Erreur: " + data.error);
        }
    })
    .catch(err => console.error("Erreur lors de l'ajout au panier:", err));
}

/* ----- Suppression d'un article / vidage du panier (panier.html) ----- */
function removeFromCart(itemId) {
    const csrftoken = getCookie('csrftoken');

    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            item_id: itemId,
            action: 'remove'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Erreur: " + data.error);
        }
    })
    .catch(err => console.error("Erreur lors de la suppression de l'article:", err));
}

function clearCart() {
    const overlay = document.getElementById('clearCartModalOverlay');
    if (overlay) overlay.classList.add('open');
}

function performClearCart() {
    const csrftoken = getCookie('csrftoken');

    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            item_id: null,
            action: 'clear'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Erreur: " + data.error);
        }
    })
    .catch(err => console.error("Erreur lors du vidage du panier:", err));
}

/* ----- Modal de confirmation avant ajout au panier ----- */
let pendingAddToCart = null;

function confirmAddToCart(itemId, itemName, quantite = 1) {
    pendingAddToCart = { itemId: itemId, quantite: quantite };

    const overlay = document.getElementById('addToCartModalOverlay');
    const textEl = document.getElementById('addToCartModalText');
    if (textEl) {
        textEl.innerHTML = 'Souhaitez-vous ajouter <strong>' + itemName + '</strong> à votre panier ?';
    }
    if (overlay) overlay.classList.add('open');
}

function closeAddToCartModal() {
    pendingAddToCart = null;
    const overlay = document.getElementById('addToCartModalOverlay');
    if (overlay) overlay.classList.remove('open');
}

document.addEventListener('DOMContentLoaded', function () {
    const overlay = document.getElementById('addToCartModalOverlay');
    const cancelBtn = document.getElementById('addToCartCancelBtn');
    const confirmBtn = document.getElementById('addToCartConfirmBtn');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeAddToCartModal);
    }

    if (overlay) {
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) closeAddToCartModal();
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (pendingAddToCart) {
                addToCart(pendingAddToCart.itemId, pendingAddToCart.quantite);
            }
            closeAddToCartModal();
        });
    }

    // Modal de confirmation "Vider le panier"
    const clearOverlay = document.getElementById('clearCartModalOverlay');
    const clearCancelBtn = document.getElementById('clearCartCancelBtn');
    const clearConfirmBtn = document.getElementById('clearCartConfirmBtn');

    if (clearCancelBtn) {
        clearCancelBtn.addEventListener('click', function () {
            if (clearOverlay) clearOverlay.classList.remove('open');
        });
    }

    if (clearOverlay) {
        clearOverlay.addEventListener('click', function (e) {
            if (e.target === clearOverlay) clearOverlay.classList.remove('open');
        });
    }

    if (clearConfirmBtn) {
        clearConfirmBtn.addEventListener('click', function () {
            if (clearOverlay) clearOverlay.classList.remove('open');
            performClearCart();
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeAddToCartModal();
            if (clearOverlay) clearOverlay.classList.remove('open');
        }
    });
});