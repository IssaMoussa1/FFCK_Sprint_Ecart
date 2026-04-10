# Méthodologie – Analyse Performance Sprint Canoë-Kayak

## 1. Périmètre des données

### Compétitions retenues
- **Championnats du Monde Senior** (WCh) : compétition annuelle hors années olympiques
- **Jeux Olympiques** (OG) : compétition tous les 4 ans

*Rationale : ces deux compétitions représentent le niveau d'excellence mondial le plus homogène. Les Coupes du Monde seront intégrées en phase 2 avec une pondération spécifique (certaines nations s'y alignent sélectivement).*

### Finales retenues
Uniquement les **Finales A** (rangs 1 à 9), qui rassemblent les meilleures embarcations mondiales sur chaque épreuve.

Les demi-finales et finales B sont exclues : elles contiennent des athlètes disqualifiés ou des nations de plus faible niveau représentativité.

### Catégories d'âge
- Phase 1 : **Senior uniquement**
- Phase 2 : extension aux **U23** et **Junior**

---

## 2. Métriques et choix méthodologiques

### 2.1 Pourquoi ne pas comparer les temps absolus ?

Les temps bruts ne sont **pas comparables** entre :
- Différentes compétitions (bassins différents, vent, température de l'eau)
- Différentes distances (200m ≠ 500m ≠ 1000m)
- Différentes embarcations (K1 ≠ C2, etc.)

### 2.2 Métrique principale : % d'écart au vainqueur

```
% écart au vainqueur = (temps_athlète - temps_1er) / temps_1er × 100
```

**Propriétés :**
- Élimine le biais des conditions environnementales (vent, température)
- Permet de comparer des performances entre compétitions différentes
- Normalisable sur n'importe quelle distance
- Interprétable directement : "+3%" = l'athlète est 3% plus lent que le vainqueur

### 2.3 Référence inter-catégorie : K1 Hommes

Le K1H est la catégorie de référence car :
- C'est la discipline la plus rapide (vitesse de pointe maximale)
- Elle est présente à toutes les compétitions majeures, toutes distances
- C'est la catégorie avec le plus grand nombre de finalistes dans l'historique

```
% écart K1H = (temps_athlète - temps_vainqueur_K1H_même_compétition_même_distance)
              / temps_vainqueur_K1H × 100
```

### 2.4 Seuils de performance

| Seuil | Définition | Usage |
|-------|-----------|-------|
| Vainqueur médian | Médiane des temps de victoire sur la période | "Niveau pour gagner un ChM" |
| P10 | 10e percentile des temps toutes finales A | "Niveau top mondial historique" |
| Seuil Finale A | Médiane des 8e rangs | "Seuil minimal pour être en finale mondiale" |
| Médiane Finale A | Médiane de tous les finalistes A | "Niveau de milieu de finale" |

---

## 3. Données françaises – traitement spécifique

### Problème du biais de bassin
Les sélections françaises se déroulent sur des bassins nationaux (conditions différentes : vent variable, température de l'eau différente) → **impossible de comparer les temps absolus** directement avec les temps internationaux.

### Solution retenue
Utiliser le **% d'écart au vainqueur** calculé sur les compétitions internationales des athlètes français. Cela nécessite d'avoir les résultats des athlètes français **en compétition internationale**, pas uniquement leurs temps de sélection.

*Note : si seuls les temps de sélection sont disponibles, une correction empirique par bassin peut être envisagée (ratio moyen temps_sélection / temps_international pour les athlètes ayant participé aux deux) — mais ce facteur de correction sera explicitement documenté et son incertitude quantifiée.*

---

## 4. Limites connues et points de vigilance

1. **Programme variable** : les épreuves au programme des ChM ont évolué (ex. C1F 1000m n'était pas systématiquement au programme avant 2010). Les comparaisons historiques longues doivent en tenir compte.

2. **JO vs ChM** : le programme olympique est plus restreint (environ 12 épreuves vs 30+ aux ChM). Les analyses mixant JO et ChM doivent isoler les épreuves communes.

3. **Athlètes neutres (AIN)** : depuis 2022, certains athlètes russes/biélorusses concourent sous bannière neutre. Ils sont conservés dans l'analyse internationale mais exclus de toute analyse nationale.

4. **Petits effectifs** : certaines épreuves (C4F notamment) n'ont parfois que 5-6 finalistes. Les métriques statistiques sont à interpréter avec prudence.

---

## 5. Historique des mises à jour

| Date | Action | Responsable |
|------|--------|------------|
| 2025-04 | Création du projet, Phase 1 (Senior 2012–2025) | — |
