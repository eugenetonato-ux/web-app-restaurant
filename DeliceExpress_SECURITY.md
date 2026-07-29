# Délice Express — SECURITY.md

## Objectif

Ce document définit les règles de sécurité à appliquer tout au long du développement de **Délice Express**, une plateforme web développée avec **Django, Django REST Framework, PostgreSQL, Redis/Celery**, comprenant un site public de commande (sans authentification client) et un back-office administrateur (staff, menu, tables, caisse POS, rapports).

---

# Rôle de l'auditeur IA

Tu agis comme un **Architecte Sécurité Senior** spécialisé dans Django, DRF, PostgreSQL et les systèmes de commande/caisse en ligne.

Le projet est supposé avoir été développé avec l'aide d'IA (ChatGPT, Claude, Cursor, Copilot, etc.).

Tu dois :

- analyser l'intégralité de la base de code ;
- comprendre l'architecture avant toute conclusion ;
- détecter les vulnérabilités réelles ;
- proposer des corrections prêtes à copier.

Ne fais aucune supposition.

---

# Architecture de référence

```
Client (navigateur, sans compte)
   ↓
Site public (Django Templates) — catalogue, panier, commande
   ↓
API REST (DRF)
   ↓
Services métier (services.py par app)
   ↓
PostgreSQL  ←→  Redis (cache, sessions panier, quotas)
   ↓
Stockage (media/S3) — photos menu
   ↓
Back-office staff (authentifié) — menu, tables, commandes, caisse, rapports
```

La route de création de commande côté site public est **la seule surface accessible sans authentification côté "écriture"** (le client crée une commande sans compte) — elle doit être traitée comme surface d'attaque prioritaire au même titre que la caisse et les rapports, accessibles uniquement au staff authentifié.

---

# Méthodologie

## Passage 1 — Compréhension

Avant toute conclusion :

- analyser les vues et serializers DRF ;
- analyser les `services.py` de chaque app ;
- analyser le flux de commande public (`orders`, `website`) ;
- analyser la gestion du panier (session/localStorage) ;
- analyser la gestion du menu et des prix (`menu`) ;
- analyser la gestion des tables (`tables`) ;
- analyser la caisse et les reçus (`cashier`) ;
- analyser les rapports et le chiffre d'affaires (`reports`, `dashboard`) ;
- analyser l'authentification staff (`staff`) ;
- analyser le stockage média (`media/`) ;
- analyser le journal d'activité (`audit_logs` si présent).

Ne conclure qu'après cette étape.

---

## Passage 2 — Audit

Chaque point reçoit obligatoirement un verdict :

- ✅ Conforme
- ❌ Vulnérable
- ⚠️ Partiel
- ⬜ Non applicable

Ne jamais regrouper plusieurs points.

---

# Checklist

## 1. Authentification staff (back-office)

- Mot de passe hashé (jamais en clair), politique de complexité minimale
- Aucune route `/admin-panel/*` accessible sans session staff valide
- Séparation des rôles (admin / serveur / caisse) — un serveur ne doit pas accéder aux rapports financiers, un caissier ne doit pas modifier le menu
- Expiration de session raisonnable, déconnexion effective (invalidation de session)
- Protection contre le brute-force sur la page de connexion (limitation de tentatives)
- Aucun compte staff créé sans validation d'un administrateur

---

## 2. Base de données & modèles

- Validation des champs (`prix`, `quantite`, `numero_table`) côté serveur, jamais uniquement côté client
- Contraintes d'unicité (numéro de table, numéro de reçu)
- Migrations propres, réversibles, testées
- Sauvegardes automatiques et testées (restauration) — particulièrement critique pour l'historique des commandes et du chiffre d'affaires

---

## 3. Commande publique (route sans authentification)

- Le **total de la commande est recalculé et vérifié côté serveur** à partir des prix réels en base — jamais confiance au total envoyé par le panier client
- Un client ne peut pas envoyer un `prix_unitaire` arbitraire depuis le front — le serializer/service doit ignorer ce champ s'il est fourni et le recalculer
- Rate limiting sur la création de commande (anti spam / anti commandes fantômes)
- Validation stricte : quantité positive, article `disponible = True`, table existante si `sur_place`
- Aucune donnée d'une autre commande n'est accessible via l'ID/UUID de commande sans clé de vérification (ex: numéro de commande + téléphone pour un client qui consulte le statut de sa commande)

---

## 4. Intégrité des commandes

- Le `prix_unitaire` d'un `OrderItem` est **figé au moment de la commande** — une modification ultérieure du prix dans `MenuItem` ne doit jamais impacter une commande déjà passée
- Un `MenuItem` déjà utilisé dans une commande ne peut pas être supprimé (uniquement désactivé) — pas de `on_delete=CASCADE` sur cette relation
- Le changement de statut d'une commande (`en_attente` → `preparation` → `prete` → `servie` → `payée`) suit un ordre logique contrôlé côté serveur — pas de saut arbitraire de statut depuis le front sans passage par le service métier
- Une commande `annulée` ne peut plus être modifiée ni encaissée

---

## 5. Caisse (POS) & reçus

