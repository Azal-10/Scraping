import requests
from bs4 import BeautifulSoup
import csv
import json

# URL du site à scraper
url = "http://books.toscrape.com/"

# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les livres (ils sont dans des balises <article> avec la classe 'product_pod')
    books = soup.find_all('article', class_='product_pod')

    # Liste pour stocker les données des livres
    books_data = []

    # Parcourir chaque livre pour extraire les détails
    for book in books:
        # Extraire le titre (dans une balise <h3> > <a> > attribut 'title')
        title = book.h3.a['title']

        # Extraire le prix (dans une balise <p> avec la classe 'price_color')
        price = book.find('p', class_='price_color').text

        # Extraire les étoiles de notation (dans la classe de la balise <p> avec la classe 'star-rating')
        rating_class = book.p['class']  # Exemple : ['star-rating', 'Three']
        rating = rating_class[1]  # La note est le deuxième élément de la liste

        # Extraire le lien de l'image (dans une balise <img> > attribut 'src')
        image_url = book.img['src']
        full_image_url = f"http://books.toscrape.com/{image_url}"  # Convertir en URL absolue

        # Ajouter les données du livre à la liste
        books_data.append({
            'Titre': title,
            'Prix': price,
            'Note': rating,
            'Image URL': full_image_url
        })

        # Afficher les détails du livre (optionnel)
        print(f"Titre : {title}")
        print(f"Prix : {price}")
        print(f"Note : {rating}")
        print(f"Image URL : {full_image_url}")
        print("-" * 50)  # Séparateur pour plus de clarté

    # Exporter les données en CSV
    with open('books_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Titre', 'Prix', 'Note', 'Image URL'])
        writer.writeheader()
        writer.writerows(books_data)

    # Exporter les données en JSON
    with open('books_data.json', mode='w', encoding='utf-8') as file:
        json.dump(books_data, file, ensure_ascii=False, indent=4)

    print("Données exportées avec succès dans 'books_data.csv' et 'books_data.json'.")
else:
    print(f"Erreur : Impossible d'accéder au site (code {response.status_code})")