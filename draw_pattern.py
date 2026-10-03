from enum import Enum

import plotly.graph_objects as go
from scipy.interpolate import CubicSpline


class Maille(Enum):
    AUCUNE = 0
    SIMPLE_FONTURE = 1
    DOUBLE_FONTURE = 2

    def __str__(self):
        if self == Maille.AUCUNE:
            return ""
        elif self == Maille.SIMPLE_FONTURE:
            return "X"
        elif self == Maille.DOUBLE_FONTURE:
            return "O"


class Point(Enum):
    JERSEY = 0  # maille tout le temps simple fonture
    SIMPLE_COTE = (
        1  # alternance des mailles 1 sur la simple fonture / 1 sur la double fonture
    )
    DOUBLE_COTE = (
        2  # alternance des mailles : 2 sur la simple fonture / 2 sur la double fonture
    )

    def __str__(self):
        return self.name.replace("_", " ").lower()


class Rang:
    # l'index donne la position de la maille, le type donne la maille
    rang: list[Maille]


def largeur_cm_en_maille(largeur_cm: float, nb_maille_10cm: int) -> int:
    return round(largeur_cm * nb_maille_10cm / 10)


def hauteur_cm_en_rang(hauteur_cm: float, nb_rang_10cm: int) -> int:
    return round(hauteur_cm * nb_rang_10cm / 10)


def largeur_maille_en_cm(largeur_maille: int, nb_maille_10cm: int) -> float:
    return largeur_maille * 10.0 / nb_maille_10cm


def hauteur_rang_en_cm(hauteur_rang: int, nb_rang_10cm: int) -> float:
    return hauteur_rang * 10.0 / nb_rang_10cm


