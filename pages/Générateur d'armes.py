import streamlit as st
import random
import pandas as pd

# Noms d’armes par catégorie
ONE_HAND_MELEE = [
    "Épée courte", "Dague", "Fléau d'arme", "Marteau de guerre", "Sabre", "Glaive court", "Couteau", "Fouet", "Gourdin", "Masse d'armes", "Cimeterre", "Rapière", "Poignard"
]
TWO_HAND_MELEE = [
    "Épée longue", "Hache de guerre", "Masse lourde", "Lance", "Baton", "Hallebarde"
]
TWO_HAND_RANGED = [
    "Arc long", "Arbalète", "Lance-pierre", "Arc de chasse", "Javelot", "Harpon", "Fronde"
]

WEAPON_TYPES = {
    "Arme à 1 main (CAC)": {
        "names": ONE_HAND_MELEE,
        "damage_multiplier": 1.0
    },
    "Arme à 2 mains (CAC)": {
        "names": TWO_HAND_MELEE,
        "damage_multiplier": 1.2
    },
    "Arme à 2 mains (Distance)": {
        "names": TWO_HAND_RANGED,
        "damage_multiplier": 0.8
    }
}

# Prix basé sur dégâts
def calculate_price(damage):
    return round(0.28 * (damage ** 2.5))

def generate_weapon(weapon_type, dmg_min, dmg_max):
    base_damage = random.randint(dmg_min, dmg_max)
    multiplier = WEAPON_TYPES[weapon_type]["damage_multiplier"]
    adjusted_damage = round(base_damage * multiplier)
    name = random.choice(WEAPON_TYPES[weapon_type]["names"])
    price = calculate_price(base_damage)
    return {
        "Nom": name,
        "Type": weapon_type,
        "Dégâts": adjusted_damage,
        "Dégâts de base": base_damage,
        "Prix (PO)": price
    }

# Initialisation de session state
if "magasin" not in st.session_state:
    st.session_state.magasin = {}

st.title("🏪 Générateur de Magasin d'Armes")

st.subheader("🎯 Filtres globaux")
col1, col2 = st.columns(2)
with col1:
    dmg_min = st.number_input("Dégâts minimum (référentiel 1 main)", min_value=1, value=4)
with col2:
    dmg_max = st.number_input("Dégâts maximum (référentiel 1 main)", min_value=dmg_min, value=10)

st.markdown("### 🧃 Générer un magasin complet")

with st.form("shop_form"):
    nb_items = st.slider("Nombre d'armes par catégorie", 1, 20, 5)
    submitted_shop = st.form_submit_button("Générer le magasin")

    if submitted_shop:
        magasin = {}
        for weapon_type in WEAPON_TYPES.keys():
            magasin[weapon_type] = [
                generate_weapon(weapon_type, dmg_min, dmg_max) for _ in range(nb_items)
            ]
        st.session_state.magasin = magasin  # Stockage persistant

# Bouton pour réinitialiser le magasin
if st.session_state.magasin:
    if st.button("🗑️ Réinitialiser le magasin"):
        st.session_state.magasin = {}

# Affichage des tableaux
if st.session_state.magasin:
    for weapon_type, items in st.session_state.magasin.items():
        df = pd.DataFrame(items)[["Nom", "Type", "Dégâts", "Prix (PO)"]].sort_values(by="Prix (PO)", ascending=True)
        st.markdown(f"#### 🗃️ {weapon_type}")
        st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("By OpenAI & ChatGPT – Générateur de loot pour Re:Born ⚔️")
