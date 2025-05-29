
import streamlit as st

st.title("Comparateur de coût : Centrale vs Fournisseur local")

st.markdown("Entrez les prix HT pour comparer les deux options d’achat.")

prix_centrale = st.number_input("Prix HT - Centrale d’achat (€)", min_value=0.0, format="%.2f")
prix_local = st.number_input("Prix HT - Fournisseur local (€)", min_value=0.0, format="%.2f")

if prix_centrale > 0 and prix_local > 0:
    cout_centrale = prix_centrale * 1.187
    difference = prix_local - cout_centrale

    st.markdown(f"### Résultats :")
    st.markdown(f"- Coût total via la **centrale** : **{cout_centrale:.2f} €**")
    st.markdown(f"- Coût via le **fournisseur local** : **{prix_local:.2f} €**")

    if difference > 0:
        st.success(f"✅ La **centrale** est moins chère de {abs(difference):.2f} €.")
    elif difference < 0:
        st.warning(f"⚠️ Le **fournisseur local** est moins cher de {abs(difference):.2f} €.")
    else:
        st.info("🤝 Les deux options reviennent au **même prix**.")
