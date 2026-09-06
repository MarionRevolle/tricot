from enum import Enum


class Maille(Enum):
    AUCUNE = 0
    SIMPLE_FONTURE = 1
    DOUBLE_FONTURE = 2


class Rang:
    # l'index donne la position de la maille, le type donne la maille
    rang: list[Maille]


class PatronDroit:
    def __init__(self, nb_maille_10cm: int, nb_rang_10cm: int):
        self.patron: list[list[Rang]] = []
        self.echantillon_10cm: dict[str, int] = {
            "nb_maille_10cm": nb_maille_10cm,
            "nb_rang_10cm": nb_rang_10cm,
        }

    def ajouter_patron_symetrique_en_cm(
        self,
        largeur_bas_cm: float,
        hauteur_cm: float,
        largeur_haut_cm: float,
    ):

        # TODO
        # - rajouter la gestion des points (cote ou jersey), pour le moment
        #   tout jersey
        # - rajouter la gestion d'un rabat de maille obligatoire au début
        #   (ex rabattre 5 mailles au début)
        # - rajouter si on commence tout de suite par l'operation ou alors si
        #   on attend 1 double rang aller retour pareil pour la fin

        # traduction cm -> maille et rang
        largeur_bas_maille = round(
            largeur_bas_cm * self.echantillon_10cm["nb_maille_10cm"] / 10
        )
        largeur_haut_maille = round(
            largeur_haut_cm * self.echantillon_10cm["nb_maille_10cm"] / 10
        )
        if largeur_bas_maille % 2 == 1:
            print(
                f"INFO: nombre de mailles en bas pas symétrique ({largeur_bas_maille})"
            )
            largeur_bas_maille += 1
        if largeur_haut_maille % 2 == 1:
            print(
                f"INFO: nombre de mailles en haut pas symétrique ({largeur_haut_maille})"
            )
            largeur_haut_maille += 1

        hauteur_rang = round(hauteur_cm * self.echantillon_10cm["nb_rang_10cm"] / 10)
        if hauteur_rang % 2 == 1:
            print(f"INFO: nombre de rang impaire ({hauteur_rang})")
            hauteur_rang += 1

        # calculer et répartir les diminussions / augmentations
        nb_operations = (largeur_haut_maille - largeur_bas_maille) / 2
        nb_rangs = hauteur_rang / 2 - 2

        quotient, reste = divmod(nb_operations, nb_rangs)
        if abs(quotient) >= 2:
            print(
                f"WARNING: attention il va y avoir de très grosses augmentations/diminussions ({quotient})"
            )
        repartition = [quotient] * nb_rangs
        for i in range(reste):
            repartition[i * nb_rangs // reste] += 1

        # ranger ça dans le patron

        max_maille = max(largeur_haut_maille, largeur_bas_maille)
        milieu = max_maille / 2
        patron_courant: list[Rang] = list()

        # rang initial
        rang_initial = [Maille.AUCUNE] * max_maille
        rang_initial[
            milieu - largeur_bas_maille / 2 : milieu + largeur_bas_maille / 2
        ] = [Maille.SIMPLE_FONTURE] * largeur_bas_maille
        patron_courant.append(rang_initial)

        # rang avec les operations
        for r in range(nb_rangs):
            nb_mailles = largeur_bas_maille + repartition[r] * 2
            rang_courant = [Maille.AUCUNE] * max_maille
            rang_courant[milieu - nb_mailles / 2 : milieu + nb_mailles / 2] = [
                Maille.SIMPLE_FONTURE
            ] * nb_mailles
            patron_courant.append(rang_courant)

        # rang final
        rang_final = [Maille.AUCUNE] * max_maille
        rang_final[
            milieu - largeur_haut_maille / 2 : milieu + largeur_haut_maille / 2
        ] = [Maille.SIMPLE_FONTURE] * largeur_haut_maille
        patron_courant.append(rang_final)

        self.patron.append(patron_courant)
