import csv
import requests
from bs4 import BeautifulSoup

fichier = "teluq_prof.csv"


def if_no_value(results):
    if labo_stage is not None:
        try:
            idx_1 = [i for i, r in enumerate(results) if r.name == "h2"][3]
            idx_2 = [i for i, r in enumerate(results) if r.name == "h2"][4]
        except AttributeError:
            return
    else:
        if affiliation is not None :
            try:
                idx_1 = [i for i, r in enumerate(results) if r.name == "h2"][2]
                idx_2 = [i for i, r in enumerate(results) if r.name == "h2"][3]
            except IndexError:
                return
        else:
            if formation is not None:
                try:
                    idx_1 = [i for i, r in enumerate(results) if r.name == "h2"][1]
                    idx_2 = [i for i, r in enumerate(results) if r.name == "h2"][2]
                except IndexError:
                    return
            elif formation is None:
                try:
                    idx_1 = [i for i, r in enumerate(results) if r.name == "h2"][0]
                    idx_2 = [i for i, r in enumerate(results) if r.name == "h2"][1]
                except IndexError:
                    return
    expertises = [r for i, r in enumerate(results) if idx_1 < i < idx_2]
    return expertises

def value_sexe(sexe):
    if sexe == "Professeure":
        return "femme"
    elif sexe == "Professeur":
        return "homme"

def if_no_depart(departement):
    if departement is None:
        return ""
    else:
        return departement.text

def if_no_courriel(courriel_prof):
    if courriel_prof is None:
        return ""
    else:
        return courriel_prof.find("a").text

def if_no_tel(numero_telephone):
    if numero_telephone is None:
        return ""
    else:
        return numero_telephone.text

def if_no_poste(poste):
    if poste is None:
        return ""
    else:
        return poste.strip().strip(",")

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

url = "https://www.teluq.ca/siteweb/univ/professeurs.html"
contenu = requests.get(url,headers=entete)
n = 0
page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
liste_prof = page.find("div", class_="boite_1")
list_prof = liste_prof.find_all("li")

with open(fichier,"w") as f2:
    creation_fichier = csv.writer(f2,)
    creation_fichier.writerow(["Université", "Prénom et nom", "Département", "Poste du prof", "Genre du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])
    for prof in list_prof:
        href = prof.find("a")["href"]
        lien_prof = "https://www.teluq.ca/siteweb/univ/" + href

        #Ici je suis dans la page des professeur.e.s.
        contenu2 = requests.get(lien_prof,headers=entete) #Accéder à la page
        page_prof = BeautifulSoup(contenu2.text, "html.parser") #Lire la page
        print("<>" * 40)
        n +=1
        universite = "Université TÉLUQ"

        #Nom du / de la professeur.e
        nom_du_prof = page_prof.find("h1", class_="titrePage").text
        prof_nom = nom_du_prof[nom_du_prof.find(";")+1:]
        #print(prof_nom)

        #Département du / de la prof.e 
        div_depart_poste = page_prof.find("div", class_="infosGen")
        departement = div_depart_poste.find("a")
        type_departement = if_no_depart(departement)
        #print(departement)

        #Poste du / de la prof.e 
        poste = div_depart_poste.find("p").contents[0].strip().strip(",")
        type_poste = if_no_poste(poste)
        #print(poste)

        #Sexe du / de la prof.e --->
        if " " in poste:
            sexe = poste[0:poste.find(" ")]
        else:
            sexe = poste
        genre = value_sexe(sexe)
        #print(genre)
        
        #Courriel et numéro de téléphone du / de la prof.e
        courriel_numero_prof = page_prof.find("div", class_="boite_2 add-d-bottom")
        courriel_prof = courriel_numero_prof.find("p", class_="add-d-bottom")
        adresse_courriel = if_no_courriel(courriel_prof)
        #print(courriel_prof)

        numero_telephone = courriel_numero_prof.find("span", attrs={"itemprop":"telephone"})
        telephone = if_no_tel(numero_telephone)
        #print(numero_telephone)

        #Champs d'expertise.
        div_expert = page_prof.find("div", id="ProfilProf")
        results = div_expert.find_all(["h2", "p", "ul"])
        champ_expertise = div_expert.find("h2", text="Champs d'expertise")
        labo_stage = div_expert.find("h2", text="Laboratoire") and div_expert.find("h2", text="Étudiants et stagiaires")
        formation = div_expert.find("h2", text="Formation")
        affiliation = div_expert.find("h2", text="AFFILIATION PROFESSIONNELLE") or div_expert.find("h2", text="Affiliations") or div_expert.find("h2", text="Affiliation professionnelle")
        if champ_expertise is None:
            elem = ""
        else:
            for domaine_expertise in if_no_value(results):
                elements = "".join(domaine_expertise.get_text().strip())
                elem = str(elements).replace("\n", "|").strip()
            #Il est nécessaire après avoir roulé le code de nettoyer certains trucs et d'ajouter des < | > entre les expertises de Joëlle Basque (3e en partant du haut)
            ## Avec la méthode pour certains profs, leurs expertises se répêtent.

            #print(n, "Le petit train travaille...")
        infos = [universite, prof_nom, type_departement, type_poste, genre, adresse_courriel, telephone, elem, lien_prof]
        print(infos)
        creation_fichier.writerow(infos)