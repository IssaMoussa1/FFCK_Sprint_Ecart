#!/usr/bin/env python3
"""
Scraper Canoë-Kayak Sprint – canoeresults.eu
Collecte les Finales A des Championnats du Monde Senior et JO (2012–2025)
Produit : icf_sprint_finals_A.csv

Usage : python scraper_canoe_sprint.py
Dépendances : pip install requests beautifulsoup4
"""

import re
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import date

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

EVENTS = [
    # (event_id, year, competition_type, location)
    # Championnats du Monde Senior
    ("7161", 2025, "WCh", "Milan, ITA"),
    ("7160", 2024, "WCh", "Samarkand, UZB"),
    ("7159", 2023, "WCh", "Duisburg, GER"),
    ("7158", 2022, "WCh", "Halifax, CAN"),
    ("7157", 2021, "WCh", "Copenhagen, DEN"),
    ("7156", 2019, "WCh", "Szeged, HUN"),
    ("7155", 2018, "WCh", "Montemor, POR"),
    ("7154", 2017, "WCh", "Racice, CZE"),
    ("7153", 2015, "WCh", "Milan, ITA"),
    ("7152", 2014, "WCh", "Moscow, RUS"),
    ("7151", 2013, "WCh", "Duisburg, GER"),
    # Jeux Olympiques
    ("6343", 2024, "OG",  "Paris, FRA"),
    ("4537", 2020, "OG",  "Tokyo, JPN"),
    ("2502", 2016, "OG",  "Rio de Janeiro, BRA"),
    ("42",   2012, "OG",  "London, GBR"),
]

BASE_URL = "http://www.canoeresults.eu/view-results/sprint"
OUTPUT_FILE = f"data/raw/icf_sprint_finals_A_{date.today()}.csv"

# ─── PARSING ──────────────────────────────────────────────────────────────────

# Regex pour parser le label d'épreuve (ex. "K1 men 500 m")
EVENT_PATTERN = re.compile(
    r'^(K|C)(\d)\s+(men|women|mix)\s+([\d,\.]+)\s*m',
    re.IGNORECASE
)

def parse_time_to_seconds(t: str) -> float | None:
    """Convertit un temps textuel en secondes flottantes.
    Formats gérés : '00:35.243', '1:36.262', '35.243', '34.29'
    """
    t = t.strip()
    if not t or t in ("-", "DSQ", "DNF", "DNS", "Lapped", ""):
        return None
    # Supprimer les préfixes 00: éventuels
    t = re.sub(r'^0+:', '', t)
    parts = t.split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        else:
            return float(parts[0])
    except ValueError:
        return None

def parse_event_label(label: str):
    """Retourne (boat_class, gender, distance_m) depuis le label d'épreuve."""
    label = label.strip()
    m = EVENT_PATTERN.match(label)
    if not m:
        return None, None, None
    boat_type  = m.group(1).upper()          # K ou C
    crew_size  = m.group(2)                  # 1, 2, 4
    gender_raw = m.group(3).lower()          # men / women / mix
    dist_raw   = m.group(4).replace(',', '') # 200, 500, 1000, 5000
    boat_class = f"{boat_type}{crew_size}"   # K1, K2, C1, etc.
    gender     = {"men": "H", "women": "F", "mix": "MIX"}.get(gender_raw, gender_raw)
    try:
        # Supprimer les séparateurs de milliers (point ET virgule)
        # ex: "1.000" ou "1,000" → "1000", "5.000" → "5000"
        dist_clean = re.sub(r'[.,]', '', dist_raw)
        distance = int(dist_clean)
    except ValueError:
        distance = None
    return boat_class, gender, distance

