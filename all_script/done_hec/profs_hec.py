# # coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

fichier = "profs_hec.csv"

entete = {
	"User-Agent": "Olivier Faucher - requête acheminée dans le cadre d'un cours de journalisme de données",
	"From":"faucher.olivier@courrier.uqam.ca"
	}

def genre_prof_type(sexe):
	if sexe == "Professeure":
		return "femme"
	if sexe == "Professeur":
		return "homme"
	if sexe == "Maître":
		return "impossible à déterminer"

def determiner_expert_prof(champ_expertise):
	if champ_expertise is None:
		return ""
	else:
		expertises = champ_expertise.find_next("ul").text.strip()
		return expertises

url = "https://www.hec.ca/profs/"
contenu = requests.get(url,headers=entete)
page = BeautifulSoup(contenu.text.encode("latin-1").decode("utf-8"),"html.parser")
departements = page.find("div", id="br-123383").find_next("ul").find_all("li")

with open(fichier,"w") as f2:
	creation_fichier = csv.writer(f2,)
	creation_fichier.writerow(["Université", "Prénom et nom", "Département", "Poste du prof", "Genre du prof", "Email", "Numéro de téléphone", "Champs d'expertises", "Lien vers le prof"])

	for departement in departements:
		lien_depart = departement.find("a")["href"] #trouver le lien de chaque département
		acces = requests.get(lien_depart,headers=entete) #Accéder à la page
		page_départ = BeautifulSoup(acces.text, "html.parser") #Lire la page

		#Arrivé(e)s sur la page d'un département!
		section_profs = page_départ.find("div", class_="ALBOfProfs") #Section des profs
		professeurs = section_profs.find_all("div", class_="row") #trouver les profs

		#Accéder à la page prof
		for professeur in professeurs:
			lien_page_prof = professeur.find("div", class_="col-sm-4").find("a")["href"]
			#print(lien_page_prof)
			acces_prof = requests.get(lien_page_prof,headers=entete)
			page_prof = BeautifulSoup(acces_prof.text.encode("latin-1").decode("utf-8"), "html.parser")
		
			#Arrivé(e)s sur la page du prof!
			if not "Attaché" in page_prof.find("h2", class_="hTypeMenu proftitledepart").text:
				
				print("<>"*40)

				#Créer la colonne qui nomme le HEC
				universite = "HEC Montréal"

				#Rammasse le nom du prof
				section_info = page_prof.find("div", class_="container", id="LeContenu")
				nom_prof2 = section_info.find("h1").text
				

				#Poste du Professeur ou de la Professeure -->
				poste = section_info.find("h2").text
				poste_prof = poste.split(",")[0]
				

				#Sexe du / de la prof.e
				if " " in poste_prof:
					sexe = poste_prof[0:poste_prof.find(" ")]
				else :
					sexe = poste_prof
				genre_prof = genre_prof_type(sexe)

				#Rammasse le département
				departement = section_info.find("h2").text 
				departement2 = departement.split(",")
				departement3 = departement2[1].strip()
				#print(departement3)


				#Rammasse Le courriel
				courriel = section_info.find("div", class_="col-sm-4")
				courriel2 = courriel.find("a", class_="hTypeMenu").text
				#print(courriel2)


				#Rammasse le numéro de téléphone
				tel = courriel.find_all("a", class_="hTypeMenu")[1].text
				#print(tel)


				#Rammasse l'expertise
				exp = section_info.find("div", class_="col-sm-8")
				#print(exp.text)
				#h3 = exp.find_all("h3")
				champ_expertise = exp.find("h3", text=" Expertise ")
				champ_expert = str(determiner_expert_prof(champ_expertise)).replace("\n", "|").replace("\r","")

				infos = [universite, nom_prof2, departement3, poste_prof, genre_prof, courriel2, tel, champ_expert, lien_page_prof]
				print(infos)
				creation_fichier.writerow(infos)




		

		


