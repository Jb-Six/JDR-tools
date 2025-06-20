import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="Re:Born Toolkit", page_icon="🧙‍♂️")
FAV_FILE = "favoris.json"
CONVERTED_FILE = "monstres_convertis.json"

def load_favoris():
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_favoris(favoris):
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump(favoris, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_monsters():
    with open(CONVERTED_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_monsters(monstres):
    with open(CONVERTED_FILE, "w", encoding="utf-8") as f:
        json.dump(monstres, f, ensure_ascii=False, indent=2)

@st.cache_data
def get_monsters():
    return load_monsters()

# Utilise session_state pour l’édition (pas de cache_data)
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "edit_monstre" not in st.session_state:
    st.session_state["edit_monstre"] = {}

monstres = load_monsters()
def challenge_to_float(challenge):
    value = str(challenge).split(" ")[0]
    try:
        if "/" in value:
            num, denom = value.split("/")
            return float(num) / float(denom)
        return float(value)
    except Exception:
        return 0

challenges_floats = [challenge_to_float(m['Difficulté']) for m in monstres]
min_challenge, max_challenge = min(challenges_floats), max(challenges_floats)

st.sidebar.title("Recherche de Monstre")
min_selected, max_selected = st.sidebar.slider(
    "Filtrer par plage de difficulté (Challenge)",
    min_value=min_challenge,
    max_value=max_challenge,
    value=(min_challenge, max_challenge),
    step=0.5,
    format="%.3g"
)

monstres_filtrés = [
    m for m in monstres
    if min_selected <= challenge_to_float(m['Difficulté']) <= max_selected
]
noms_monstres_filtrés = [m['name'] for m in monstres_filtrés]

if noms_monstres_filtrés:
    monstre_nom = st.sidebar.selectbox("Choisis un monstre :", sorted(noms_monstres_filtrés))
else:
    monstre_nom = None
    st.sidebar.info("Aucun monstre ne correspond à ce filtre.")

if "favoris" not in st.session_state:
    st.session_state["favoris"] = load_favoris()

def add_favori(nom):
    if nom not in st.session_state["favoris"]:
        st.session_state["favoris"].append(nom)
        save_favoris(st.session_state["favoris"])

def remove_favori(nom):
    if nom in st.session_state["favoris"]:
        st.session_state["favoris"].remove(nom)
        save_favoris(st.session_state["favoris"])

with st.sidebar:
    st.markdown("### ⭐ Favoris")
    fav_options = ["Aucun"] + sorted(st.session_state["favoris"])
    selected_fav = st.selectbox("Voir un favori :", fav_options, key="favori_selectbox")
    if selected_fav != "Aucun":
        monstre_nom = selected_fav
    if selected_fav != "Aucun":
        if st.button("❌ Retirer ce favori"):
            remove_favori(selected_fav)
            st.rerun()

monstre = next((m for m in monstres_filtrés if m['name'] == monstre_nom), None)

def reset_edit_mode():
    st.session_state["edit_mode"] = False
    st.session_state["edit_monstre"] = {}

if monstre:
    if not st.session_state["edit_mode"]:
        # --- FICHE STANDARD ---
        col1, col2 = st.columns([2, 1])  # Gauche : infos, Droite : image

        with col2:
            st.markdown(
                f"""
                <div style="max-height:500px; overflow:hidden; display:flex; justify-content:center;">
                    <img src="{monstre['img_url']}" alt="{monstre['name']}" style="height:500px; object-fit:contain;" />
                </div>
                <p style="text-align:center;">{monstre['name']}</p>
                """,
                unsafe_allow_html=True
            )

        with col1:
            st.title(monstre['name'])
            st.markdown(f"<span style='color:#777;font-size:1.1em'>{monstre['meta']}</span>", unsafe_allow_html=True)
            st.markdown(f"<b>Difficulté :</b> {monstre['Difficulté']}", unsafe_allow_html=True)
            # Boutons favoris & édition
            cols = st.columns([2, 2])
            with cols[0]:
                if monstre['name'] in st.session_state["favoris"]:
                    if st.button("⭐ Retirer des favorise"):
                        remove_favori(monstre['name'])
                        st.rerun()
                else:
                    if st.button("☆ Ajouter aux favoris"):
                        add_favori(monstre['name'])
                        st.rerun()
            with cols[1]:
                if st.button("✏️ Mode édition"):
                    st.session_state["edit_mode"] = True
                    # Deepcopy pour ne pas modifier en live
                    import copy
                    st.session_state["edit_monstre"] = copy.deepcopy(monstre)
                    st.rerun()

            # Bloc de stats principales
            pv = monstre.get("PV", 0)
            armure = monstre.get("Armure", 0)
            vitesse = monstre.get("Vitesse", "?")

            stats_disp = ""
            for stat_fr in ["Force", "Agilité", "Intelligence", "Chance"]:
                stat = monstre["stats"].get(stat_fr, {"valeur": 0, "bonus": 0})
                val, bonus = stat["valeur"], stat["bonus"]
                bonus_str = f"+{bonus}" if bonus >= 0 else f"{bonus}"
                stats_disp += (
                    f"<div style='flex:1;min-width:85px;margin-bottom:4px;'>"
                    f"<span style='font-weight:700;color:#444;font-size:1.20em;'>{stat_fr}</span> "
                    f"<br><span style='font-weight:600;margin-left:0px;font-size:1.0em'>{val}</span> "
                    f"<span style='color:#4787b2;font-size:1.0em;margin-left:2px;'>({bonus_str})</span>"
                    f"</div>"
                )

            st.markdown(
                f"""
            <div style='margin:20px 0 20px 0;background:linear-gradient(90deg,#f8fafb 85%,#e8ecf1 100%);border-radius:18px;border:1.5px solid #e0e4ea;box-shadow:0 2px 8px #b6c5d933;padding:24px 28px 18px 28px;max-width:700px;'>
                <div style='font-size:1.20em;font-weight:700;margin-bottom:12px;display:flex'>
                    <div style='flex:1;'>
                        <span style='color:#222;'>PV</span>
                        <br><span style='font-weight:600;font-size:1.0em'>{pv}</span>
                    </div>
                    <div style='flex:1;'>
                        <span style='color:#222;'>Armure</span>
                        <br><span style='font-weight:600;font-size:1.0em'>{armure}</span>
                    </div>
                    <div style='flex:1;'>
                        <span style='color:#222;'>Vitesse</span>
                        <br><span style='font-weight:600;font-size:1.0em'>{vitesse}</span>
                    </div>
                </div>
                <div style='display:flex;gap:16px;justify-content:space-between;margin-bottom:6px;flex-wrap:wrap;border-bottom:1px solid #e0e4ea;padding-bottom:7px;'>
                    {stats_disp}
                </div>
                <div style='margin-top:12px;display:flex;flex-wrap:wrap;gap:18px;font-size:1.04em;color:#666;'>
                    <div>
                        <span style='font-weight:600;color:#4b677d;'>Sens</span>
                        <span style='background:#eef3fa;color:#466ab6;padding:2px 10px 2px 8px;border-radius:8px;margin-left:4px;font-size:0.99em;'>{monstre.get('Sens', '')}</span>
                    </div>
                    <div>
                        <span style='font-weight:600;color:#4b677d;'>Langues</span>
                        <span style='background:#eef3fa;color:#466ab6;padding:2px 10px 2px 8px;border-radius:8px;margin-left:4px;font-size:0.99em;'>{monstre.get('Langues', '')}</span>
                    </div>
                </div>
            </div>
                """,
                unsafe_allow_html=True
            )

            # Immunités, résistances
            if monstre.get("Immunités dégâts"):
                st.markdown(f"<b>Immunités aux dégâts :</b> {monstre['Immunités dégâts']}", unsafe_allow_html=True)
            if monstre.get("Immunités conditions"):
                st.markdown(f"<b>Immunités aux conditions :</b> {monstre['Immunités conditions']}", unsafe_allow_html=True)
            if monstre.get("Résistances"):
                st.markdown(f"<b>Résistances :</b> {monstre['Résistances']}", unsafe_allow_html=True)

        # ---- CAPACITÉS / ACTIONS ----
        if monstre.get("Traits"):
            st.markdown("### Capacités", unsafe_allow_html=True)
            st.markdown(monstre["Traits"], unsafe_allow_html=True)
        if monstre.get("Actions"):
            st.markdown("### Actions", unsafe_allow_html=True)
            st.markdown(monstre["Actions"], unsafe_allow_html=True)
        if monstre.get("Actions légendaires"):
            st.markdown("### Actions légendaires", unsafe_allow_html=True)
            st.markdown(monstre["Actions légendaires"], unsafe_allow_html=True)

    else:
        # --- MODE ÉDITION ---
        edit_monstre = st.session_state["edit_monstre"]
        st.title("Mode édition : " + edit_monstre.get("name", ""))
        st.info("Modifie les champs et clique sur 'Enregistrer' pour appliquer les changements.")

        with st.form("form_edit_monstre"):
            colA, colB = st.columns([2, 1])
            with colA:
                name = st.text_input("Nom", value=edit_monstre.get("name", ""))
                meta = st.text_input("Meta (type, alignement...)", value=edit_monstre.get("meta", ""))
                difficulte = st.text_input("Difficulté", value=edit_monstre.get("Difficulté", ""))
                pv = st.number_input("PV", value=edit_monstre.get("PV", 0), min_value=0)
                armure = st.number_input("Armure", value=edit_monstre.get("Armure", 0), min_value=0)
                vitesse = st.text_input("Vitesse", value=edit_monstre.get("Vitesse", ""))

                stats = edit_monstre.get("stats", {})
                st.markdown("#### Statistiques principales")
                force_val = st.number_input("Force", value=stats.get("Force", {}).get("valeur", 0))
                force_bonus = st.number_input("Bonus Force", value=stats.get("Force", {}).get("bonus", 0))
                agilite_val = st.number_input("Agilité", value=stats.get("Agilité", {}).get("valeur", 0))
                agilite_bonus = st.number_input("Bonus Agilité", value=stats.get("Agilité", {}).get("bonus", 0))
                intelligence_val = st.number_input("Intelligence", value=stats.get("Intelligence", {}).get("valeur", 0))
                intelligence_bonus = st.number_input("Bonus Intelligence", value=stats.get("Intelligence", {}).get("bonus", 0))
                chance_val = st.number_input("Chance", value=stats.get("Chance", {}).get("valeur", 0))
                chance_bonus = st.number_input("Bonus Chance", value=stats.get("Chance", {}).get("bonus", 0))

                st.markdown("#### Défenses & Attributs")
                immunites_degats = st.text_area("Immunités dégâts", value=edit_monstre.get("Immunités dégâts", ""))
                immunites_conditions = st.text_area("Immunités conditions", value=edit_monstre.get("Immunités conditions", ""))
                resistances = st.text_area("Résistances", value=edit_monstre.get("Résistances", ""))
                sens = st.text_input("Sens", value=edit_monstre.get("Sens", ""))
                langues = st.text_input("Langues", value=edit_monstre.get("Langues", ""))

                st.markdown("#### Capacités & Actions")
                traits = st.text_area("Capacités (Traits)", value=edit_monstre.get("Traits", ""))
                actions = st.text_area("Actions", value=edit_monstre.get("Actions", ""))
                actions_legendaires = st.text_area("Actions légendaires", value=edit_monstre.get("Actions légendaires", ""))

            with colB:
                img_url = st.text_input("URL de l'image", value=edit_monstre.get("img_url", ""))
                st.image(img_url, use_container_width=True)

            # --- Validation ---
            col_save, col_cancel = st.columns(2)
            submitted = col_save.form_submit_button("💾 Enregistrer les modifications")
            canceled = col_cancel.form_submit_button("❌ Annuler")

        if canceled:
            reset_edit_mode()
            st.rerun()

        if submitted:
            # Mets à jour le dict avec les nouvelles valeurs
            edit_monstre["name"] = name
            edit_monstre["meta"] = meta
            edit_monstre["Difficulté"] = difficulte
            edit_monstre["PV"] = pv
            edit_monstre["Armure"] = armure
            edit_monstre["Vitesse"] = vitesse
            edit_monstre["stats"] = {
                "Force": {"valeur": force_val, "bonus": force_bonus},
                "Agilité": {"valeur": agilite_val, "bonus": agilite_bonus},
                "Intelligence": {"valeur": intelligence_val, "bonus": intelligence_bonus},
                "Chance": {"valeur": chance_val, "bonus": chance_bonus},
            }
            edit_monstre["Immunités dégâts"] = immunites_degats
            edit_monstre["Immunités conditions"] = immunites_conditions
            edit_monstre["Résistances"] = resistances
            edit_monstre["Sens"] = sens
            edit_monstre["Langues"] = langues
            edit_monstre["Traits"] = traits
            edit_monstre["Actions"] = actions
            edit_monstre["Actions légendaires"] = actions_legendaires
            edit_monstre["img_url"] = img_url

            # Remplace dans la liste principale (par nom)
            for i, m in enumerate(monstres):
                if m["name"] == monstre["name"]:
                    monstres[i] = edit_monstre
                    break
            save_monsters(monstres)

            st.success("Modifications enregistrées !")
            reset_edit_mode()
            st.rerun()

else:
    st.warning("Monstre non trouvé.")
