#coding: utf-8

import json
import csv
import requests
from bs4 import BeautifulSoup 

entete = {
	"User-Agent":"Stéphanie Prévost - 438-777-4252. Je fais un moissonnage de donnée dans le cadre d'un cours universitaire en journalisme de données.",
	"From":"stephanie-prevost@hotmail.ca"
}

fichier = "Bishop_PROF.csv"
f2 = open(fichier,"w")
csvOutput = csv.writer(f2)
csvOutput.writerow(["université", "titre", "prénom et nom", "domaine", "courriel", "num Téléphone", "url"])

for lettreOrd in range(ord("A"), ord("Z")+1):
	lettre = chr(lettreOrd)
	url = "https://www.ubishops.ca/bu-directory/char/{}".format(lettre)

	contenu = requests.get(url,headers=entete)
	page=BeautifulSoup(contenu.text,"html.parser") 
	profs=page.find_all("div", attrs={"data-entry-type":"individual"})

	for prof in profs:
		university = "Bishop university"

		titleHtml = prof.find("span", class_="title")
		if titleHtml is None:
			title = ""
		else:
			title = titleHtml.text

		prenom = prof.find("span", class_="given-name").text
		nom = prof.find("span", class_="family-name").text
		prenom_nom = prenom + " " + nom 
		
		domaineHtml = prof.find("span", class_="organization-unit")
		if domaineHtml is None:
			domaine = ""
		else:
			domaine = domaineHtml.text

		courrielHTML = prof.find("span", class_="email-address")
		if courrielHTML is None:
			courriel = ""
		else:
			courriel = courrielHTML.find("a").text

		nbTelHTML = prof.find("span", class_="tel")
		if nbTelHTML is None:
			nbTel = ""
		else:
			nbTel = nbTelHTML.find("span", class_ = "value").text
		
		# print([university, title, prenom, nom, domaine, courriel, nbTel, url])
		infos = [university, title, prenom_nom, domaine, courriel, nbTel, url]
		print("<>"*40)
		print(infos)
		csvOutput.writerow(infos)

# Le document contient tout le personnel de l'école et possiblement plus. Il faudra nettoyer le dossier avant de l'utiliser.