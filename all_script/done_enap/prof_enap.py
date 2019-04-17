import csv
import requests
from bs4 import BeautifulSoup

fichier = "enap_prof.csv"

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

def if_no_poste(poste_prof):
    if poste_prof is None:
        return ""
    else:
        return poste_prof.text.strip()

def deteminer_genre(sex):
    if sex == "Professeure":
        return "femme"
    elif sex == "Directrice":
        return "femme"
    elif sex == "Professeur":
        return "homme"
    elif sex == "Directeur":
        return "homme"
    elif sex == "Maître":
        return "impossible à déterminer"



def if_no_depart(campus_dep):
    if campus_dep is None:
        return ""
    else:
        return campus_dep.text.strip()

def if_no_num_tel(numero_telephone):
    if numero_telephone is None:
        return ""
    else:
        num_telephone = numero_telephone.text 
        num = num_telephone[num_telephone.find(":")+2:]
        if coordonnees.find("span", id="ctl13_ctl00_emploisRepeater_Label4_0") is not None :
            return num + coordonnees.find("span", id="ctl13_ctl00_emploisRepeater_Label4_0").text
        else:
            return num

def if_no_email(adresse_courriel):
    if adresse_courriel is None:
        return ""
    else:
        return adresse_courriel

def if_no_expert(champs_expertise):
    try:
        list = []
        expert = champs_expertise.find_all("span")
        for exp in expert:
            list.append(exp.get_text())
        elements = str(list).replace(",", "|")
        return elements
    except AttributeError:
        return ""

url = "http://enap.ca/enap/fr/EnseigantUniversite-intro.aspx"
contenu = requests.get(url,headers=entete)
n = 0
page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
profil_div = page.find("div", id="profilDiv")
liste_profs = profil_div.find_all("div", attrs={"style":"white-space: nowrap;"})


with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)
    creation_fichier.writerow(["Université", "Prénom et nom", "Campus", "Poste du prof", "Genre du prof","Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])
    for profs in liste_profs:
        if profs.find("a") is not None:
            href = profs.find("a")["href"]
            #print(href)
            url_prof = "http://enap.ca" + href
            #print(url_prof)
            n +=1
            contenu2 = requests.get(url_prof,headers=entete)
            page_prof = BeautifulSoup(contenu2.text,"html.parser") #pour analyser le code html
            coordonnees = page_prof.find("div", class_="profil_boite")
            print("<>" * 40)

            universite = "Ecole nationale d'administration publique"

            #Nom du / de la prof.e
            nom_du_prof = page_prof.find("div", class_="profs_nomLabel").text.strip()
            #print(nom_du_prof)

            #Poste prof.e
            poste_prof = coordonnees.find("div", class_="profil_titre2")
            poste = if_no_poste(poste_prof)
            #print(poste)
            
            #Sexe du prof --->
            sexe = poste_prof.text.strip()
            if " " in sexe:
                sex = sexe[0:sexe.find(" ")]
            else:
                sex = sexe
            #print(sex)
            genre = deteminer_genre(sex)
            #print(genre)

            #Département du / de la prof.e
            campus_dep = coordonnees.find("div", class_="profil_campus")
            campus = if_no_depart(campus_dep)
            #print(campus_dep)

            #Numéro de téléphone
            numero_telephone = coordonnees.find("span", id="ctl13_ctl00_emploisRepeater_Label3_0")
            numero = if_no_num_tel(numero_telephone)
            #print(num_telephone)

            #Courriel 
            adresse_courriel = coordonnees.find("div", class_="profil_courriel").find("a").text
            courriel = if_no_email(adresse_courriel)
            #print(adresse_courriel)

            #Expertise 
            champs_expertise = page_prof.find("td", attrs={"valign":"top"})
            exp = if_no_expert(champs_expertise)
            print(exp)
            
            #print(n, "Le petit train travaille...")
            infos = [universite, nom_du_prof, campus, poste, genre, adresse_courriel, numero, exp, url_prof]
            print(infos)
            creation_fichier.writerow(infos)
            
### Après coup, il faut modifier la section des maître d'enseignement et ajouter leur sexe manuellement.