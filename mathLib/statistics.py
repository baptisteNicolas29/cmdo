from typing import Tuple, List

import numpy as np


__all__: List[str] = [
    'mirrored_gaussian_profile',
    'retrieve_gaussian_profile',
]


def mirrored_gaussian_profile(
    length: int = None,
    std_dev: float = None,
    start: int = None
) -> np.ndarray:

    """
    Génère une liste avec un profil gaussien symétrique autour du centre.

    Paramètres :
        - length :
            int, nombre total d'éléments dans la liste
            (doit être impair pour un centre exact)
        - std_dev :
            float, écart-type pour contrôler la largeur du pic
        - start :
            int, valeur de départ pour la normalisation

    Retour :
        - np.ndarray
            liste de valeurs suivant un profil gaussien symétrique
    """

    if length is None:
        raise ValueError(
            "Le nombre d'éléments n doit être spécifié."
        )
    if length % 2 == 0:
        raise ValueError(
            "Le nombre d'éléments n doit être impair\
            pour avoir un centre exact."
        )

    std_dev = std_dev or 1.0
    length = length - (start * 2) if start is not None else length

    # Calcul des valeurs gaussiennes pour la moitié de la liste
    half_n = length // 2 + 1
    half_values = [
        np.exp(-0.5 * ((i - half_n + 1) / std_dev) ** 2)
        for i in range(half_n)
    ]

    # Normaliser la moitié des valeurs entre 0 et 1
    max_value = max(half_values)
    normalized_half = [v / max_value for v in half_values]

    # Construire la liste complète avec la symétrie autour du centre
    full_values = normalized_half + normalized_half[-2::-1]

    # Ajouter des zéros aux extrémités
    if start is not None:
        to_add = [0] * start
        full_values = to_add + full_values + to_add

    return full_values


def retrieve_gaussian_profile(
    values: List[float]
) -> Tuple[int, float, int]:

    """
    Retrouve std_dev et start à partir d'une liste donnée.

    Paramètres :
        - values : list[float]
            une liste suivant un profil gaussien symétrique.

    Retour :
        - Tuple[int, float, int]
            paramètres estimés.
    """

    # Identifier 'start' en comptant les zéros au début
    start = 0
    while start < len(values) and values[start] == 0:
        start += 1

    # Extraire la partie centrale sans les zéros
    trimmed_values = values[start:len(values)-start]

    # Vérifier la symétrie
    if trimmed_values != trimmed_values[::-1]:
        raise ValueError("Les valeurs ne sont pas symétriques.")

    # Identifier le centre
    center_index = len(trimmed_values) // 2
    center_value = trimmed_values[center_index]

    # Utiliser la définition de la gaussienne pour trouver std_dev
    x = np.arange(center_index + 1)  # Distance par rapport au centre
    y = np.array(trimmed_values[center_index:])

    # Calculer les distances standardisées
    log_y = np.log(y / center_value)  # Échelle logarithmique
    std_dev = np.sqrt(-x[1]**2 / (2 * log_y[1]))
    std_dev = round(std_dev, 3)

    return len(values), std_dev, start
