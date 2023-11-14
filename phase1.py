import argparse
import requests
import json
from datetime import datetime


def analyser_commande():

    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser =argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")

    parser.add_argument("symbole", nargs = "+", help="Le nom du symbole boursier")
    parser.add_argument("-d","--début", help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f","--fin", help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
    parser.add_argument("-v","--valeur", choices=["fermeture", "ouverture", "min", "max", "volume"], default = "fermeture", help="La valeur désiré (par défaut: fermeture)")

       return parser.parse_args()

def produire_historique(symbole, début, fin, valeur):
    """
    Récupérer l'historique d'un symbole pour une période donnée.

    Args:
        symbole (str): Le nom du symbole boursier.
        début (str): La date de début de l'historique (format: AAAA-MM-JJ).
        fin (str): La date de fin de l'historique (format: AAAA-MM-JJ).
        valeur (str): La valeur désirée (fermeture, ouverture, min, max, volume).

    Returns:
        list: Une liste de tuples (date, valeur) pour la période spécifiée.
    """

    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': début, 'fin': fin}
    réponse = requests.get(url=url, params=params)

     if réponse.status_code == 200:
        historique = réponse.json().get('historique', {})
        if historique:
            # Manipulez l'historique selon la valeur désirée et retournez la liste de tuples (date, valeur)
            # ...
            return historique
        else:
            print(f"Aucun historique trouvé pour le symbole {symbole} dans la période spécifiée.")
    else:
        print(f"Échec de la requête pour le symbole {symbole}. Code d'erreur : {réponse.status_code}")

if __name__ == "__main__":
    args = analyser_commande()

    for symbole in args.symboles:
        début = args.début if args.début else datetime.now().strftime('%Y-%m-%d')
        fin = args.fin if args.fin else datetime.now().strftime('%Y-%m-%d')

        historique = produire_historique(symbole, début, fin, args.valeur)

        # Format de l'affichage
        print(f"titre={symbole}: valeur={args.valeur}, début={début}, fin={fin}")
        print(historique)
        print()