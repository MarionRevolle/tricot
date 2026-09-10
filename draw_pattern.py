from enum import Enum


class Maille(Enum):
    AUCUNE = 0
    SIMPLE_FONTURE = 1
    DOUBLE_FONTURE = 2


class Point(Enum):
    JERSEY = 0  # maille tout le temps simple fonture
    SIMPLE_COTE = (
        1  # alternance des mailles 1 sur la simple fonture / 1 sur la double fonture
    )
    DOUBLE_COTE = (
        2  # alternance des mailles : 2 sur la simple fonture / 2 sur la double fonture
    )


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
        self.nb_aiguilles = 200
        self.operations: list[
            tuple[int, int]
        ] = []  # (operation gauche, operation droite)
        self.nb_maille_depart = 0

    def to_csv(self, nom_fichier: str):
        with open(nom_fichier, "w") as f:
            for i, partie in enumerate(reversed(self.patron)):
                for rang in reversed(partie):
                    f.write(
                        ",".join(
                            ["" if maille == Maille.AUCUNE else "V" for maille in rang]
                        )
                    )
                    f.write("\n")

    def largeur_cm_en_maille(self, largeur_cm: float) -> int:
        return round(largeur_cm * self.echantillon_10cm["nb_maille_10cm"] / 10)

    def hauteur_cm_en_rang(self, hauteur_cm: float) -> int:
        return round(hauteur_cm * self.echantillon_10cm["nb_rang_10cm"] / 10)

    def ajouter_trapeze(
        self,
        largeur_bas_cm: float,
        hauteur_cm: float,
        largeur_haut_cm: float,
        rabat_de_maille: int = 0,
    ):

        # TODO
        # - rajouter la gestion des points (cote ou jersey), pour le moment
        #   tout jersey
        # - réparer commencer et finir tout de suite, pour le moment c'est cassé

        # traduction cm -> maille et rang
        largeur_bas_maille = self.largeur_cm_en_maille(largeur_bas_cm)
        largeur_haut_maille = self.largeur_cm_en_maille(largeur_haut_cm)
        if largeur_bas_maille % 2 == 1:
            print(
                f"INFO: nombre de mailles en bas pas symétrique ({largeur_bas_maille})"
            )
            largeur_bas_maille += 1

        largeur_bas_maille -= rabat_de_maille * 2
        if largeur_haut_maille % 2 == 1:
            print(
                f"INFO: nombre de mailles en haut pas symétrique ({largeur_haut_maille})"
            )
            largeur_haut_maille += 1

        hauteur_rang = self.hauteur_cm_en_rang(hauteur_cm)
        if hauteur_rang % 2 == 1:
            print(f"INFO: nombre de rang impaire ({hauteur_rang})")
            hauteur_rang += 1

        # calculer et répartir les diminussions / augmentations
        nb_operations = round((largeur_haut_maille - largeur_bas_maille) / 2)

        nb_rangs = round(hauteur_rang / 2)

        quotient, reste = divmod(nb_operations, nb_rangs)
        if abs(quotient) >= 2:
            print(
                f"WARNING: attention il va y avoir de très grosses augmentations/diminussions ({quotient})"
            )
        repartition = [int(quotient)] * nb_rangs
        for i in range(int(reste)):
            repartition[i * nb_rangs // reste] += 1

        # ranger ça dans le patron

        milieu = int(self.nb_aiguilles / 2)
        patron_courant: list[Rang] = []

        # rang avec les operations
        for r in range(nb_rangs):
            nb_mailles = largeur_bas_maille + sum(repartition[0 : r + 1]) * 2
            rang_courant = [Maille.AUCUNE] * self.nb_aiguilles
            rang_courant[
                milieu - int(nb_mailles / 2) : milieu + int(nb_mailles / 2)
            ] = [Maille.SIMPLE_FONTURE] * nb_mailles
            patron_courant.append(rang_courant)
            patron_courant.append(rang_courant)

        self.patron.append(patron_courant)