class Courbe:
    def __init__(
        self, nb_maille_10cm: int, nb_rang_10cm: int, points: list[tuple[int, int]]
    ):
        self.points_cm: list[tuple[float, float]] = [
            (
                largeur_maille_en_cm(p[0], nb_maille_10cm),
                hauteur_rang_en_cm(p[1], nb_rang_10cm),
            )
            for p in points
        ]

        if len(self.points_cm) < 2:
            raise ValueError("Une spline nécessite au moins deux points")

        abscisses = [point[0] for point in self.points_cm]
        ordonnees = [point[1] for point in self.points_cm]
        if len(set(abscisses)) != len(abscisses):
            raise ValueError("Les largeurs des points doivent être différentes")

        ordre = sorted(range(len(abscisses)), key=abscisses.__getitem__)
        abscisses_triees = [abscisses[i] for i in ordre]
        ordonnees_triees = [ordonnees[i] for i in ordre]
        self.fonction = CubicSpline(abscisses_triees, ordonnees_triees)

    def print(self):
        abscisses = self.fonction.x
        debut = abscisses[0]
        fin = abscisses[-1]
        echantillons = [debut + (fin - debut) * i / 199 for i in range(200)]
        figure = go.Figure()
        figure.add_scatter(
            x=echantillons,
            y=self.fonction(echantillons),
            mode="lines",
            name="Spline",
        )
        figure.add_scatter(
            x=[point[0] for point in self.points_cm],
            y=[point[1] for point in self.points_cm],
            mode="markers",
            name="Points",
        )
        figure.update_layout(
            title="Fonction de la courbe",
            xaxis_title="Hauteur (cm)",
            yaxis_title="Largeur (cm)",
        )
        figure.write_html("courbe.html", auto_open=False)
        print("Graphique enregistré dans courbe.html")


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
        operation_gauche: int,
        operation_droite: int,
        point: Point,
        nb_mailles_depart_gauche: int,
        nb_mailles_depart_droit: int,
    ) -> Rang:
        rang = [Maille.AUCUNE] * self.nb_aiguilles
        milieu = int(self.nb_aiguilles / 2)
        nb_mailles_gauche = nb_mailles_depart_gauche + operation_gauche
        nb_mailles_droit = nb_mailles_depart_droit + operation_droite
        nb_mailles = nb_mailles_droit + nb_mailles_gauche

        if point == Point.JERSEY:
            rang[milieu - nb_mailles_gauche : milieu + nb_mailles_droit] = [
                Maille.SIMPLE_FONTURE
            ] * nb_mailles
        elif point == Point.SIMPLE_COTE:
            for i in range(nb_mailles):
                if i % 2 == 0:
                    rang[milieu - nb_mailles_gauche + i] = Maille.SIMPLE_FONTURE
                else:
                    rang[milieu - nb_mailles_gauche + i] = Maille.DOUBLE_FONTURE
        elif point == Point.DOUBLE_COTE:
            for i in range(nb_mailles):
                if (i // 2) % 2 == 0:
                    rang[milieu - nb_mailles_gauche + i] = Maille.SIMPLE_FONTURE
                else:
                    rang[milieu - nb_mailles_gauche + i] = Maille.DOUBLE_FONTURE
        return rang

    def to_csv(self, nom_fichier: str):

        # ranger ça dans le patron
        patron: list[Rang] = []

        # rang avec les operations
        nb_mailles_depart_gauche = int(self.nb_maille_depart / 2)
        nb_mailles_depart_droit = self.nb_maille_depart - nb_mailles_depart_gauche
        for partie, op in enumerate(self.operations):
            point = self.points[partie]
            for r, o in enumerate(op):
                rang = self.faire_un_rang(
                    o[0], o[1], point, nb_mailles_depart_gauche, nb_mailles_depart_droit
                )
                patron.append(rang)
                patron.append(rang)
                nb_mailles_depart_gauche += o[0]
                nb_mailles_depart_droit += o[1]

        with open(nom_fichier, "w") as f:
            for rang in reversed(patron):
                f.write(",".join([str(maille) for maille in rang]))
                f.write("\n")

    def __str__(self) -> str:

        def tuple_to_text(t):
            gauche, droite = t
            gauche = abs(gauche)
            droite = abs(droite)
            if gauche == droite:
                return f"{gauche} mailles à gauche et à droite"
            return f"{gauche} mailles à gauche et {droite} mailles à droite"

        str = f"Montez {self.nb_maille_depart} mailles\n"
        for p, o in enumerate(self.operations):
            # CAS 1 : il n'y a que des zéro partout
            if sum([item[0] + item[1] for item in o]) == 0:
                str += f"Tricoter {len(o) * 2} rangs de {self.points[p]}\n"
            # CAS 2 : il n'y a que des zéros partout sauf au premier rang
            elif sum([item[0] + item[1] for item in o[1:]]) == 0:
                if o[0][0] + o[0][1] < 0:
                    str += "Diminuer "
                else:
                    str += "Augmenter "
                str += tuple_to_text(o[0]) + "\n"
                str += (
                    f"Continuer en {self.points[p]} pendant {(len(o) - 1) * 2} rangs\n"
                )
            # CAS 3 : Sinon trouver les répétitions et les afficher
            else:
                special_rank_1 = abs(o[0][0]) > 2 or abs(o[0][1]) > 0
                if special_rank_1:
                    if o[0][0] + o[0][1] < 0:
                        str += "Rabattre "
                    else:
                        str += "Monter "
                    str += tuple_to_text(o[0]) + "\n"

                str += "TODO\n"
        return str

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
        # traduction cm -> maille et rang
        largeur_bas_maille = largeur_cm_en_maille(
            largeur_bas_cm, self.echantillon_10cm["nb_maille_10cm"]
        )
        largeur_haut_maille = largeur_cm_en_maille(
            largeur_haut_cm, self.echantillon_10cm["nb_maille_10cm"]
        )
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
                    f"INFO: la largeur théorique n'est pas la même que les largeurs de trapèze, il faut rajouter une opération pour ajuster la largeur ({largeur_theorique} vs {largeur_bas_maille})    "
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

        hauteur_rang = hauteur_cm_en_rang(
            hauteur_cm, self.echantillon_10cm["nb_rang_10cm"]
        )
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

    def operation_courbe(
        self,
        hauteur_cm: float,
        courbe: Courbe,
        courbe_a_droite: bool = True,
    ):
        operations = []
        hauteur_courante = 0.0
        operation_faites = 0.0

        while hauteur_courante < hauteur_cm:
            operation_cm = courbe.fonction(hauteur_courante)
            operation_maille = int(
                largeur_cm_en_maille(
                    operation_cm, self.echantillon_10cm["nb_maille_10cm"]
                )
                - operation_faites
            )
            if courbe_a_droite:
                operations.append((0, operation_maille))
            else:
                operations.append((operation_maille, 0))

            hauteur_courante += hauteur_rang_en_cm(
                2, self.echantillon_10cm["nb_rang_10cm"]
            )
            operation_faites += operation_maille
        return operations

    def ajouter_courbe(
        self,
        hauteur_cm: float,
        courbe: Courbe,
        courbe_a_droite: bool = True,
        point: Point = Point.JERSEY,
    ):
        operations = self.operation_courbe(hauteur_cm, courbe, courbe_a_droite)
        self.operations.append(operations)
        self.points.append(point)

    def ajouter_mixte_courbe_trapeze(
        self,
        hauteur_total_cm: float,
        largeur_bas_cm: float,
        largeur_haut_cm: float | None,
        hauteur_courbe_cm: float,
        courbe: Courbe,
        largeur_haut_maille: float | None = None,
        rabat_de_maille: int = 0,
        courbe_a_droite: bool = True,
    ):

        # étape 1 : on dessine la courbe
        hauteur_sans_courbe_cm = hauteur_total_cm - hauteur_courbe_cm

        operations_rectangle = [(0, 0)] * int(
            hauteur_cm_en_rang(
                hauteur_sans_courbe_cm, self.echantillon_10cm["nb_rang_10cm"]
            )
            / 2
        )

        operations_courbe = self.operation_courbe(
            hauteur_courbe_cm, courbe, courbe_a_droite
        )

        operations = operations_rectangle + operations_courbe

        nb_maille_courbe = sum(gauche + droite for gauche, droite in operations)

        # étape 2 : on dessine le trapèze
        if largeur_haut_cm is None and largeur_haut_maille is None:
            raise ValueError(
                "Il faut soit la largeur du haut en cm soit la largeur du haut en mailles"
            )
        if largeur_haut_cm is not None and largeur_haut_maille is not None:
            raise ValueError(
                "Il faut soit la largeur du haut en cm soit la largeur du haut en mailles, pas les deux"
            )
        if largeur_haut_cm is not None:
            largeur_haut_maille = largeur_cm_en_maille(
                largeur_haut_cm, self.echantillon_10cm["nb_maille_10cm"]
            )

        largeur_bas_maille = (
            largeur_cm_en_maille(
                largeur_bas_cm, self.echantillon_10cm["nb_maille_10cm"]
            )
            + rabat_de_maille
            + nb_maille_courbe
        )

        # calculer et répartir les diminussions / augmentations
        nb_operations = largeur_haut_maille - largeur_bas_maille

        nb_rangs = len(operations) - 1

        quotient, reste = divmod(nb_operations, nb_rangs)
        if abs(quotient) >= 2:
            print(
                f"WARNING: attention il va y avoir de très grosses augmentations/diminussions ({quotient})"
            )
        if courbe_a_droite:
            operations[0] = (rabat_de_maille, operations[0][1])
        else:
            operations[0] = (operations[0][0], rabat_de_maille)

        for i in range(1, int(nb_rangs)):
            if courbe_a_droite:
                operations[i] = (
                    int(quotient),
                    operations[i][1],
                )
            else:
                operations[i] = (
                    operations[i][0],
                    int(quotient),
                )

        for i in range(int(reste)):
            if courbe_a_droite:
                operations[i * nb_rangs // reste + 1] = (
                    int(quotient) + 1,
                    operations[i * nb_rangs // reste + 1][1],
                )
            else:
                operations[i * nb_rangs // reste + 1] = (
                    operations[i * nb_rangs // reste + 1][0],
                    int(quotient) + 1,
                )

        self.operations.append(operations)
        self.points.append(Point.JERSEY)

    def ajouter_depuis_une_copie(
        self,
        patron_copie: "PatronDroit",
        copie_indice_operation: int,
        droite: bool = True,
        courant_indice_operation: int | None = None,
    ):

        operation_a_copier = patron_copie.operations[copie_indice_operation]
        if courant_indice_operation is None:
            operations = [(0, 0)] * len(operation_a_copier)
            self.operations.append(operations)
            self.points.append(patron_copie.points[copie_indice_operation])
            courant_indice_operation = len(self.operations) - 1

        for i, op in enumerate(operation_a_copier):
            if droite:
                self.operations[courant_indice_operation][i] = (
                    self.operations[courant_indice_operation][i][0],
                    patron_copie.operations[copie_indice_operation][i][0],
                )
            else:
                self.operations[courant_indice_operation][i] = (
                    patron_copie.operations[copie_indice_operation][i][1],
                    self.operations[courant_indice_operation][i][1],
                )
