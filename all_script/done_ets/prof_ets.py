import csv
import requests
from bs4 import BeautifulSoup

fichier = "ets_prof.csv"

def if_no_poste(poste):
    if poste is None:
        return ""
    else:
        return poste

def if_no_adresse_courriel(adresse_courriel):
    if adresse_courriel is None:
        return ""
    else:
        return adresse_courriel

def determiner_sexe_prof(sexe):
    if sexe == "Professeure":
        return "femme"
    elif sexe == "Professeur":
        return "homme"
    elif sexe == "Directeur":
        return "homme"

def if_no_num_tel(num_tel):
    if num_tel is None:
        return ""
    else:
        return num_tel

def trouver_expertise_prof():
    if expertise is None:
        return ""
    else:
        expert = str(expertise.find_next("ul").text).replace("\n", "|")
        return expert

n = 0
entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}
with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)
    creation_fichier.writerow(["Université", "Prénom et nom", "Département", "Poste du prof", "Genre du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])

    for item in range(ord('a'), ord('z')+1):
        upper_chars = chr(item).upper() 
        url = "https://www.etsmtl.ca/recherche/professeurs-chercheurs/t/" + upper_chars
        contenu = requests.get(url,headers=entete)
        n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
        page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
        div_fiche_prof = page.find_all("div", class_="list__prof-list__item")

        for fiche_prof in div_fiche_prof:
            n += 1
            lien_fiche_prof = fiche_prof.find("a")["href"]
            #print(lien_fiche_prof)
            fiche_prof_url = "https://www.etsmtl.ca" + lien_fiche_prof
            contenu2 = requests.get(fiche_prof_url,headers=entete)
            page_fiche_prof = BeautifulSoup(contenu2.text, "html.parser")
            coordonnees = page_fiche_prof.find("div", class_="wrapper fiche__wrapper")
            
            print("<>" * 40)

            #Nom de l'université -->
            universite = "École de technologie supérieure"

            #Nom du / de la prof.e -->
            nom_du_prof = coordonnees.find("h1").find("span", class_="fiche__header").text.strip()
            #print(nom_du_prof)

            #Département du / de la prof.e --->
            departement = page_fiche_prof.find("div", class_="wrapper_content_tab").find("h2").text.strip()

            #Poste --->
            elements = page_fiche_prof.find_all("span", class_="fiche__item__desc")
            poste = elements[0].text
            poste_prof = if_no_poste(poste)
            #print(poste_prof)
            
            #Sexe --->
            if " " in poste_prof:
                sexe = poste_prof[0:poste_prof.find(" ")]
            else:
                sexe = poste_prof
            genre_prof = determiner_sexe_prof(sexe)
            #print(genre_prof)
            # print(sexe)

            fiche_item = page_fiche_prof.find_all("div", class_="fiche__item")
            fiche_item_label = page_fiche_prof.find("span", class_="fiche__item__label")
            #print(fiche_item_label)
            
            for elem in fiche_item:
            #Courriel --->
                if elem.get_text().split()[0] in ["Courriel"]:
                    adresse_courriel = elem.find_next("span")
                    if_no_adresse_courriel(adresse_courriel)
                    courriel = adresse_courriel.find_next("span").text.strip()
                    #print(courriel)
            #Téléphone numéro de --->
                elif elem.get_text().split()[0] in ["Téléphone"]:
                    num_tel = elem.find_next("span")
                    if_no_num_tel(num_tel)
                    telephone = num_tel.find_next("span").text.strip()
                    #print(telephone)

            #Champs d'expertise --->
            expertise = page_fiche_prof.find("div", class_="wrapper_content_tab").find("h3", text=" Expertises :")
            champ_expert = trouver_expertise_prof()
            #print(champ_expert)

            infos = [universite, nom_du_prof, departement, poste_prof, genre_prof, courriel, telephone, champ_expert, fiche_prof_url]
            #print(n, "Le petit train avance...")
            print(infos)
            creation_fichier.writerow(infos)