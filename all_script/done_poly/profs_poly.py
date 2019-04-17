# # coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "profs_poly.csv"

entete = {
    "User-Agent":"Nicolas St-Germain - 438/492-2926 : Étudiant en journalisme à L'UQAM",
    "From":"niikostg@gmail.com"
}

def trouver_depart():
	if len(departement_poste.find_all("a")) == 3:
		try:
			departement = departement_poste.find_all("a")[2].text
			return departement
		except IndexError:
			return
	else:
		if len(departement_poste.find_all("a")) == 2: 
			try:
				departement = departement_poste.find_all("a")[1].text
				return departement
			except IndexError:
				return
		else:
			if len(departement_poste.find_all("a")) == 1:
				try:	
					departement = departement_poste.find("a").text
					return departement
				except IndexError:
					return

def trouver_poste():
	if len(departement_poste.find_all("strong")) == 3:
		try:
			poste = departement_poste.find_all("strong")[-1].text
			return poste
		except IndexError:
			return
	else:
		if len(departement_poste.find_all("strong")) == 2: 
			try:
				poste = departement_poste.find_all("strong")[-1].text
				return poste
			except IndexError:
				return
		else:
			if len(departement_poste.find_all("strong")) == 1:
				try:	
					poste = departement_poste.find("strong").text
					return poste
				except IndexError:
					return

def trouver_expertise():
	if champ_expertise is None:
		return ""
	else:
		list = []
		for domaine in champ_expertise.find_all("span"):
			list.append(domaine.get_text())
		domaine_expertise = str(list).replace(",", "|")
		return domaine_expertise

def trouver_sexe():
	if sexe_prof == "Professeure":
		return 'femme'
	elif sexe_prof == "Professeur":
		return 'homme'
	elif sexe_prof == "Maître":
		return "impossible à déterminer"


with open(fichier,"w") as f2:
	creation_fichier = csv.writer(f2,)
	creation_fichier.writerow(["Université", "Prénom et nom", "Genre du prof","Département", "Poste du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])
	for i in range (0,16):
		url = f"https://www.polymtl.ca/expertises/recherche/expertises?page={i}&f%5B0%5D=bundle%3Afiche_expert"
		contenu = requests.get(url,headers=entete)
		n = 0 #permet de garder le track quand le code roule, être certain que tout va bien.
		#print(url)
		page = BeautifulSoup(contenu.text,"html.parser") #pour analyser le code html
		div_fiche_complete = page.find("div", class_="search-results-wrapper")
		fiche_complete = div_fiche_complete.find_all("div", class_="search-result")

		for fiche in fiche_complete:
			lien_fiche = fiche.find("div", class_="fiche-complete shown-md").find("a")["href"]
			#print(lien_fiche)
			contenu2 = requests.get(lien_fiche,headers=entete)
			page_prof = BeautifulSoup(contenu2.text,"html.parser") #pour analyser le code html
			print("<>"*40)
			universite = "Polytechnique"
			informations = page_prof.find("div", class_="encadre-fiche-expert")

			#Nom de l'enseignant.e --->
			nom_du_prof = informations.find("div",class_="nom-expert").text.strip()
			#print(nom_du_prof)

			departement_poste = informations.find("div", class_="fiche-expert-resume-titre")
			
			#Département --->
			#print(len(departement_poste.find_all("a")))
			depart = trouver_depart()
			#print(trouver_depart())
			
			#Poste --->
			#print(len(departement_poste.find_all("strong")))
			#print(trouver_poste())
			if "," in trouver_poste():
				poste_prof = trouver_poste()[0:trouver_poste().find(",")]
			else:
				poste_prof = trouver_poste()
			#print(poste_prof)

			#Genre --->
			sexe_prof = poste_prof[0:poste_prof.find(" ")]
			genre_prof = trouver_sexe()
			#print(sexe_prof)
			#print(genre_prof)

			coordonnes = informations.find("div", class_="fiche-expert-resume-coordonnees")
			#Courriel --->
			courriel_ad = coordonnes.find("a").text.strip()
			#print(courriel_ad)

			#Téléphone --->
			for num_telelephone in coordonnes.find_all("span"):
				#print(num_telelephone.get_text())
				if num_telelephone.get_text().split()[0] in ["Tél."]:
					num_tel = num_telelephone.get_text()
					num = num_tel[num_tel.find(":")+2:].strip()
					#print(num)

			#Champ d'expertise --->
			champ_expertise = informations.find("div", class_="fiche-expert-resume-expertises")
			expert = trouver_expertise()

			infos = [universite, nom_du_prof, genre_prof, depart, poste_prof, courriel_ad, num, expert, lien_fiche]
			print(infos)
			creation_fichier.writerow(infos)

###### EFFACER LES CHERCHEURS ET CHERCHEUSES #######
##FAIRE LES IMPOSSIBLE À DÉTERMINER À LA MAIN (21) ##