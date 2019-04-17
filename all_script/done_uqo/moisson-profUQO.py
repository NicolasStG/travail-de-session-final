#coding: utf-8

import json
import csv
import requests
from bs4 import BeautifulSoup 

entete = {
	"User-Agent":"Stéphanie Prévost - 438-777-4252. Je fais un moissonnage de donnée dans le cadre d'un cours universitaire en journalisme de données.",
	"From":"stephanie-prevost@hotmail.ca"
}

fichier = "UQO_PROF.csv"
f2 = open(fichier,"w")
csvOutput = csv.writer(f2)
csvOutput.writerow(["université", "nom", "ville", "pavillon", "domaine", "spécialisation", "num Téléphone","courriel", "url"])

lettre_dic = {
	"DPP" : "Département de psychoéducation et de psychologie",
	"DRI" : "Département de relations industrielles",
	"DTS" : "Département de travail social",
	"DSA" : "Département des sciences administratives",
	"DCTB" : "Département des sciences comptables",
	"DSE" : "Département des sciences de l'éducation",
	"DSI" : "Département des sciences infirmières",
	"DSN" : "Département des sciences naturelles",
	"DSSO" : "Département des sciences sociales",
	"DEL" : "Département d'études langagières",
	"DII" : "Département d'informatique et d'ingénierie",
	"EMI" : "École multidisciplinaire de l'image"
}

university = "Université du Québec en Outaouais"

def parsePage(nom, lettre, liens_fiche_prof):

	contenu2=requests.get(liens_fiche_prof, headers=entete)

	page_suite = BeautifulSoup(contenu2.text,"html.parser") 

	infos_profs = page_suite.find("div", id="divInfoProf")
	if infos_profs != None:

		#informations des profs:

		pavillonHTML = infos_profs.find("div", id="divBureau")
		if pavillonHTML != None:
			pavillon = pavillonHTML.find("span", id="lblNomPavillon").text
		else:
			pavillon = ""

		if pavillon == "Campus de Saint-Jérôme":
			ville = "Saint-Jérôme"
		else:
			ville = "Gatineau"

		courrielHTML = infos_profs.find("a", id="lnkCourriel")
		if courrielHTML != None:
			courriel = courrielHTML.text
		else:
			courriel = ""

		domaineHtml = infos_profs.find("a", id="linkDepartement")
		if domaineHtml != None:
			domaine = domaineHtml.find("span", id="lblDepartement").text
		else:
			domaine = ""

		specialisationHTML = infos_profs.find("div", id="divSpec")
		if specialisationHTML != None:
			listDeLi = specialisationHTML.find("ul", id="lstSpec").find_all("li")
			def getText(li):
				return li.text
			listDeSpecialisation = map(getText, listDeLi)
			specialisation = "| ".join(listDeSpecialisation)
		else:
			specialisation = ""

		nbTelHTML = infos_profs.find("span", id="lblNoTel")
		if nbTelHTML != None:
			nbTel = nbTelHTML.text
		else:
			nbTel = ""

		infos = [university, prenom_nom, ville, pavillon, domaine, specialisation, nbTel, courriel, liens_fiche_prof]
		print(infos)
		csvOutput.writerow(infos)
	else:
		infos = [university, prenom_nom, "", "", lettre_dic.get(lettre), "", "", "", ""]
		csvOutput.writerow(infos)


for lettre in lettre_dic:
	url = "http://apps.uqo.ca/DosEtuCorpsProf/AffDepartement.aspx?dep={}&onglet=p".format(lettre)

	contenu = requests.get(url,headers=entete)
	print("<>"*40)
	page=BeautifulSoup(contenu.text,"html.parser") 

	#prof:

	profs=page.find("table", id="lstProf").find_all("tr")

	for prof in profs:

		url_Prof = prof.find_all("a")[1]["href"]

		liens_fiche_prof = "http://apps.uqo.ca/DosEtuCorpsProf/" + url_Prof

		nom = prof.find_all("a")[1].text
		nom_famille = nom[0:nom.find(",")]
		prenom = nom[nom.find(",")+2:]
		prenom_nom = prenom + " " + nom_famille
		#print(prenom_nom) 

		parsePage(nom, lettre, liens_fiche_prof)

	#prof asssocié:

	div_profs_asso=page.find("div", id="divProfAssoc")
	if div_profs_asso != None:
		
		profs_asso = div_profs_asso.find_all("tr")
		
		for prof_asso in profs_asso:

			span_nom = prof_asso.find("span")
			url_Prof = span_nom.find("a") 
			nom = span_nom.text
			nom_famille = nom[0:nom.find(",")]
			prenom = nom[nom.find(",")+2:]
			prenom_nom = prenom + " " + nom_famille

			if url_Prof == None:
				#print(nom)
				csvOutput.writerow([university, prenom_nom, "", "",lettre_dic.get(lettre), "", "", "", ""])
			else:
				liens_fiche_prof = url_Prof["href"]
				bon_lien = "http://apps.uqo.ca/DosEtuCorpsProf/"
				if  bon_lien in liens_fiche_prof:
					# nom_famille = url_Prof[0:url_Prof.find(",")]
					# prenom = url_Prof[url_Prof.find(",")+2:]
					# prenom_nom = prenom + " " + nom_famille
					parsePage(prenom_nom, lettre, liens_fiche_prof)
				else:
					# nom_famille = url_Prof[0:url_Prof.find(",")]
					# prenom = url_Prof[url_Prof.find(",")+2:]
					# prenom_nom = prenom + " " + nom_famille
					#print(url_Prof.text)
					csvOutput.writerow([university, prenom_nom,"", "", lettre_dic.get(lettre), "", "", "", ""])

	#prof honoraire:
	div_profs_honor=page.find("div", id="divProfHonor")
	if div_profs_honor != None:
		
		profs_honor = div_profs_honor.find_all("tr")
		
		for prof_honor in profs_honor:

			span_nom =prof_honor.find("span")
			url_Prof = span_nom.find("a")
			nom = span_nom.text
			nom_famille = nom[0:nom.find(",")]
			prenom = nom[nom.find(",")+2:]
			prenom_nom = prenom + " " + nom_famille

			if url_Prof == None:
				#print(nom)
				csvOutput.writerow([university, prenom_nom, "", "", lettre_dic.get(lettre),"", "", "", ""])
			else:
				liens_fiche_prof = url_Prof["href"]
				bon_lien = "http://apps.uqo.ca/DosEtuCorpsProf/"
				if bon_lien in liens_fiche_prof:
					# nom_famille = url_Prof[0:url_Prof.find(",")]
					# prenom = url_Prof[url_Prof.find(",")+2:]
					# prenom_nom = prenom + " " + nom_famille
					parsePage(prenom_nom, lettre, liens_fiche_prof)
				else:
					# nom_famille = url_Prof[0:url_Prof.find(",")]
					# prenom = url_Prof[url_Prof.find(",")+2:]
					# prenom_nom = prenom + " " + nom_famille
					#print(url_Prof.text)
					csvOutput.writerow([university, prenom_nom,"", "", lettre_dic.get(lettre), "", "", "", ""])

##### RETIRER LE PROF ÉMÉRITE DU CSV ######
		
