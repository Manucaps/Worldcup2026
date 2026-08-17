import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # pour générer les images sans écran

# ── 1. LES DONNÉES DU MONDIAL 2026 ──────────────────────
# Source : stats officielles FIFA 2026
data = {
    "joueur": [
        "Kylian Mbappé", "Vinícius Jr", "Ousmane Dembélé",
        "Ismaïla Sarr", "Jonathan David", "Lamine Yamal",
        "Rodri", "Michael Olise", "Erling Haaland", "Bukayo Saka"
    ],
    "pays": [
        "France", "Brésil", "France",
        "Sénégal", "Canada", "Espagne",
        "Espagne", "France", "Norvège", "Angleterre"
    ],
    "buts": [10, 4, 4, 4, 3, 3, 2, 7, 2, 3],
    "passes_decisives": [4, 1, 2, 1, 0, 5, 3, 3, 1, 2],
    "matchs": [8, 7, 7, 5, 4, 8, 8, 7, 5, 7]
}

df = pd.DataFrame(data)

# ── 2. CALCULS ───────────────────────────────────────────
df["contributions"] = df["buts"] + df["passes_decisives"]
df["buts_par_match"] = (df["buts"] / df["matchs"]).round(2)
df = df.sort_values("contributions", ascending=False)

# ── 3. AFFICHER LE CLASSEMENT ────────────────────────────
print("\n🏆 TOP BUTEURS & PASSEURS — COUPE DU MONDE 2026")
print("=" * 58)
print(f"{'Joueur':<20} {'Pays':<12} {'Buts':>5} {'PD':>4} {'Total':>6}")
print("-" * 58)
for _, row in df.iterrows():
    print(f"{row['joueur']:<20} {row['pays']:<12} {row['buts']:>5} "
          f"{row['passes_decisives']:>4} {row['contributions']:>6}")

# ── 4. GRAPHIQUE — TOP CONTRIBUTEURS ────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Coupe du Monde 2026 — Statistiques clés", 
             fontsize=14, fontweight='bold')

# Graphique 1 : Buts + Passes décisives (barres empilées)
top5 = df.head(5)
axes[0].bar(top5["joueur"], top5["buts"], 
            label="Buts", color="#1B2A4A")
axes[0].bar(top5["joueur"], top5["passes_decisives"],
            bottom=top5["buts"], label="Passes décisives", color="#0A7C6E")
axes[0].set_title("Top 5 — Contributions offensives")
axes[0].set_ylabel("Nombre")
axes[0].legend()
axes[0].tick_params(axis='x', rotation=30)

# Graphique 2 : Buts par match (efficacité)
top_eff = df.nlargest(5, "buts_par_match")
axes[1].barh(top_eff["joueur"], top_eff["buts_par_match"], 
             color="#B7490A")
axes[1].set_title("Top 5 — Efficacité (buts/match)")
axes[1].set_xlabel("Buts par match")

plt.tight_layout()
plt.savefig("worldcup2026_stats.png", dpi=150, bbox_inches='tight')
print("\n✅ Graphique généré : worldcup2026_stats.png")

# ── 5. STATS PAR PAYS ────────────────────────────────────
print("\n🌍 STATS PAR PAYS")
print("=" * 40)
par_pays = df.groupby("pays").agg(
    buts_total=("buts", "sum"),
    joueurs=("joueur", "count")
).sort_values("buts_total", ascending=False)
print(par_pays.to_string())

# ── 6. ANECDOTE SUR MBAPPÉ ───────────────────────────────
mbappe = df[df["joueur"] == "Kylian Mbappé"].iloc[0]
print(f"\n⚡ RECORD : Mbappé — {mbappe['buts']} buts en "
      f"{mbappe['matchs']} matchs ({mbappe['buts_par_match']} buts/match)")
print("   Il est désormais le meilleur buteur de l'histoire")
print("   des Coupes du Monde avec 22 buts en 3 éditions.")
print("\n🏆 Vainqueur : ESPAGNE 🇪🇸")
import requests

def commenter_avec_ia(stats_texte):
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": "TON_CLE_API", 
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 300,
            "messages": [{
                "role": "user",
                "content": f"En 3 phrases, commente ces stats de la Coupe du Monde 2026 comme un journaliste sportif : {stats_texte}"
            }]
        }
    )
    return response.json()["content"][0]["text"]

stats_resume = f"Mbappé : 10 buts en 8 matchs. Espagne vainqueur. 307 buts au total en 104 matchs."
print("\n🤖 ANALYSE IA :")
print(commenter_avec_ia(stats_resume))