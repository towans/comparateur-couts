
import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.title("Comparateur de coût : Centrale vs Fournisseur local")

# Définir le fichier d'historique
HISTO_PATH = Path("historique.json")

# Charger l'historique existant
if HISTO_PATH.exists():
    with open(HISTO_PATH, "r", encoding="utf-8") as f:
        historique_data = json.load(f)
else:
    historique_data = {}

# Interface utilisateur
st.markdown("Entrez les informations pour comparer les deux options d’achat.")

produit = st.text_input("Nom du produit (obligatoire)").strip()

# Champs prix en texte pour meilleure UX (effacement auto)
col1, col2 = st.columns(2)
with col1:
    prix_centrale_input = st.text_input("Prix HT - Centrale (€)", value="", key="prix_centrale")
with col2:
    prix_local_input = st.text_input("Prix HT - Local (€)", value="", key="prix_local")

# Soumettre
if st.button("Comparer") and produit and prix_centrale_input and prix_local_input:
    try:
        prix_centrale = float(prix_centrale_input.replace(",", "."))
        prix_local = float(prix_local_input.replace(",", "."))

        cout_centrale = prix_centrale * 1.187
        difference = prix_local - cout_centrale

        if difference > 0:
            verdict = f"Centrale moins chère de {abs(difference):.2f} €"
            st.success(f"✅ {verdict}")
        elif difference < 0:
            verdict = f"Fournisseur local moins cher de {abs(difference):.2f} €"
            st.warning(f"⚠️ {verdict}")
        else:
            verdict = "Égalité parfaite"
            st.info("🤝 Les deux options reviennent au **même prix**.")

        # Mise à jour ou ajout dans l'historique
        historique_data[produit] = {
            "Prix centrale (€)": prix_centrale,
            "Prix local (€)": prix_local,
            "Centrale après cotisations (€)": round(cout_centrale, 2),
            "Verdict": verdict
        }

        # Sauvegarde du fichier
        with open(HISTO_PATH, "w", encoding="utf-8") as f:
            json.dump(historique_data, f, indent=2, ensure_ascii=False)

    except ValueError:
        st.error("⛔️ Merci d’entrer des nombres valides pour les prix.")

# Affichage de l'historique
if historique_data:
    st.markdown("## 📊 Historique des produits comparés")
    df = pd.DataFrame.from_dict(historique_data, orient="index")
    df.index.name = "Produit"
    st.dataframe(df.reset_index(), use_container_width=True)

# Réinitialiser
if st.button("Réinitialiser l'historique"):
    if HISTO_PATH.exists():
        HISTO_PATH.unlink()
    st.experimental_rerun()
