import csv
import sqlite3
import streamlit as st
import os

DB_PATH = "fantasy.db"

def build_database(csv_path):
    conn = sqlite3.connect("fantasy.db")
    cur = conn.cursor()

    # Drop tables
    cur.execute("DROP TABLE IF EXISTS Player_Stats")
    cur.execute("DROP TABLE IF EXISTS Players")

    # Create Players table
    cur.execute("""
    CREATE TABLE Players (
        Player_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Team TEXT,
        Position TEXT,
        Age INTEGER
    );
    """)

    # Create Player Stats table
    cur.execute("""
    CREATE TABLE Player_Stats (
        Stat_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Player_ID INTEGER,
        MP FLOAT,
        FG FLOAT,
        FGA FLOAT,
        FT FLOAT,
        FTA FLOAT,
        ThreeP FLOAT,
        TRB FLOAT,
        AST FLOAT,
        STL FLOAT,
        BLK FLOAT,
        TOV FLOAT,
        PTS FLOAT,
        FOREIGN KEY (Player_ID) REFERENCES Players(Player_ID)
    );
    """)

    # Load CSV
    with open(csv_path, "r") as f:
        r = csv.DictReader(f)

        for row in r:

            # Insert into Players
            cur.execute("""
                INSERT INTO Players (Name, Team, Position, Age)
                VALUES (?, ?, ?, ?)
            """, (
                row["Player"],
                row["Team"],
                row["Pos"],
                row["Age"]
            ))

            player_id = cur.lastrowid

            # Insert into Player_Stats
            cur.execute("""
                INSERT INTO Player_Stats (Player_ID, MP, FG, FGA, FT, FTA, ThreeP, TRB, AST, STL, BLK, TOV, PTS)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id,
                row["MP"],
                row["FG"],
                row["FGA"],
                row["FT"],
                row["FTA"],
                row["3P"],
                row["TRB"],
                row["AST"],
                row["STL"],
                row["BLK"],
                row["TOV"],
                row["PTS"]
            ))

    conn.commit()
    conn.close()
    print("Database built successfully!")



csv_path = "/Users/aryansehgal/Desktop/nbastats.csv"
build_database(csv_path)


SCORING = {
    "PTS": 1,
    "REB": 1,
    "AST": 2,
    "STL": 4,
    "BLK": 4,
    "TO": -2,
    "FG": 2,
    "FGA": -1,
    "FTM": 1,
    "FTA": -1,
    "3P": 1
}

def load_csv(path):
    rows = []
    with open(path, "r") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows

def fantasy_points(row):
    total = 0
    for stat, mult in SCORING.items():
        if stat in row and row[stat] != "":
            total += float(row[stat]) * mult
    return total

def compute_rankings(players):
    ranked = []
    for p in players:
        fp = fantasy_points(p)
        ranked.append({
            "Player": p["Player"],
            "Pos": p["Pos"],
            "FP": fp
        })

    ranked.sort(key=lambda x: x["FP"], reverse=True)

    for i, p in enumerate(ranked):
        p["overall_rank"] = i + 1

    pos_groups = {}
    for p in ranked:
        pos = p["Pos"]
        if pos not in pos_groups:
            pos_groups[pos] = []
        pos_groups[pos].append(p)

    for pos in pos_groups:
        gp = pos_groups[pos]
        gp.sort(key=lambda x: x["FP"], reverse=True)
        for i, p in enumerate(gp):
            p["pos_rank"] = i + 1

    return ranked

def search_players(ranked, name):
    name = name.lower()
    return [p for p in ranked if name in p["Player"].lower()]


# ---------------- STREAMLIT APP ----------------

st.title("🏀 ESPN Fantasy Basketball Calculator")
st.write("Search players, compute fantasy points, rankings, and compare players.")

csv_path = "/Users/aryansehgal/Desktop/nbastats.csv"
players = load_csv(csv_path)
ranked = compute_rankings(players)

tabs = st.tabs(["🔍 Search Player", "⚔️ Player Comparison"])

# ---------------- SEARCH TAB ----------------
with tabs[0]:
    query = st.text_input("Search player by name:")
    if query:
        matches = search_players(ranked, query)

        if len(matches) == 0:
            st.error("No players found.")
        else:
            table = []
            for p in matches:
                table.append({
                    "Player": p["Player"],
                    "Position": p["Pos"],
                    "Fantasy Points": round(p["FP"], 2),
                    "Overall Rank": p["overall_rank"],
                    "Position Rank": p["pos_rank"]
                })

            st.table(table)

# ---------------- COMPARISON TAB ----------------
with tabs[1]:
    all_names = [p["Player"] for p in ranked]

    col1, col2 = st.columns(2)

    with col1:
        p1_name = st.selectbox("Select Player 1:", all_names)

    with col2:
        p2_name = st.selectbox("Select Player 2:", all_names)

    if p1_name and p2_name:
        p1 = next(p for p in ranked if p["Player"] == p1_name)
        p2 = next(p for p in ranked if p["Player"] == p2_name)

        st.subheader("📊 Player Comparison")

        comp_table = [
            {
                "Metric": "Player Name",
                "Player 1": p1["Player"],
                "Player 2": p2["Player"]
            },
            {
                "Metric": "Position",
                "Player 1": p1["Pos"],
                "Player 2": p2["Pos"]
            },
            {
                "Metric": "Fantasy Points",
                "Player 1": round(p1["FP"], 2),
                "Player 2": round(p2["FP"], 2)
            },
            {
                "Metric": "Overall Rank",
                "Player 1": p1["overall_rank"],
                "Player 2": p2["overall_rank"]
            },
            {
                "Metric": "Position Rank",
                "Player 1": p1["pos_rank"],
                "Player 2": p2["pos_rank"]
            }
        ]

        st.table(comp_table)

        # Winner Highlight
        if p1["FP"] > p2["FP"]:
            st.success(f"🏆 **{p1['Player']}** is the better fantasy option.")
        elif p2["FP"] > p1["FP"]:
            st.success(f"🏆 **{p2['Player']}** is the better fantasy option.")
        else:
            st.info("🤝 Both players have the same fantasy value!")
