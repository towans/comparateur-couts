
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
prix_centrale = st.number_input("Prix HT - Centrale d’achat (€)", min_value=0.0, format="%.2f")
prix_local = st.number_input("Prix HT - Fournisseur local (€)", min_value=0.0, format="%.2f")

# Soumettre
if st.button("Comparer") and produit:
    cout_centrale = prix_centrale * 1.187
    difference = prix_local - cout_centrale

    if difference > 0:
        verdict = f"Centrale moins chère de {abs(difference):.2f} €"
    elif difference < 0:
        verdict = f"Fournisseur local moins cher de {abs(difference):.2f} €"
    else:
        verdict = "Égalité parfaite"

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

    st.success(f"Comparaison enregistrée pour **{produit}**")

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