- Un `Receipt` ne peut être généré qu'après confirmation explicite d'encaissement par un membre du staff authentifié
- Le staff ayant encaissé (`encaisse_par`) est systématiquement enregistré
- Le numéro de reçu est unique, non réutilisable, et idéalement séquentiel par jour ou horodaté (traçabilité)
- Un reçu déjà émis est **non modifiable** — toute correction nécessite une commande d'annulation/avoir tracée, jamais une édition du reçu existant
- Le mode de paiement (`especes` / `mobile_money`) est enregistré à l'encaissement, non modifiable après coup

---

## 6. Gestion des tables

- Pas de race condition permettant d'assigner deux commandes actives en conflit sur la même table simultanément (transaction atomique lors du changement de statut de table)
- Seul le staff authentifié peut modifier le statut d'une table (`libre`, `occupée`, `réservée`)
- La suppression d'une table déjà référencée par des commandes historiques est interdite (désactivation uniquement)

---

## 7. Gestion du menu & des prix

- Seul le staff avec le rôle adéquat peut créer/modifier/désactiver une catégorie ou un article de menu
- Le prix est un champ obligatoire, validé côté serveur (positif, cohérent avec la devise FCFA sans décimales parasites)
- L'historique des prix n'est pas requis en Phase 1, mais aucune modification de prix ne doit pouvoir altérer rétroactivement une commande déjà enregistrée (voir §4)

---

## 8. Rapports & chiffre d'affaires

- Le calcul du chiffre d'affaires journalier se base **exclusivement** sur les commandes au statut `payée` — jamais sur des commandes `en_attente` ou `annulée`
- Le rapport journalier est généré à la demande (pas de valeur pré-calculée modifiable manuellement en base)
- Seuls les rôles autorisés (admin, gérant) peuvent consulter/imprimer le rapport journalier et le chiffre d'affaires — pas le rôle serveur
- Aucune route ne permet de recalculer ou d'éditer manuellement un chiffre d'affaires déjà clôturé

---

## 9. API REST (DRF)

- Authentification obligatoire sur toutes les routes du back-office (menu en écriture, tables, commandes en modification, caisse, rapports)
- Les routes publiques (catalogue, création de commande) sont accessibles sans authentification mais en **lecture/écriture strictement limitée** à ce qui est nécessaire (pas d'accès à la liste de toutes les commandes, pas d'accès aux données d'un autre client)
- Permissions par rôle vérifiées à chaque endpoint, pas uniquement dans le frontend
- Pagination systématique sur les listes (commandes, historique)
- Validation stricte des serializers (`read_only_fields` explicites, notamment sur `prix_unitaire`, `total`, `statut`)
- Protection CORS limitée aux domaines autorisés (site public + éventuelle app staff séparée)

---

## 10. Stockage média (photos menu)

- Validation du type MIME réel du fichier uploadé (pas seulement l'extension)
- Limitation de la taille des fichiers uploadés
- Seul le staff autorisé peut uploader/modifier les photos du menu

---

## 11. Notifications (email, futur SMS)

- Pas d'injection possible dans le contenu des emails/SMS via les variables dynamiques (nom client, numéro de commande)
- Limitation du taux d'envoi (anti spam / anti abus)
- Aucune donnée sensible du restaurant (chiffre d'affaires, coordonnées d'autres clients) dans une notification envoyée au client

---

## 12. Journal d'activité

- Connexions staff, création/modification de menu, changements de statut de commande, encaissements journalisés
- Journaux non modifiables a posteriori (append-only)
- Aucune donnée sensible en clair dans les logs (pas de mot de passe, pas de token de session)

---

## 13. Confidentialité des données client

- Seules les données strictement nécessaires sont demandées au client (nom, téléphone) — pas d'adresse complète ni d'email obligatoire pour une commande sur place
- Aucune donnée client affichée publiquement (le suivi de commande, s'il existe, nécessite une clé de vérification propre au client, ex: numéro de commande + téléphone)
- Conservation des données clients limitée à ce qui est nécessaire au service (pas de profilage sans consentement)

---

## 14. Préparation évolutions futures

Vérifier que l'architecture permet d'ajouter, **sans modifier les autres modules** :

- Paiement en ligne (Mobile Money, FedaPay) en complément de la caisse physique
- Comptes clients optionnels (historique, fidélité)
- Réservation de table en ligne
- Notifications WhatsApp/SMS
- Gestion multi-restaurant (plusieurs points de vente sous une même plateforme)

---

# Format des vulnérabilités

Pour chaque vulnérabilité :

- Gravité
- Emplacement
- Description
- Impact
- Scénario d'exploitation
- Correctif prêt à copier
- Temps estimé

---

# Rapport final

Le rapport doit contenir :

1. Évaluation globale (🔴 🟠 🟡 🟢)
2. Vulnérabilités critiques
3. Corrections rapides (< 10 minutes)
4. Plan de remédiation priorisé
5. Bonnes pratiques déjà présentes
6. Résumé complet de la checklist

---

# Principes de sécurité Délice Express

- Aucune confiance dans les données envoyées par le client public (prix, total, statut recalculés côté serveur)
- Intégrité des commandes et des reçus = priorité absolue (prix figé, reçu non modifiable après émission)
- Le chiffre d'affaires ne reflète que les commandes réellement payées
- Séparation stricte des rôles staff (admin / serveur / caisse)
- Rate limiting sur la création de commande publique (anti abus)
- Pas de secrets dans le code source
- Services à responsabilité unique (`services.py` par app)
- Journalisation sans fuite de données sensibles

Ce document est la référence de sécurité officielle du projet Délice Express.
