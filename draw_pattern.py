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
            tuple[int, int]
        ] = []  # (operation gauche, operation droite)
        self.nb_maille_depart = 0

    def to_csv(self, nom_fichier: str):

        # ranger ça dans le patron

        milieu = int(self.nb_aiguilles / 2)
        patron: list[Rang] = []

        # rang avec les operations
        for r, o in enumerate(self.operations):
            nb_mailles = (
                self.nb_maille_depart
                + sum(item[0] for item in self.operations[0:r])
                + sum(item[1] for item in self.operations[0:r])
            )
            rang = [Maille.AUCUNE] * self.nb_aiguilles
            rang[milieu - int(nb_mailles / 2) : milieu + int(nb_mailles / 2)] = [
                Maille.SIMPLE_FONTURE
            ] * nb_mailles
            patron.append(rang)
            patron.append(rang)

        with open(nom_fichier, "w") as f:
            for rang in reversed(patron):
                f.write(
                    ",".join(
                        ["" if maille == Maille.AUCUNE else "V" for maille in rang]
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

        str = f"Montez {self.nb_maille_depart} mailles\n"

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
        if len(self.operations) > 0:
            largeur_theorique = (
                self.nb_maille_depart
                + sum(item[0] for item in self.operations)
                + sum(item[1] for item in self.operations)
            )
            if largeur_theorique != largeur_bas_maille:
                raise RuntimeError(
                    f"ERREUR: largeur du bas du trapeze ({largeur_bas_maille}) ne correspond pas à la largeur théorique ({largeur_theorique})"
                )

        largeur_bas_maille += rabat_de_maille * 2
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

        nb_rangs = round(hauteur_rang / 2) - 1

        quotient, reste = divmod(nb_operations, nb_rangs)
        if abs(quotient) >= 2:
            print(
                f"WARNING: attention il va y avoir de très grosses augmentations/diminussions ({quotient})"
            )
        operations = [(rabat_de_maille, rabat_de_maille)] + [
            (int(quotient), int(quotient))
        ] * nb_rangs
        for i in range(int(reste)):
            operations[i * nb_rangs // reste + 1] = (
                int(quotient) + 1,
                int(quotient) + 1,
            )

        if self.nb_maille_depart == 0:
            self.nb_maille_depart = largeur_bas_maille
        self.operations += operations
