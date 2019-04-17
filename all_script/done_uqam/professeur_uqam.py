# coding : utf-8

import csv
import requests
from bs4 import BeautifulSoup
from uqam_function import * #permet de faire sortir tout ce que le document fonction contient. 

fichier = "professeur_UQAM.csv"

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

url = "https://professeurs.uqam.ca/liste-departements-ecoles/"
contenu = requests.get(url,headers=entete)
n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
div_departements = page.find("div", class_="entry-content")
departements = div_departements.find_all("li")

with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)
    creation_fichier.writerow(["Université", "Prénom et nom", "Département", "Poste du prof", "Genre du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Entretien avec médias", "Lien vers le prof"])

    #Ici je suis à la première page et je veut accéder aux différents départements.
    for departement in departements:
        lien_departement = departement.find("a")["href"] #Trouver le lien qui mènent vers les départements
        
        #Ici je suis dans la page des différents départements et je veux accéder aux professeurs.
        contenu2 = requests.get(lien_departement,headers=entete) #Accéder à la page
        page_departement = BeautifulSoup(contenu2.text, "html.parser") #Lire la page
        professeurs = page_departement.find_all("div", class_="vignette")
        for professeur in professeurs:
            n +=1   
            url_href = professeur.find("a")["href"] #Trouver le lien qui mènent vers la page du prof.e
            if not "/QKM%252fbavKTxUIk141GN77Uw__/" in url_href: #cet URL était un page "Poste Vacant," c'était la seule qui causait problème. 
                url_enseignants = "https://professeurs.uqam.ca" + url_href #Compléter la page avec l'url précédent
                contenu3 = requests.get(url_enseignants,headers=entete) #Accéder à la page
                page_prof = BeautifulSoup(contenu3.text, "html.parser") #Lire la page
                universite = "Université du Québec à Montréal"
                print("<>" * 40)

                #Nom de l'enseignant.e --->
                nom_du_prof = page_prof.find("header",class_="entry-header").find("h1")
                prenom_nom_famille = trouver_nom_du_prof(nom_du_prof)
                #print(prenom_nom_famille)

                #Département --->
                departement_prof = page_prof.find("div", class_="unite contenu_icone")
                type_depart = trouver_departement_prof(departement_prof)
                
                #Poste --->
                poste_prof = page_prof.find("div", class_="titre_professeur")
                prof_poste = trouver_poste_prof(poste_prof)
                #print(prof_poste)

                #Genre --->
                sexe = poste_prof.text
                if " " in sexe:
                    sexe_prof = sexe[0:sexe.find(" ")]
                else:
                    sexe_prof = sexe
                genre_prof = determiner_sex(sexe_prof)
                #print(genre_prof)

                #Courriel --->
                courriel_prof = page_prof.find("div", class_="courriel contenu_icone")
                adresse_courriel = trouver_courriel_prof(courriel_prof)

                #Téléphone --->
                telephone_prof = page_prof.find("div", class_="telephone contenu_icone").contents[2]
                numero_tel = trouver_telephone_prof(telephone_prof)

                #Champ d'expertise --->
                expertise = page_prof.find("div", id="expertises")
                #print(trouver_expertise(expertise))
                domaine_expertise = trouver_expertise(expertise)

                #Entretien média :
                entretenir_media = page_prof.find("div", class_="messageMedia contenu_icone")
                parler_media = parler_ou_non_media(entretenir_media)
                
                #print(n, "Le petit train travaille...")
                infos = [universite, prenom_nom_famille, type_depart, prof_poste, genre_prof, adresse_courriel, numero_tel, domaine_expertise, parler_media, url_enseignants]
                print(infos)
                creation_fichier.writerow(infos)

    #Le document .csv nécessite quand même un nettoyage après coup, parce que certains professeurs reviennent deux fois. Dont Jessica Payeras-Robles et Djaouida Hamdani
    ## Une prof.e marquée Chargée de cours devra être retirée. 
    ###Et le genre des maîtres doivent être fait manuellement si possible. Certains n'ont pas de photo donc impossible à déterminer