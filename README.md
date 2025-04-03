# Analyse des Précipitations par Année

Ce projet permet d'analyser les données de précipitations par localité et par année à l'aide de Streamlit, Pandas et Plotly. L'application interactive permet de visualiser les périodes de pluie et d'explorer les données de manière intuitive.

## Fonctionnalités

- Chargement d'un fichier Excel contenant des données de précipitations.
- Détection des périodes de pluie par localité et par année.
- Visualisation des distributions de précipitations à l'aide de graphiques interactifs.
- Exportation des résultats sous forme de fichier CSV.
- Sélection des années et des localités pour une analyse ciblée.

## Prérequis

Assurez-vous d'avoir installé les bibliothèques nécessaires. Vous pouvez les installer via pip :

```bash
pip install streamlit pandas plotly openpyxl
```

## Utilisation

1. **Lancer l'application** :
   Exécutez la commande suivante dans votre terminal :

   ```bash
   streamlit run app.py
   ```

2. **Charger un fichier Excel** :
   Dans la barre latérale, utilisez le bouton de téléchargement pour charger un fichier Excel contenant les colonnes suivantes :
   - `localite` : Nom de la localité
   - `date` : Date des précipitations (format : YYYY-MM-DD)
   - `precipitation` : Quantité de précipitations en millimètres

3. **Configurer les paramètres** :
   Ajustez le seuil de précipitation et le nombre maximal d'années à afficher à l'aide des curseurs.

4. **Visualiser les données** :
   Explorez les graphiques générés pour analyser les tendances de précipitations et les périodes de pluie.

5. **Exporter les résultats** :
   Utilisez le bouton d'exportation pour télécharger les périodes de pluie détectées au format CSV.

## Exemple de format de fichier attendu

Voici un exemple de données que votre fichier Excel devrait contenir :

| localite | date       | precipitation |
|----------|------------|---------------|
| Ville1   | 2023-01-01 | 10            |
| Ville1   | 2023-06-02 | 15            |
| Ville2   | 2024-01-01 | 5             |

## Auteurs

- POUM BIMBAR Paul Ghislain - Développeur principal

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
