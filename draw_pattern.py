# %%
from enum import Enum
print ("coucou")

# %%
class Maille(Enum):
    AUCUNE = 0
    SIMPLE_FONTURE = 1
    DOUBLE_FONTURE = 2

class Rang():
    rang = list[Maille] # l'index donne la position de la maille, le type donne la maille

class PatronDroit:
    patron = list[Rang] # liste de rang
    echantillon_10cm = dict() # nb maille pour 10 cm et nb rang pour 10 cm

    def __init__(self, nb_maille_10cm, nb_rang_10cm):
        self.echantillon_10cm["nb_maille_10cm"] = nb_maille_10cm
        self.echantillon_10cm["nb_rang_10cm"] = nb_rang_10cm

    def ajouter_patron_symetrique_cm(self, largeur_bas_cm, hauteur_cm, largeur_haut_cm):
        # TODO
        # - rajouter la gestion des points (cote ou jersey)
        # - rajouter la gestion d'un rabat de maille obligatoire (ex rabattre 5 mailles au début)

        # traduction cm -> maille et rang
        largeur_bas_maille = round(largeur_bas_cm * self.echantillon_10cm["nb_maille_10cm"] / 10 )
        largeur_haut_maille = round(largeur_haut_cm * self.echantillon_10cm["nb_maille_10cm"] / 10 )
        if largeur_bas_maille % 2 == 1:
            print(f"INFO: nombre de mailles en bas pas symétrique ({largeur_bas_maille})")
            largeur_bas_maille +=1
        if largeur_haut_maille % 2 == 1:
            print(f"INFO: nombre de mailles en haut pas symétrique ({largeur_haut_maille})")
            largeur_haut_maille += 1

        max_maille = max(largeur_haut_maille, largeur_bas_maille)

        hauteur_rang = round(hauteur_cm * self.echantillon_10cm["nb_rang_10cm"] / 10 )
        if hauteur_rang % 2 == 1:
            print(f"INFO: nombre de rang impaire ({hauteur_rang})")
            hauteur_rang += 1

        # calculer et répartir les diminusions / augmentations
        nb_operations = abs(largeur_haut_maille - largeur_bas_maille) / 2
        nb_rangs = hauteur_rang / 2 - 2

        quotient, reste = divmod(nb_operations, nb_rangs)
        repartition = [quotient] * nb_rangs
        for i in range(reste):
            repartition[i * nb_rangs // reste] += 1

        # ranger ça dans le patron
        patron_courant = list(Rang)
        rang_initial = [Maille(0)] * max_maille
        for r in range(hauteur_rang - 2):
            print("coucou il faut continuer")





