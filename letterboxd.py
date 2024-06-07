import csv
from selenium import webdriver
from bs4 import BeautifulSoup

webdriver_path = r"C:\Users\loris\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(webdriver_path)


names_list = []
link_base = "https://www.allocine.fr"
with open ('watchlist.csv', 'r') as csvfile :
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        completes_movies = []
        completes_movies.append(row[1])
        completes_movies.append(row[2])
        names_list.append(completes_movies)

# print(names_list)
nb_passage = 0
for x in range(len(names_list)):
    complete_movie = names_list[x]
    # print(complete_movie)
    link_search = "https://www.allocine.fr/rechercher/?q="
    link_name = complete_movie[0]+ " " +complete_movie[1]
    link_name = link_name.replace(" ", "%20")
    link_search = link_search + link_name
    # print(link_search)
    driver.get(link_search)
    driver.implicitly_wait(10)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    link_movie=soup.find(class_="xXx meta-title-link")
    print(link_movie)
    names_list[x].append(link_movie.get('href'))
    #print(names_list)
    lien_fiche_movie = link_base + names_list[x][2]
    driver.get(lien_fiche_movie)
    driver.implicitly_wait(10)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    link_sceance = soup.find(class_="seance item")
    #print(link_sceance)
    liste_sceance_salle = []
    compteur=0
    # print('nombre de passage', nb_passage)
    # nb_passage += 1
    try :
        names_list[x].append(link_sceance.get('href'))
        #print(names_list[x])
        for day in range(7):
            jour = "d-" + str(day) + "/"
            lien_sceance = link_base + link_sceance.get('href')+jour
            # print(lien_sceance)
            driver.get(lien_sceance)
            driver.implicitly_wait(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title_cinema = soup.find('h2', class_="title")
            # print("jour",x ,title_cinema)
            if not(title_cinema):
                #Erreur ?
                liste_sceance_salle.append("NONE")
                compteur += 1
            else:
                # for i in range(len(title_cinema)):
                #print(title_cinema.text.strip())
                liste_sceance_salle.append(title_cinema.text.strip())
        if compteur == 7 : 
            names_list[x].append("Seances dans plus d'une semaine")
        else : 
            names_list[x].append(liste_sceance_salle)
    except AttributeError: 
        names_list[x].append("Pas de séances")

print(names_list)

# Ouverture du fichier CSV en mode écriture
with open('letterboxd.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Création d'un objet CSV writer
    csv_writer = csv.writer(csv_file)

    # Écriture de l'en-tête
    csv_writer.writerow(['Titre', 'Date', 'lien_film', 'Seances', 'lieux_seances'])

    # Parcourir la liste des données et écrire chaque ligne dans le fichier CSV
    for row in names_list:
        title, date, film_link, seances = row[:4]
        lieux_seances = row[4] if len(row) > 4 else []

        # Si la dernière colonne est une liste, convertissez-la en chaîne séparée par des virgules
        if isinstance(lieux_seances, list):
            lieux_seances = ', '.join(lieux_seances)

        # Écrire la ligne dans le fichier CSV
        csv_writer.writerow([title, date, film_link, seances, lieux_seances])

print('Le fichier CSV a été créé avec succès ')
