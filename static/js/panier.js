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
            alert("Article ajouté au panier avec succès !");
        } else {
            alert("Erreur: " + data.error);
        }
    })
    .catch(err => console.error("Erreur lors de l'ajout au panier:", err));
}
