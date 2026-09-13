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
        self.echantillon_10cm: dict[str, int] = {
            "nb_maille_10cm": nb_maille_10cm,
            "nb_rang_10cm": nb_rang_10cm,
        }
        self.nb_aiguilles = 200
        self.operations: list[
            list[tuple[int, int]]
        ] = []  # (operation gauche, operation droite)
        self.points: list[Point] = []
        self.nb_maille_depart = 0

    def faire_un_rang(
        self,
        operation_droite: int,
        operation_gauche: int,
        point: Point,
        nb_mailles_depart: int,
    ) -> Rang:
        rang = [Maille.AUCUNE] * self.nb_aiguilles
        milieu = int(self.nb_aiguilles / 2)
        nb_mailles = nb_mailles_depart + operation_droite + operation_gauche

        if point == Point.JERSEY:
            rang[milieu - int(nb_mailles / 2) : milieu + int(nb_mailles / 2)] = [
                Maille.SIMPLE_FONTURE
            ] * nb_mailles
        elif point == Point.SIMPLE_COTE:
            for i in range(nb_mailles):
                if i % 2 == 0:
                    rang[milieu - int(nb_mailles / 2) + i] = Maille.SIMPLE_FONTURE
                else:
                    rang[milieu - int(nb_mailles / 2) + i] = Maille.DOUBLE_FONTURE
        elif point == Point.DOUBLE_COTE:
            for i in range(nb_mailles):
                if (i // 2) % 2 == 0:
                    rang[milieu - int(nb_mailles / 2) + i] = Maille.SIMPLE_FONTURE
                else:
                    rang[milieu - int(nb_mailles / 2) + i] = Maille.DOUBLE_FONTURE
        return rang

    def to_csv(self, nom_fichier: str):

        # ranger ça dans le patron
        patron: list[Rang] = []

        # rang avec les operations
        nb_mailles_depart = self.nb_maille_depart
        for partie, op in enumerate(self.operations):
            point = self.points[partie]
            for r, o in enumerate(op):
                rang = self.faire_un_rang(
                    o[0],
                    o[1],
                    point,
                    nb_mailles_depart,
                )
                patron.append(rang)
                patron.append(rang)
                nb_mailles_depart += o[0] + o[1]

        with open(nom_fichier, "w") as f:
            for rang in reversed(patron):
                f.write(
                    ",".join(
                        [
                            ""
                            if maille == Maille.AUCUNE
                            else "X"
                            if maille == Maille.SIMPLE_FONTURE
                            else "O"
                            for maille in rang
                        ]
                    )
                )
                f.write("\n")

    def __str__(self) -> str:
        print("aller on fait un truc intelligent pour afficher le patron")

        def trouver_quoi_ecrire(index: int) -> str:
            operation_courante = self.operations[index]
            if operation_courante[0] == 0 and operation_courante[1] == 0:
                print("trouver jusuq'à quand on fait du tout droit")
                return "tout droit"
            if abs(operation_courante[0]) > 1 and abs(operation_courante[1]) > 1:
                if operation_courante[0] > 0:
                    return f"Rajouter {operation_courante[0]} mailles à gauche et {operation_courante[1]} mailles à droite"
                else:
                    return f"Rabattre {operation_courante[0]} mailles à gauche et {operation_courante[1]} mailles à droite"
            else:
                if operation_courante[0] > 0:
                    print("Augmenter à une maille du bord tous les deux rangs")
                    print("TODO trouver le pattern")
                    return f"Rajouter {operation_courante[0]} maille à gauche et {operation_courante[1]} maille à droite"
                else:
                    print("Diminuer à une maille du bord tous les deux rangs")
                    return f"Rabattre {operation_courante[0]} maille à gauche et {operation_courante[1]} maille à droite"

        str = f"Montez {self.nb_maille_depart} mailles\n"

    def largeur_cm_en_maille(self, largeur_cm: float) -> int:
        return round(largeur_cm * self.echantillon_10cm["nb_maille_10cm"] / 10)

    def hauteur_cm_en_rang(self, hauteur_cm: float) -> int:
        return round(hauteur_cm * self.echantillon_10cm["nb_rang_10cm"] / 10)

    def ajuster_nb_mailles_fonction_point(self, nb_mailles: int, point: Point) -> int:
        if point == Point.SIMPLE_COTE and nb_mailles % 2 != 1:
            print(
                f"INFO: avec la simple côte il faut un multiple de 2 +1  ({nb_mailles} + 1)"
            )
            nb_mailles += 1
        elif point == Point.DOUBLE_COTE and nb_mailles % 4 != 0:
            print(
                f"INFO: avec la double côte il faut un multiple de 4 en maille + 2 ({nb_mailles} + {nb_mailles % 4 - 0})"
            )
            nb_mailles += nb_mailles % 4 - 0
        return nb_mailles

    def ajouter_trapeze(
        self,
        largeur_bas_cm: float,
        hauteur_cm: float,
        largeur_haut_cm: float,
        rabat_de_maille: int = 0,
        point: Point = Point.JERSEY,
    ):

        # TODO
        # - rajouter la gestion des points (cote ou jersey), pour le moment
        #   tout jersey

        # traduction cm -> maille et rang
        largeur_bas_maille = self.largeur_cm_en_maille(largeur_bas_cm)
        largeur_haut_maille = self.largeur_cm_en_maille(largeur_haut_cm)
        largeur_bas_maille = self.ajuster_nb_mailles_fonction_point(
            largeur_bas_maille, point
        )
        largeur_haut_maille = self.ajuster_nb_mailles_fonction_point(
            largeur_haut_maille, point
        )

        ajustement_gauche = 0
        ajustement_droit = 0
        if len(self.operations) > 0:
            # peut être qu'il y a eu des côtes et qu'il a fallu ajuster la largeur et donc il faut bien ajouter l'opération nécessaire pour retourner au bon nombre de mailles
            largeur_theorique = self.nb_maille_depart
            for o in self.operations:
                largeur_theorique += sum(item[0] for item in o)
                largeur_theorique += sum(item[1] for item in o)

            if largeur_theorique != largeur_bas_maille:
                print(
                    f"INFO: la largeur théorique n'est pas la même que les largeurs de trapèse, il faut rajouter une opération pour ajuster la largeur ({largeur_theorique} vs {largeur_bas_maille})    "
                )
                ajustement_gauche = int((largeur_bas_maille - largeur_theorique) / 2)
                ajustement_droit = (
                    largeur_bas_maille - largeur_theorique
                ) - ajustement_gauche

        largeur_bas_maille += rabat_de_maille * 2
        if (largeur_haut_maille - largeur_bas_maille) % 2 == 1:
            print(
                "INFO: trapèze symétric donc il faut qu'on est un nombre d'opération symétrique)"
            )
            largeur_haut_maille += 1

        hauteur_rang = self.hauteur_cm_en_rang(hauteur_cm)
        if hauteur_rang % 2 == 1:
            print(f"INFO: nombre de rang impaire ({hauteur_rang})")
            hauteur_rang += 1

        # calculer et répartir les diminussions / augmentations
        nb_operations = round((largeur_haut_maille - largeur_bas_maille) / 2)

        nb_rangs = round(hauteur_rang / 2) - 1

        quotient, reste = divmod(nb_operations, nb_rangs)
        if abs(quotient) >= 2:
            print(
                f"WARNING: attention il va y avoir de très grosses augmentations/diminussions ({quotient})"
            )
        operations = [
            (rabat_de_maille + ajustement_gauche, rabat_de_maille + ajustement_droit)
        ] + [(int(quotient), int(quotient))] * nb_rangs
        for i in range(int(reste)):
            operations[i * nb_rangs // reste + 1] = (
                int(quotient) + 1,
                int(quotient) + 1,
            )

        if self.nb_maille_depart == 0:
            self.nb_maille_depart = largeur_bas_maille
        self.operations.append(operations)
        self.points.append(point)
