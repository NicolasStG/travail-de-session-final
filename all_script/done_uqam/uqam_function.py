def trouver_nom_du_prof(nom_du_prof):
    if nom_du_prof is None:
        return ""
    else:
        return nom_du_prof.text.strip()

def trouver_departement_prof(departement_prof):
    if departement_prof is None:
        return ""
    else:
        return departement_prof.find("a").text

def trouver_poste_prof(poste_prof):
    if poste_prof is None:
        return ""
    else:
        return poste_prof.text

def determiner_sex(sexe_prof):
    #Section femmme ---->
    if sexe_prof == "Professeure": #or "Vice-doyenne" or "Doyenne" or "Rectrice" or "Vice-rectrice":
        return "femme"
    elif sexe_prof == "Vice-doyenne":
        return "femme"
    elif sexe_prof == "Doyenne":
        return "femme"
    elif sexe_prof == "Rectrice":
        return "femme"
    elif sexe_prof == "Vice-rectrice":
        return "femme"
    
    #Section homme ---->
    elif sexe_prof == "Professeur": #or "Vice-doyen" or "Doyen" or "Recteur" or "Vice-recteur":
        return "homme"
    elif sexe_prof == "Vice-doyen":
        return "homme"
    elif sexe_prof == "Doyen":
        return "homme"
    elif sexe_prof == "Recteur":
        return "homme"
    elif sexe_prof == "Vice-recteur":
        return "homme"
    
    #Autre ---> Maître ou Chargée
    else:
        return "impossible à déterminer"



def trouver_courriel_prof(courriel_prof):
    if courriel_prof is None:
        return ""
    else : 
        return courriel_prof.find("a").text

def trouver_telephone_prof(telephone_prof):
    if telephone_prof is None:
        return ""
    else :
        return telephone_prof[telephone_prof.find(":")+2:].strip()

def trouver_expertise(expertise):
   if expertise:
       if ',' in expertise.find("ul").get_text():
         return "|".join(expertise.find("ul").text.split(",")).replace(".","")
       else:
         return str(expertise.find("ul").text).replace("\n", "|")
   else:
       return ""

def parler_ou_non_media(entretenir_media):
    if entretenir_media is None:
        return ""
    else:
        return entretenir_media.text