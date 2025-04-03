import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Précipitations par Année",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour détecter le début, la fin et la durée des pluies par année
def detecter_periodes_pluie_par_annee(df, seuil_precipitation=5):
    resultats = []
    localites = df['localite'].unique()
    
    for localite in localites:
        df_loc = df[df['localite'] == localite].sort_values('date')
        df_loc['annee'] = df_loc['date'].dt.year
        annees = df_loc['annee'].unique()
        
        for annee in annees:
            df_annee = df_loc[df_loc['annee'] == annee]
            debut_pluie = df_annee[df_annee['precipitation'] > seuil_precipitation]['date'].min()
            fin_pluie = df_annee[df_annee['precipitation'] > seuil_precipitation]['date'].max()
            
            if pd.notna(debut_pluie) and pd.notna(fin_pluie):
                duree = (fin_pluie - debut_pluie).days + 1  # +1 pour inclure le jour de fin
                resultats.append({
                    'localite': localite,
                    'annee': annee,
                    'debut_pluie': debut_pluie,
                    'fin_pluie': fin_pluie,
                    'duree_jours': duree
                })
    
    return pd.DataFrame(resultats)

# Sidebar pour les contrôles
with st.sidebar:
    st.title("Paramètres")
    uploaded_file = st.file_uploader("Charger le fichier Excel", type=['xlsx'])
    seuil = st.slider("Seuil de précipitation (mm)", 1, 20, 5)
    max_annees_graph = st.slider("Nombre max d'années à afficher", 1, 10, 5)
    st.markdown("---")
    st.info("Format attendu : localite, date, precipitation")

# Main content
st.title("Analyse des Précipitations par Localité et Année")
st.markdown("Visualisez et analysez les périodes et durées de pluie par localité et par année")

if uploaded_file is not None:
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(uploaded_file)
        df['date'] = pd.to_datetime(df['date'])
        
        # Vérification des colonnes nécessaires
        required_columns = ['localite', 'date', 'precipitation']
        if not all(col in df.columns for col in required_columns):
            st.error("Le fichier doit contenir les colonnes : localite, date, precipitation")
        else:
            # Extraction des années
            df['annee'] = df['date'].dt.year
            annees_disponibles = sorted(df['annee'].unique())
            
            # Sélection des années dans la sidebar
            with st.sidebar:
                annees_selectionnees = st.multiselect(
                    "Sélectionner les années",
                    options=annees_disponibles,
                    default=annees_disponibles[:max_annees_graph]
                )
            
            # Filtrer les données selon les années sélectionnées
            df_filtre = df[df['annee'].isin(annees_selectionnees)]
            
            # Création de deux colonnes pour le layout
            col1, col2 = st.columns(2)
            
            # Graphique interactif dans la première colonne
            with col1:
                st.subheader("Distribution des Précipitations")
                fig = px.scatter(
                    df_filtre,
                    x='date',
                    y='precipitation',
                    color='localite',
                    facet_col='annee',
                    title="Précipitations par Date, Localité et Année",
                    height=500,
                    facet_col_spacing=0.05
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Précipitation (mm)",
                    legend_title="Localité"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Analyse des périodes dans la deuxième colonne
            with col2:
                st.subheader("Périodes et Durées de Pluie par Année")
                resultats = detecter_periodes_pluie_par_annee(df_filtre, seuil)
                
                # Formatage des dates pour l'affichage
                resultats_display = resultats.copy()
                resultats_display['debut_pluie'] = resultats_display['debut_pluie'].dt.strftime('%Y-%m-%d')
                resultats_display['fin_pluie'] = resultats_display['fin_pluie'].dt.strftime('%Y-%m-%d')
                
                st.dataframe(
                    resultats_display,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "duree_jours": st.column_config.NumberColumn("Durée (jours)", format="%d")
                    }
                )
                
                # Bouton d'exportation
                csv = resultats.to_csv(index=False)
                st.download_button(
                    label="Exporter les résultats (CSV)",
                    data=csv,
                    file_name=f"periodes_pluie_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # Graphique temporel par localité et année
            st.subheader("Évolution Temporelle")
            localite_selection = st.selectbox("Choisir une localité", df_filtre['localite'].unique())
            annee_selection = st.selectbox("Choisir une année", annees_selectionnees)
            
            df_loc_annee = df_filtre[
                (df_filtre['localite'] == localite_selection) & 
                (df_filtre['annee'] == annee_selection)
            ]
            
            fig_temps = px.line(
                df_loc_annee,
                x='date',
                y='precipitation',
                title=f"Précipitations à {localite_selection} ({annee_selection})",
                height=300
            )
            fig_temps.add_hline(y=seuil, line_dash="dash", line_color="red", 
                              annotation_text=f"Seuil: {seuil}mm")
            st.plotly_chart(fig_temps, use_container_width=True)
            
            # Affichage de la durée pour la sélection
            duree_selection = resultats[
                (resultats['localite'] == localite_selection) & 
                (resultats['annee'] == annee_selection)
            ]['duree_jours'].iloc[0] if not resultats.empty else "N/A"
            st.write(f"Durée de la saison de pluie : **{duree_selection} jours**")
            
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {str(e)}")
else:
    st.warning("Veuillez charger un fichier Excel pour commencer l'analyse.")
    
    # Exemple de format de fichier
    st.markdown("### Exemple de format attendu :")
    exemple_data = pd.DataFrame({
        'localite': ['Ville1', 'Ville1', 'Ville2'],
        'date': ['2023-01-01', '2023-06-02', '2024-01-01'],
        'precipitation': [10, 15, 5]
    })
    st.dataframe(exemple_data)