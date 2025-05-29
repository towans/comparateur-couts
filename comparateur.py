
import streamlit as st
import pandas as pd

st.title("Comparateur de coût : Centrale vs Fournisseur local")
st.markdown("Entrez les prix HT pour comparer les deux options d’achat.")

# Initialiser l'historique
if "historique" not in st.session_state:
    st.session_state.historique = []

# Entrée utilisateur
produit = st.text_input("Nom du produit (facultatif)")
prix_centrale = st.number_input("Prix HT - Centrale d’achat (€)", min_value=0.0, format="%.2f")
prix_local = st.number_input("Prix HT - Fournisseur local (€)", min_value=0.0, format="%.2f")

# Calcul
if prix_centrale > 0 and prix_local > 0:
    cout_centrale = prix_centrale * 1.187
    difference = prix_local - cout_centrale

    st.markdown("### Résultats :")
    st.markdown(f"- Coût total via la **centrale** : **{cout_centrale:.2f} €**")
    st.markdown(f"- Coût via le **fournisseur local** : **{prix_local:.2f} €**")

    if difference > 0:
        verdict = f"Centrale moins chère de {abs(difference):.2f} €"
        st.success(f"✅ {verdict}")
    elif difference < 0:
        verdict = f"Fournisseur local moins cher de {abs(difference):.2f} €"
        st.warning(f"⚠️ {verdict}")
    else:
        verdict = "Égalité parfaite"
        st.info("🤝 Les deux options reviennent au **même prix**.")

    # Ajouter à l'historique
    st.session_state.historique.append({
        "Produit": produit if produit else "(Sans nom)",
        "Prix centrale (€)": prix_centrale,
        "Prix local (€)": prix_local,
        "Centrale après cotisations (€)": round(cout_centrale, 2),
        "Verdict": verdict
    })

# Affichage de l'historique
if st.session_state.historique:
    st.markdown("## 📊 Historique de comparaison")
    df = pd.DataFrame(st.session_state.historique)
    st.dataframe(df, use_container_width=True)
