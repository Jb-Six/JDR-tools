import streamlit as st
import random

# Listes de noms d'armes par catégorie
ONE_HAND_MELEE = [
    "Épée courte", "Hachette", "Dague", "Fléau", "Marteau de poing", "Sabre", "Glaive court"
]
TWO_HAND_MELEE = [
    "Épée longue", "Hache de guerre", "Marteau de guerre", "Masse lourde", "Lance", "Gourdin"
]
TWO_HAND_RANGED = [
    "Arc long", "Arbalète lourde", "Lance-pierre", "Arc de chasse", "Javelot de guerre", "Harpon"
]

RARITIES = {
    "Commun": 0,
    "Rare": 1,
    "Très rare": 2,
    "Légendaire": 3,
}

PRICE_TABLE = {
    "Commun": 10,
    "Rare": 50,
    "Très rare": 250,
    "Légendaire": 1000
}

RARITIES_DISPLAY = list(RARITIES.keys())

# Dégâts par rareté et catégorie
DAMAGE_TABLE = {
    "Arme à 1 main (CAC)":     [5, 10, 20, 40],
    "Arme à 2 mains (CAC)":    [6, 12, 24, 48],
    "Arme à 2 mains (Distance)": [4, 8, 16, 32]
}
NAME_TABLE = {
    "Arme à 1 main (CAC)": ONE_HAND_MELEE,
    "Arme à 2 mains (CAC)": TWO_HAND_MELEE,
    "Arme à 2 mains (Distance)": TWO_HAND_RANGED
}

st.title("⚔️ Générateur d'Armes")

col1, col2 = st.columns(2)
with col1:
    weapon_type = st.selectbox("Type d'arme", list(DAMAGE_TABLE.keys()))
with col2:
    rarity = st.selectbox("Rareté", RARITIES_DISPLAY)

with st.form("arme_form"):
    submitted = st.form_submit_button("Générer une arme !")
    if submitted:
        # Choix du nom aléatoire
        name = random.choice(NAME_TABLE[weapon_type])
        degats = DAMAGE_TABLE[weapon_type][RARITIES[rarity]]
        prix = PRICE_TABLE[rarity]

        st.success(f"**{name}**")
        st.write(f"**Type :** {weapon_type}")
        st.write(f"**Rareté :** {rarity}")
        st.write(f"**Dégâts :** {degats}")
        st.write(f"💰 **Prix :** {prix} PO")

        st.markdown(
            "<div style='margin-top: 1em; color: #666; font-size: 0.9em;'>"
            "🔄 Clique sur le bouton pour générer une nouvelle arme !"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Sélectionne un type et une rareté puis clique sur 'Générer une arme !'")

st.markdown("---")
st.caption("By OpenAI & ChatGPT – Générateur d’armes pour Re:Born ⚔️")