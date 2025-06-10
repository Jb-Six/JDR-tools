import streamlit as st
from openai import OpenAI
import os
cle_api = os.getenv("OPENAI_API_KEY")

# --- PARAMÉTRAGE DES LIEUX DISPONIBLES ---
LORE_PAR_LIEU = {
    "Verdelune": """
🌿 Le Village
Verdelune est un village paisible entouré de nature, blotti entre des collines boisées et des champs en friche.
La vie y est simple et rythmée par les saisons. Les villageois se connaissent tous, et les étrangers sont vite repérés.
Le maire fait de son mieux pour maintenir l'ordre, même si les choses semblent plus agitées qu’autrefois.
Personne ne quitte jamais le village. Ce n’est pas interdit, mais pourquoi le ferait-on ? Tout ce qu’il faut est ici.

🛒 Le Marché
Le marchand généraliste vend un peu de tout, mais ses prix sont élevés.
Le forgeron est connu pour ses armes solides et ses silences prolongés.
Le marchand magique est un peu étrange, toujours en train de murmurer à ses grimoires.
L’apothicaire est grincheux mais efficace, ses potions “font ce qu’elles doivent faire, ni plus, ni moins”.
Le maître des familiers expose des œufs étranges en vitrine et parle aux bêtes comme à des enfants.
Le colporteur de rumeurs aime jaser, souvent contre quelques pièces.
Les artisans du marché respectent une routine stricte, et ferment tous dès que le soleil décline.

🍻 La Taverne
Le tavernier accueille les voyageurs sans poser trop de questions, mais garde l’œil ouvert.
Il se plaint souvent de bruits dans sa cave, surtout la nuit. Des pas, des grattements… mais aucun client ne veut y descendre.
Les habitués aiment discuter autour d’un verre. Les bras de fer et les paris sont monnaie courante.

🌲 Les Abords de la Forêt
Au nord du village commence une forêt dense, sombre et silencieuse, que les villageois évitent.
On dit que ceux qui s’y aventurent ne reviennent pas toujours.
Des créatures étranges y rôdent — certaines fuient le regard, d’autres s’en nourrissent.
Le chant des oiseaux y est parfois remplacé par des échos qu’on ne reconnaît pas.

📚 Histoire et Mémoire
Verdelune fut autrefois un lieu de passage pour les voyageurs et les marchands itinérants, mais ces temps-là semblent révolus.
Certains anciens parlent de vieilles pierres au fond de la forêt, recouvertes de mousse et de symboles oubliés.
Le cimetière du village est ancien, et certains noms sur les pierres tombales sont effacés par le temps.
Les villageois respectent les traditions, même s’ils ont oublié leur origine.
"""
}

# --- FONCTIONS ---
def make_prompt(description, place, quete):
    context = LORE_PAR_LIEU.get(place, "")
    return f"""Tu es un générateur de fiches de personnages non-joueurs (PNJ) pour un jeu de rôle heroic-fantasy.
À partir de quelques informations, tu dois créer un PNJ crédible, original et utilisable directement dans une partie de jeu de rôle.
Le personnage doit s’intégrer naturellement dans un univers de fantasy médiévale (type heroic-fantasy), avec des éléments de contexte qui le rendent vivant et intéressant à interpréter.

La fiche personnage doit inclure les éléments suivants :

1. Nom : un nom cohérent avec le genre fantasy, optionnellement un surnom lié à sa réputation, ses traits ou son histoire.
2. Fonction / Métier : le rôle qu’il occupe dans la société ou son activité principale.
3. Caractère / Tempérament / Patience : un résumé de sa psychologie, de son comportement social, de son seuil de tolérance ou de son impulsivité.
4. Apparence : description de son allure générale, ses traits distinctifs, sa tenue vestimentaire.
5. Voix : timbre, accent, manière de s’exprimer, tics de langage éventuels.
6. Négociation / Quête : (optionnel)
   - Son ouverture à la discussion ou à la négociation/corruption.
   - Ce qu’il recherche ou désire en ce moment.
   - Une quête ou un service qu’il pourrait confier aux joueurs.
   - Ce qu’il offre en échange : objets, informations, faveurs, argent, etc.

Sois clair, immersif et inspire-toi du style des maîtres de jeu. Chaque fiche doit pouvoir être lue ou jouée telle quelle, sans modification nécessaire.

Contexte : {context}
Lieu d’ancrage du PNJ : {place}
Description du PNJ : {description}
Quete ou service à confier : {'Oui' if quete else 'Non'}
"""

