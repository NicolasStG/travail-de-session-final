# coding : utf-8
import csv
import requests
from bs4 import BeautifulSoup
from genderize import Genderize

fichier = "professeur_inrs.csv"

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

def trouver_courriel_prof(adresse_courriel):
    if adresse_courriel is None:
        return ""
    else : 
        return adresse_courriel.text

def trouver_sexe_prof(prenom):
    sexe = Genderize().get([prenom])
    for sex in sexe:
        gender = list(sex.values())[1]
        #print(gender)
        if gender is not None:
            probability = list(sex.values())[2]
        #print(probability)
        if gender == None:
            return "impossible à déterminer"
        else:
            if gender == "female":
                try:
                    if probability >= 0.75:
                        return "femme"
                except IndexError:    
                        return "impossible à déterminer"
            elif gender == "male":
                try:
                    if probability >= 0.75:
                        return "homme"
                except IndexError:
                    return "impossible à déterminer"
                    
def trouver_telephone_prof(numero_telephone):
    if numero_telephone is None:
        return ""
    else :
        return numero_telephone.text

def if_no_expert(): # À corriger.
    if infos_nom_expertise.find_all("p") is None:
        return ""
    else:
        list = []
        for expertises in infos_nom_expertise.find_all("p"):
            list.append(expertises.get_text().strip())
        return str(list).replace(",", "|")



with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)
    creation_fichier.writerow(["Université", "Prénom et nom", "Département", "Poste du prof", "Genre du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])

    for i in range(0,5):
        url = f"http://www.inrs.ca/les-professeurs/liste/all?page={i}"
        #print(url)
        contenu = requests.get(url,headers=entete)
        n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
        page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
        tableau_prof = page.find("div", id="profs_table_in")
        section_prof = tableau_prof.find("tbody").find_all("tr")


        #Ici je suis à la première page et je veut accéder aux différents départements.
        for fiche_prof in section_prof:
            if fiche_prof.find("a") is not None:
                lien_prof = fiche_prof.find("a")["href"]#Trouver le lien qui mènent vers les départements
                url_prof = "http://www.inrs.ca" + lien_prof[lien_prof.rfind("/"):]
                #print(url_prof)
                #Ici je suis dans la page des différents professeurs.
                contenu2 = requests.get(url_prof,headers=entete) #Accéder à la page
                page_prof = BeautifulSoup(contenu2.text, "html.parser") #Lire la page
                n += 1
                infos_nom_expertise = page_prof.find("div", id="finfos_title")
                coordonees = page_prof.find("div", id="finfos_gen")
                #print("<>" * 40)
                universite = "Institut national de la recherche scientifique"

                #Nom ---
                nom_du_prof = infos_nom_expertise.find("h1").text
                #print(nom_du_prof)

                #Poste --- Non/existant
                poste = "Professeur"
                #image = "http://www.inrs.ca" + page_prof.find("div", id="fp_photo").find("img")["src"]
                #print(image)

                #DÉTERMINER LE SEXES
                prenom = nom_du_prof[0:nom_du_prof.find(" ")]
                genre = trouver_sexe_prof(prenom) ### My Ali a changer.
                
                #Departement ---
                departement = coordonees.find("a").text
                #print(departement)

                #Numero de téléphone --
                numero_telephone = page_prof.find("li", class_="profil-telephone")
                num = trouver_telephone_prof(numero_telephone)

                #Courriel
                adresse_courriel = page_prof.find("li", class_="profil-courriel")
                courriel = trouver_courriel_prof(adresse_courriel)
                
                #expertise ---
                expert = if_no_expert()
                    #print(expert)

#                print(n, "Le petit train travaille...")
                infos = [universite, nom_du_prof,departement, poste, genre, courriel, num, expert, url_prof]
                print(infos)
                creation_fichier.writerow(infos)

    url2 = "http://www.inrs.ca/les-professeurs/associes-invites"
    contenu3 = requests.get(url2,headers=entete)
    n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
    page2 = BeautifulSoup(contenu3.text,"html.parser") #pour analyser le code html
    #print(page2)
    donnees = page2.find("table").find_all("tr")
    for elements in donnees:
        
        print("<>" * 40)
        universite = "Institut national de la recherche scientifique"

        #Prenom et nom du / de la prof.e --->
        if "," in elements.contents[0].text:
            nom_prenom = elements.contents[0].text
            prenom0 = nom_prenom[nom_prenom.find(",")+1:].strip()
            #print(prenom0)
            nom = nom_prenom[0:nom_prenom.find(",")].strip()
            prenom_nom = prenom0 + " " + nom
            #print(prenom_nom)     
            
            #DÉTERMINER LE SEXE --->
            if " " in prenom0:
                prenom = prenom0[0:prenom0.find(" ")]
            else:
                prenom = prenom0
            genre2 = trouver_sexe_prof(prenom)
            #print(genre2)

            #departement --->
            if not "Centre" in elements.contents[2].text:
                departement = elements.contents[2].text
                #print(departement)
            
            #Poste --->
            poste = "Professeur associé"

            #Courriel ; numéro de téléphone ; 
            courriel = ""
            num = ""
            expert = ""
            url_prof = ""
                # 
                # print(lien_fiche_prof)        
                
                
                
            infos = [universite, prenom_nom, departement, poste, genre2, courriel, num, expert, url_prof]
            print(infos)
            creation_fichier.writerow(infos)