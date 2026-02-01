# Projet de Suivi d'Objet

## Description

Ce projet implémente un système de suivi d'objets dans des vidéos en utilisant la méthode de sélection de ROI (Region of Interest).

## Structure du projet

```
.
├── main.py                                 # Script principal
├── Select ROI_screenshot_31.01.2026.png    # Exemple d'image pour la sélection
├── video/                                  # Dossier contenant les vidéos
├── rapportTp4.pdf                          # Documentation du projet
└── utils/
    └── func_utils_.py                      # Fonctions utilitaires nécessaires
```

## Prérequis

- Python 3.x
- Bibliothèques nécessaires (OpenCV, etc.)

## Installation

1. Assurez-vous que toutes les dépendances sont installées
2. Les fonctions nécessaires au fonctionnement du code se trouvent dans le fichier `func_utils_` situé dans le dossier `utils`

## Exécution

1. Placez-vous dans le dossier contenant le fichier `main.py`
2. Ouvrez un terminal
3. Exécutez la commande :

```bash
python3 main.py
```

## Utilisation

1. Lancez le programme avec la commande ci-dessus
2. Sélectionnez l'objet que vous souhaitez suivre en dessinant un rectangle autour
3. Appuyez sur **Entrée** ou **Espace** pour valider la sélection
4. Observez les résultats du suivi en temps réel

## Notes

- L'interface graphique s'ouvrira automatiquement
- Utilisez la souris pour sélectionner la région d'intérêt
- L'image `Select ROI_screenshot_31.01.2026.png` montre un exemple de sélection