def make_suffix():
    return """Informations supplémentaires :
Commence la conversation par un silence ("...") pour laisser les joueurs parler en premier.
"""

def make_prefix():
    return f"""Tu incarnes le PNJ décrit dans la fiche ci-dessous.
Tu vas dialoguer avec un joueur dans le cadre d’un jeu de rôle heroic-fantasy.
Reste strictement dans ton rôle, comme si tu étais ce personnage réel.

Consignes de style :
Ne commence jamais ton texte par le nom du personnage.
Évite les didascalies (actions entre parenthèses ou hors rôle).
Privilégie des répliques naturelles, interactives, jamais de longs monologues.
Parle comme le ferait ce personnage, en fonction de sa personnalité, de sa voix, et de ses intentions.

L’objectif est de maintenir une immersion totale pour le joueur.
"""

# --- INTERFACE STREAMLIT ---
st.title("🧑‍🌾 Générateur de fiches PNJ")

with st.form("pnj_form"):
    desc = st.text_area("Décris brièvement ton PNJ (rôle, personnalité, détail, etc.)", max_chars=350, height=100)
    lieu = st.selectbox("Lieu de vie du PNJ", LORE_PAR_LIEU.keys())
    # Optionnel : ajouter un bouton checkbox pour inclure une quête ou non
    quete = st.checkbox("Inclure une quête ou un service à confier aux joueurs ?")
    submit = st.form_submit_button("Générer la fiche PNJ !")

if submit and desc.strip():
    prompt = make_prompt(desc, lieu, quete)
    prefix = make_prefix()
    suffix = make_suffix()

    with st.spinner("Génération de la fiche PNJ en cours..."):
        # OpenAI API call
        client = OpenAI(api_key=cle_api)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Tu es un générateur de fiches PNJ pour un JDR heroic-fantasy."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=1,
            top_p=1
        )
        fiche = response.choices[0].message.content

    st.markdown("### Résultat de la fiche personnage générée :")
    st.code(f"{prefix}\n---\n{fiche}\n---\n{suffix}", language="markdown")

elif submit:
    st.warning("Merci de décrire ton PNJ avant de lancer la génération.")

st.markdown("---")

import datetime
import json
import os

HISTO_PATH = "historique_pnj.json"

# Charger l'historique depuis le fichier au démarrage
def load_history():
    if os.path.exists(HISTO_PATH):
        with open(HISTO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Sauvegarder l'historique dans le fichier
def save_history(history):
    with open(HISTO_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Charger en session_state si ce n'est pas déjà fait
if "pnj_history" not in st.session_state:
    st.session_state.pnj_history = load_history()

# Lorsqu’on génère, on enregistre le prompt complet dans l’historique et dans le fichier
if submit and desc.strip():
    full_prompt = f"{prefix}\n---\n{fiche}\n---\n{suffix}"
    history_title = fiche[:40].replace("\n", " ").replace("  ", " ") + "..."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "title": history_title,
        "datetime": timestamp,
        "prompt": full_prompt,
    }
    st.session_state.pnj_history.append(new_entry)
    save_history(st.session_state.pnj_history)  # On sauvegarde après ajout

# Affichage de l'historique
if st.session_state.pnj_history:
    st.markdown("### Historique des prompts générés")

    for i, entry in enumerate(st.session_state.pnj_history):
        with st.expander(f"{entry['title']})", expanded=False):
            st.markdown("#### Prompt complet")
            st.code(entry["prompt"], language="markdown")

            
            if st.button("Supprimer ce prompt", key=f"delete_{i}"):
                st.session_state.pnj_history.pop(i)
                save_history(st.session_state.pnj_history)
                st.rerun()