def scrape_event(event_id: str, year: int, comp_type: str, location: str) -> list[dict]:
    """Scrape une page canoeresults.eu et retourne les lignes de résultats."""
    url = f"{BASE_URL}?eventid[]={event_id}#event"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  ⚠ Erreur fetch {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    rows_out = []

    # Chaque épreuve est un <table> ; son header de colonne 1 contient le label
    tables = soup.find_all('table')
    for table in tables:
        # Le 1er <td> de la 1ère ligne header contient le nom de l'épreuve
        header_row = table.find('tr')
        if not header_row:
            continue
        header_cells = header_row.find_all('td')
        if not header_cells:
            continue
        event_label = header_cells[0].get_text(strip=True)

        boat_class, gender, distance = parse_event_label(event_label)
        if boat_class is None:
            continue  # pas une épreuve de sprint

        # Filtrer les épreuves 5000m si souhaité (optionnel : garder ou non)
        # Lignes de résultats (skip header)
        data_rows = table.find_all('tr')[1:]
        current_rank = None

        for tr in data_rows:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if len(cells) < 4:
                continue

            # col0 = rang (peut être vide pour membres d'équipage supplémentaires)
            # col1 = nom athlète, col2 = pays, col3 = temps
            rank_cell, name_cell, country_cell, time_cell = cells[0], cells[1], cells[2], cells[3]

            # Mise à jour du rang courant
            if rank_cell.isdigit():
                current_rank = int(rank_cell)
            elif current_rank is None:
                continue  # Ligne sans rang valide, ignorer

            # Ignorer les temps non valides (DSQ, DNF, DNS, etc.)
            time_s = parse_time_to_seconds(time_cell)
            if time_s is None:
                continue

            rows_out.append({
                "year":         year,
                "competition":  comp_type,
                "location":     location,
                "event_label":  event_label,
                "boat_class":   boat_class,
                "gender":       gender,
                "distance_m":   distance,
                "rank":         current_rank,
                "athlete":      name_cell,
                "country":      country_cell,
                "time_raw":     time_cell,
                "time_seconds": round(time_s, 3),
            })

    return rows_out

# ─── CALCUL DES MÉTRIQUES ─────────────────────────────────────────────────────

def enrich_with_metrics(all_rows: list[dict]) -> list[dict]:
    """
    Pour chaque ligne, calcule :
    - pct_gap_winner  : % d'écart au vainqueur (rang 1 de la même épreuve)
    - pct_gap_K1H_ref : % d'écart par rapport au temps du vainqueur K1H
                        de la même année/compétition/distance (référence absolue)
    """
    # Indexer les temps gagnants par (year, comp, boat_class, gender, distance)
    winner_times = {}
    for r in all_rows:
        if r["rank"] == 1:
            key = (r["year"], r["competition"], r["boat_class"], r["gender"], r["distance_m"])
            winner_times[key] = r["time_seconds"]

    # Indexer les temps K1H gagnants par (year, comp, distance)
    k1h_winner = {}
    for r in all_rows:
        if r["rank"] == 1 and r["boat_class"] == "K1" and r["gender"] == "H":
            key = (r["year"], r["competition"], r["distance_m"])
            k1h_winner[key] = r["time_seconds"]

    enriched = []
    for r in all_rows:
        r = r.copy()
        key_event = (r["year"], r["competition"], r["boat_class"], r["gender"], r["distance_m"])
        key_k1h   = (r["year"], r["competition"], r["distance_m"])

        w = winner_times.get(key_event)
        r["pct_gap_winner"] = (
            round((r["time_seconds"] - w) / w * 100, 3) if w and w > 0 else None
        )

        k1h_w = k1h_winner.get(key_k1h)
        r["pct_gap_K1H_ref"] = (
            round((r["time_seconds"] - k1h_w) / k1h_w * 100, 3)
            if k1h_w and k1h_w > 0 else None
        )

        enriched.append(r)

    return enriched

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    all_rows = []

    for event_id, year, comp_type, location in EVENTS:
        print(f"→ {year} {comp_type} {location} (id={event_id})…")
        rows = scrape_event(event_id, year, comp_type, location)
        print(f"   {len(rows)} lignes collectées")
        all_rows.extend(rows)
        time.sleep(0.8)  # politesse envers le serveur

    print(f"\nTotal brut : {len(all_rows)} lignes")

    # Filtrer uniquement Finale A = rangs 1 à 9
    finals_a = [r for r in all_rows if r["rank"] <= 9]
    print(f"Après filtre Finale A (rangs 1-9) : {len(finals_a)} lignes")

    # Calculer les métriques
    finals_a = enrich_with_metrics(finals_a)

    # Écriture CSV
    fieldnames = [
        "year", "competition", "location",
        "event_label", "boat_class", "gender", "distance_m",
        "rank", "athlete", "country",
        "time_raw", "time_seconds",
        "pct_gap_winner", "pct_gap_K1H_ref",
    ]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(finals_a)

    print(f"\n✅ Fichier généré : {OUTPUT_FILE}")
    print(f"   {len(finals_a)} lignes | {len(set((r['year'],r['competition']) for r in finals_a))} événements")

if __name__ == "__main__":
    main()
