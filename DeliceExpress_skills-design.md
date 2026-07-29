# Délice Express — Design System (Site Public + Back-office Admin)

Ce document définit l'identité visuelle du projet, construite à partir de deux références :
- **Référence 1 (site public)** — ambiance fast-food chaleureuse, jaune/orange, cartes produits colorées.
- **Référence 2 (back-office)** — dashboard violet, sidebar de navigation, cartes arrondies, widgets chiffrés.

Deux univers visuels distincts mais cohérents : le **site public** doit donner faim et donner envie de commander vite ; le **back-office** doit être clair, dense en données, et rapide à utiliser pendant le coup de feu du service.

---

## 1. Palette de couleurs

### Site public (inspiré Référence 1)
| Rôle | Couleur | Usage |
|---|---|---|
| Primaire | `#F5A623` (jaune/orange doré) | Bannière héro, accents, badges |
| Accent chaud | `#E84C3D` (rouge tomate) | Badges "HOT", prix, CTA secondaires |
| Fond clair | `#FFFFFF` / `#FAFAFA` | Fond général |
| Texte | `#1A1A1A` | Titres |
| Texte secondaire | `#6B6B6B` | Descriptions |
| Cartes catégories | Violet `#8E5CF7`, Orange `#F5A623`, Rouge `#E8445C`, Vert `#5CC98C` | Mise en avant rotative des catégories phares |

### Back-office admin (inspiré Référence 2)
| Rôle | Couleur | Usage |
|---|---|---|
| Primaire | `#6C3CE9` (violet) | Sidebar, boutons principaux, montants clés |
| Primaire clair | `#F3EEFE` | Fond des cartes actives, hover |
| Fond général | `#F7F7FB` | Fond de page |
| Cartes | `#FFFFFF` avec ombre douce | Blocs de contenu |
| Succès | `#3CC98C` | Commande payée, table libre |
| Attention | `#F5A623` | Commande en préparation |
| Erreur | `#E8445C` | Commande annulée, table occupée |
| Texte | `#1E1E2D` | Titres |
| Texte secondaire | `#8A8A9E` | Sous-titres, labels |

---

## 2. Typographie

- **Titres (H1-H3)** : sans-serif grasse (type *Poppins* ou *Sora* Bold/SemiBold) — gros titres impactants sur la bannière héro publique, chiffres du dashboard admin en grand format.
- **Corps de texte** : sans-serif régulière (type *Inter* ou *Poppins* Regular) — bonne lisibilité sur cartes produits et tableaux.
- **Prix** : toujours en gras, suffixe **FCFA** (ex: `4 000 FCFA`, jamais de virgule décimale).

---

## 3. Site public — Composants (inspirés Référence 1)

