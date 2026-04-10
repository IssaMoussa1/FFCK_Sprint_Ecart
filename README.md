# 🛶 Analyse Performance – Sprint Canoë-Kayak

Outil d'analyse statistique des performances en Finale A des Championnats du Monde et Jeux Olympiques de sprint canoë-kayak.

Développé pour la **Direction des Équipes de France de Canoë-Kayak**.

---

## 🎯 Objectif

Caractériser les écarts de performance entre les disciplines (kayak / canoë, H / F) à l'international, et positionner les performances des athlètes français dans cette distribution mondiale.

## 📊 Métriques clés

- **% d'écart au vainqueur** : normalise les comparaisons entre épreuves et distances
- **% d'écart au K1H** : référence inter-catégorie (discipline la plus rapide)
- **Seuils de Finale A** : temps médian, P10 (niveau "top mondial"), seuil 8e rang
- **Distribution par rang** : dispersion des temps au sein d'une finale

---

## 🗂️ Structure du projet

```
canoe-sprint-analysis/
│
├── data/
│   ├── raw/           ← données brutes collectées (ne jamais modifier)
│   ├── french/        ← données de sélection française
│   └── processed/     ← données enrichies (recalculables)
│
├── scripts/
│   └── scraper_canoe_sprint.py   ← collecte automatique canoeresults.eu
│
├── dashboard/
│   └── dashboard_canoe_sprint.html   ← outil de visualisation (autonome)
│
├── docs/
│   └── methodologie.md    ← choix méthodologiques documentés
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Mise en route

### Prérequis
- Python 3.10 ou supérieur
- Un navigateur web récent (Chrome, Firefox, Edge)

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/TON_COMPTE/canoe-sprint-analysis.git
cd canoe-sprint-analysis

# Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Mac / Linux
# .venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Collecte des données

```bash
python scripts/scraper_canoe_sprint.py
```

→ Génère `data/raw/icf_sprint_finals_A_AAAA-MM-JJ.csv`

### Utiliser le dashboard

1. Ouvrir `dashboard/dashboard_canoe_sprint.html` dans un navigateur
2. Cliquer sur **Choisir le fichier** et sélectionner le CSV généré
3. (Optionnel) Charger un CSV de sélections françaises dans la section 4

---

## 📡 Sources de données

| Source | Contenu | Période |
|--------|---------|---------|
| [canoeresults.eu](http://www.canoeresults.eu/view-results/sprint) | Senior WCh + JO | 1938 → présent |
| ICF (PDF) | Junior + U23 WCh | 2001 → présent *(phase 2)* |
| FFCK | Données sélections françaises | À compléter |

---

## 🗓️ Feuille de route

- [x] Phase 1 : Senior WCh + JO, 2012–2025, Sprint
- [ ] Phase 2 : Extension historique (2001–2011)
- [ ] Phase 3 : Junior et U23
- [ ] Phase 4 : Coupes du Monde
- [ ] Phase 5 : Slalom

---

## 👥 Contact

Direction des Équipes de France de Canoë-Kayak  
Fédération Française de Canoë-Kayak et Sports de Pagaie
