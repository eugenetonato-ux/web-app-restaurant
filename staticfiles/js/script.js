/* static/js/script.js — Comportements globaux du site (menus mobiles) */

document.addEventListener('DOMContentLoaded', function () {

    /* ----- Menu burger du site public (base.html) ----- */
    const navBurgerBtn = document.getElementById('navBurgerBtn');
    const navMenuLinks = document.getElementById('navMenuLinks');

    function closeAllNavDropdowns() {
        document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
            dropdown.classList.remove('open');
            const btn = dropdown.querySelector('.nav-dropdown-toggle');
            if (btn) btn.setAttribute('aria-expanded', 'false');
        });
    }

    if (navBurgerBtn && navMenuLinks) {
        navBurgerBtn.addEventListener('click', function () {
            const isOpen = navMenuLinks.classList.toggle('mobile-open');
            navBurgerBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            navBurgerBtn.innerHTML = isOpen
                ? '<i class="fa-solid fa-xmark"></i>'
                : '<i class="fa-solid fa-bars"></i>';

            // En refermant le menu burger, on referme aussi le sous-menu Catégories
            if (!isOpen) closeAllNavDropdowns();
        });

        // Ferme le menu automatiquement après le clic sur un lien (mobile)
        navMenuLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navMenuLinks.classList.remove('mobile-open');
                navBurgerBtn.setAttribute('aria-expanded', 'false');
                navBurgerBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
                closeAllNavDropdowns();
            });
        });
    }

    /* ----- Dropdown "Catégories" du site public (clic desktop + tactile mobile) ----- */
    document.querySelectorAll('.nav-dropdown').forEach(function (dropdown) {
        const toggleBtn = dropdown.querySelector('.nav-dropdown-toggle');
        if (!toggleBtn) return;

        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = dropdown.classList.toggle('open');
            toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');

            // Un seul dropdown ouvert à la fois
            document.querySelectorAll('.nav-dropdown.open').forEach(function (other) {
                if (other !== dropdown) {
                    other.classList.remove('open');
                    const otherBtn = other.querySelector('.nav-dropdown-toggle');
                    if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
                }
            });
        });
    });

    // Ferme le dropdown Catégories si on clique en dehors (desktop)
    document.addEventListener('click', function (e) {
        document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('open');
                const btn = dropdown.querySelector('.nav-dropdown-toggle');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Ferme le dropdown Catégories avec la touche Échap
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeAllNavDropdowns();
    });

    /* ----- Caisse POS : verrouille "Montant reçu" pour les paiements électroniques ----- */
    const modePaiementSelect = document.getElementById('modePaiementSelect');
    const montantRecuInput = document.getElementById('montantRecuInput');
    const montantRecuHint = document.getElementById('montantRecuHint');

    function toggleMontantRecu() {
        if (!modePaiementSelect || !montantRecuInput) return;
        const isCash = modePaiementSelect.value === 'especes';
        montantRecuInput.readOnly = !isCash;
        montantRecuInput.style.background = isCash ? '' : '#F3F4F6';
        montantRecuInput.style.cursor = isCash ? '' : 'not-allowed';
        if (!isCash) {
            montantRecuInput.value = montantRecuInput.dataset.total || montantRecuInput.value;
        }
        if (montantRecuHint) montantRecuHint.style.display = isCash ? 'none' : 'block';
    }

    if (modePaiementSelect) {
        modePaiementSelect.addEventListener('change', toggleMontantRecu);
        toggleMontantRecu();
    }

    /* ----- Recherche admin en direct (header partagé de toutes les pages back-office) ----- */
    const adminSearchBar = document.getElementById('adminSearchBar');
    const adminSearchInput = document.getElementById('adminSearchInput');
    const adminSearchResults = document.getElementById('adminSearchResults');

    if (adminSearchBar && adminSearchInput && adminSearchResults) {
        const searchUrl = adminSearchBar.dataset.searchUrl;
        let debounceTimer = null;
        let currentController = null;

        function renderSearchResults(data) {
            const commandes = data.commandes || [];
            const plats = data.plats || [];

            if (!commandes.length && !plats.length) {
                adminSearchResults.innerHTML = '<div class="search-empty">Aucun résultat pour « ' + data.query + ' ».</div>';
                adminSearchResults.classList.add('open');
                return;
            }

            let html = '';

            if (commandes.length) {
                html += '<div class="search-section-label">Commandes</div>';
                commandes.forEach(function (cmd) {
                    html += '<a class="search-result-item" href="' + cmd.url + '">' +
                        '<div><div class="search-result-title">' + cmd.reference + '</div>' +
                        '<div class="search-result-sub">' + cmd.sous_titre + '</div></div>' +
                        '<div class="search-result-right"><span class="search-result-amount">' + cmd.total + ' FCFA</span>' +
                        '<span class="search-result-badge">' + cmd.statut + '</span></div>' +
                        '</a>';
                });
            }

            if (plats.length) {
                html += '<div class="search-section-label">Plats du menu</div>';
                plats.forEach(function (plat) {
                    html += '<a class="search-result-item" href="' + plat.url + '">' +
                        '<div><div class="search-result-title">' + plat.nom + '</div>' +
                        '<div class="search-result-sub">' + plat.categorie + '</div></div>' +
                        '<div class="search-result-right"><span class="search-result-amount">' + plat.prix + ' FCFA</span>' +
                        (!plat.disponible ? '<span class="search-result-badge unavailable">Indisponible</span>' : '') +
                        '</div></a>';
                });
            }

            adminSearchResults.innerHTML = html;
            adminSearchResults.classList.add('open');
        }

        function runAdminSearch(query) {
            if (currentController) currentController.abort();
            currentController = new AbortController();

            fetch(searchUrl + '?q=' + encodeURIComponent(query), { signal: currentController.signal })
                .then(function (res) { return res.json(); })
                .then(renderSearchResults)
                .catch(function (err) {
                    if (err.name !== 'AbortError') console.error('Erreur recherche admin :', err);
                });
        }

        adminSearchInput.addEventListener('input', function () {
            const query = adminSearchInput.value.trim();
            clearTimeout(debounceTimer);

            if (query.length < 2) {
                adminSearchResults.classList.remove('open');
                adminSearchResults.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(function () {
                runAdminSearch(query);
            }, 300);
        });

        adminSearchInput.addEventListener('focus', function () {
            if (adminSearchResults.innerHTML.trim() !== '') {
                adminSearchResults.classList.add('open');
            }
        });

        document.addEventListener('click', function (e) {
            if (!adminSearchBar.contains(e.target)) {
                adminSearchResults.classList.remove('open');
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                adminSearchResults.classList.remove('open');
                adminSearchInput.blur();
            }
        });
    }

    /* ----- Sidebar off-canvas du back-office (base_admin.html) ----- */
    const adminBurgerBtn = document.getElementById('adminBurgerBtn');
    const adminSidebar = document.getElementById('adminSidebar');
    const adminOverlay = document.getElementById('adminSidebarOverlay');

    function closeAdminSidebar() {
        if (!adminSidebar) return;
        adminSidebar.classList.remove('mobile-open');
        if (adminOverlay) adminOverlay.classList.remove('active');
        if (adminBurgerBtn) adminBurgerBtn.setAttribute('aria-expanded', 'false');
    }

    if (adminBurgerBtn && adminSidebar) {
        adminBurgerBtn.addEventListener('click', function () {
            const isOpen = adminSidebar.classList.toggle('mobile-open');
            if (adminOverlay) adminOverlay.classList.toggle('active', isOpen);
            adminBurgerBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    if (adminOverlay) {
        adminOverlay.addEventListener('click', closeAdminSidebar);
    }

    // Ferme la sidebar admin automatiquement après le clic sur un lien (mobile)
    if (adminSidebar) {
        adminSidebar.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeAdminSidebar);
        });
    }
});