### 3.1 En-tête
- Logo à gauche (nom "Délice Express" + icône burger/plat stylisée)
- Menu horizontal : Accueil, Menu, Catégories, Contact
- Icônes recherche + panier (badge avec nombre d'articles)
- Bouton "Commander" (au lieu de "Login" — pas de compte requis)

### 3.2 Bannière héro
- Grand bloc jaune/orange avec photo plat signature en avant-plan
- Titre impactant ("FRAIS, GÉNÉREUX & SAVOUREUX") + sous-texte promo
- Bouton CTA "Voir le menu"
- À droite : 2 tuiles secondaires — un plat vedette avec prix, une tuile ambiance/livraison

### 3.3 Catégories de menu
- Rangée de cartes carrées colorées (une couleur par catégorie : Burgers, Pizzas, Boissons, Desserts...)
- Photo du plat + nom catégorie + lien "Voir →"

### 3.4 Liste des articles (grille produits)
- Carte produit : photo, badge optionnel ("Nouveau", "Populaire"), nom, courte description, prix en FCFA, bouton rond "+" pour ajouter au panier
- Grille responsive 4 colonnes desktop / 2 colonnes mobile

### 3.5 Panier
- Panneau latéral ou page dédiée : liste des articles, quantité modifiable (+/-), sous-total par ligne, total général en FCFA
- Choix du type de commande : **Sur place** (sélection du n° de table) / **À emporter** / **Livraison**
- Champ nom + téléphone client
- Bouton "Valider ma commande"

---

## 4. Back-office admin — Composants (inspirés Référence 2)

### 4.1 Sidebar (fixe, violet foncé)
- Logo "Délice Express" en haut
- Navigation avec icônes : **Dashboard**, **Menu** (catégories/articles), **Tables**, **Commandes**, **Caisse**, **Rapports**, **Paramètres**
- Encart promo bas de sidebar remplacé par un rappel utile (ex: "Commandes en attente : 3")

### 4.2 En-tête dashboard
- Message d'accueil personnalisé ("Bonjour, [Nom du staff]")
- Barre de recherche (rechercher une commande, un article)
- Icônes notifications + profil

### 4.3 Carte "Chiffre d'affaires du jour"
- Grande carte violette (équivalent de la carte "Balance" de la référence) affichant le **CA du jour en FCFA**
- Boutons secondaires : "Voir le rapport", "Imprimer le rapport journalier"

### 4.4 Commandes en cours (équivalent "Order Menu")
- Liste des commandes actives : n° commande, table ou type (emporter/livraison), articles, total, statut coloré (badge)
- Boutons rapides pour changer de statut (En préparation → Prête → Servie)
- Bouton "Encaisser" ouvrant la caisse POS

### 4.5 Catégories & tables (équivalent rangée "Category" icônes)
- Rangée d'icônes/cartes pour gérer rapidement les catégories de menu
- Vue grille des tables du restaurant : `Table N°1`, `Table N°2`, `Table N°3`... avec statut coloré (libre = vert, occupée = rouge, réservée = orange)

### 4.6 Articles populaires / gestion menu (équivalent "Popular Dishes")
- Cartes articles avec photo, nom, prix FCFA, bouton modifier/désactiver
- Formulaire d'ajout : nom, catégorie, prix, photo, description, disponibilité

### 4.7 Caisse POS
- Récapitulatif de la commande sélectionnée, choix du mode de paiement (Espèces / Mobile Money)
- Bouton "Encaisser et imprimer le reçu"
- Le reçu est un **ticket caisse POS** (pas un PDF) : gabarit étroit format 80mm, typographie monospace/condensée pensée pour imprimante thermique — nom du restaurant, n° reçu, articles, total, date/heure, n° de table si sur place
- Impression déclenchée directement depuis le navigateur (aucun téléchargement de fichier, contrairement au rapport)

### 4.8 Rapport journalier
- Le rapport est un **fichier PDF généré au clic** (mise en page A4, logo du restaurant, date, CA total, nombre de commandes, ticket moyen, top 5 des articles vendus, répartition sur place / emporter / livraison)
- Bouton "Générer le rapport PDF" → téléchargement + aperçu, imprimable ensuite depuis le lecteur PDF
- Historique consultable des rapports déjà générés (par date)

---

## 5. Composants transverses

- **Boutons** : coins arrondis (`border-radius: 12px`), ombre légère, état hover avec léger assombrissement
- **Cartes** : coins arrondis (`16-20px`), ombre douce (`0 4px 20px rgba(0,0,0,0.06)`)
- **Badges de statut** : pastille colorée + texte court (`En préparation`, `Prête`, `Payée`, `Annulée`)
- **Montants** : toujours affichés en gras avec le suffixe `FCFA`, jamais de symbole étranger (`$`, `€`)

---

## 6. Ton et contenu

- Ton chaleureux, direct, orienté appétit sur le site public ("Fraîcheur garantie", "Commandez en 2 clics")
- Ton fonctionnel et efficace sur le back-office (pas de fioritures — le staff doit agir vite pendant le service)