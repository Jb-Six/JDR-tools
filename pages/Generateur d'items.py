import streamlit as st
import random
import math

ITEMS = {
    "Casque": ["Force", "PDV"],
    "Amulette": ["Intelligence", "Force"],
    "Armure": ["Armure", "Agilité"],
    "Bottes": ["Agilité", "PDV"]
}

RARITIES = {
    "Commun": {"points": 5, "price": 10},
    "Rare": {"points": 10, "price": 50},
    "Très rare": {"points": 20, "price": 250},
    "Légendaire": {"points": 40, "price": 1000},
}

POLARITIES = [
    (1.10, -0.10, 2.0),    # 1
    (1.00, 0.00, 1.8),
    (0.90, 0.10, 1.7),
    (0.80, 0.20, 1.6),
    (0.75, 0.25, 1.5),
    (0.70, 0.30, 1.4),
    (0.65, 0.35, 1.3),
    (0.60, 0.40, 1.2),
    (0.55, 0.45, 1.1),
    (0.50, 0.50, 1.0),     # 10
    (0.50, 0.50, 1.0),     # 11
    (0.45, 0.55, 1.1),
    (0.40, 0.60, 1.2),
    (0.35, 0.65, 1.3),
    (0.30, 0.70, 1.4),
    (0.25, 0.75, 1.5),
    (0.20, 0.80, 1.6),
    (0.10, 0.90, 1.7),
    (0.00, 1.00, 1.8),
    (-0.10, 1.10, 2.0),    # 20
]

def calculate_price(base_price, polarity_mult):
    return int(round(base_price * polarity_mult))

def generate_item(item_type, rarity, roll=None):
    points = RARITIES[rarity]["points"]
    base_price = RARITIES[rarity]["price"]
    stat_names = ITEMS[item_type]

    # Choix du jet de dé
    if roll is None:
        roll = random.randint(1, 20)
    r1, r2, price_mult = POLARITIES[roll - 1]
    polar_str = f"{int(r1*100)}% / {int(r2*100)}%"
    if roll in [1, 20]:
        polar_str += " (Stats négatives possibles)"
    stats = {}

    if item_type == "Armure":
        best_A = 0
        best_G = 0
        best_score = float('inf')
        max_A = points // 5
        for A in range(0, max_A + 1):
            G = points - 5*A
            if G < 0:
                continue
            ratio_A = (5*A) / points if points else 0
            ratio_G = G / points if points else 0
            score = abs(ratio_A - r1) + abs(ratio_G - r2)
            if score < best_score:
                best_score = score
                best_A = A
                best_G = G
        stats[stat_names[0]] = best_A
        stats[stat_names[1]] = best_G
    else:
        stat1 = int(round(points * r1))
        stat2 = points - stat1
        if stat1 == 0 and r1 < 0: stat1 = int(points * r1)
        if stat2 == 0 and r2 < 0: stat2 = int(points * r2)
        if stat1 + stat2 != points:
            diff = points - (stat1 + stat2)
            stat2 += diff
        stats[stat_names[0]] = stat1
        stats[stat_names[1]] = stat2
    final_price = calculate_price(base_price, price_mult)
    return {
        "type": item_type,
        "rarity": rarity,
        "roll": roll,
        "polar_str": polar_str,
        "stats": stats,
        "final_price": final_price
    }

# ----------- Streamlit UI -------------
st.title("🎲 Générateur d'Items JDR")

col1, col2 = st.columns(2)
with col1:
    item_type = st.selectbox("Type d'item", list(ITEMS.keys()))
with col2:
    rarity = st.selectbox("Rareté", list(RARITIES.keys()))

use_custom_roll = st.checkbox("Choisir manuellement la valeur du jet de dé ?")
roll_value = None
if use_custom_roll:
    roll_value = st.slider("Valeur du jet de dé (1 à 20)", 1, 20, 10)

with st.form("item_form"):
    submitted = st.form_submit_button("Générer un item !")
    if submitted:
        item = generate_item(item_type, rarity, roll=roll_value)
        st.success(f"**{item['type']}** ({item['rarity']})")
        st.write(f"🎲 **Jet de polarité : {item['roll']}** → {item['polar_str']}")
        st.markdown("**Stats :**")
        for stat, value in item["stats"].items():
            st.write(f"- {stat} : {value}")
        st.write(f"💰 **Prix :** {item['final_price']} PO")

        st.markdown(
            "<div style='margin-top: 1em; color: #666; font-size: 0.9em;'>"
            "⚔️ Appuie à nouveau sur le bouton pour un nouvel item !"
            "</div>",
            unsafe_allow_html=True
        )

    else:
        st.info("Sélectionne un type, une rareté, puis clique sur 'Générer un item !'")

st.markdown("---")
st.caption("By OpenAI & ChatGPT - Adapté à ton JDR ⚔️")
