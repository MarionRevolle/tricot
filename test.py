# %%
import draw_pattern

# %%

dos = draw_pattern.PatronDroit(35, 51)
dos.ajouter_trapeze(50, 7, 50, point=draw_pattern.Point.DOUBLE_COTE)
dos.ajouter_trapeze(50, 24, 50)
dos.ajouter_trapeze(50, 24, 15, rabat_de_maille=-5)
dos.to_csv("dos.csv")

# %%
devant = draw_pattern.PatronDroit(35, 51)
devant.ajouter_trapeze(28, 7, 28, point=draw_pattern.Point.DOUBLE_COTE)
devant.ajouter_trapeze(28, 23, 28)
encolure = draw_pattern.Courbe(
    28,
    36,
    [
        (0, 0),
        (0 + 2, -25),
        (0 + 2 + 2, -3 - 25),
        (0 + 2 + 2 + 2, -2 - 3 - 25),
        (0 + 2 + 2 + 2 + 2, -2 - 2 - 3 - 25),
        (0 + 2 + 2 + 2 + 2 + 2, -1 - 2 - 2 - 3 - 25),
        (0 + 2 + 2 + 2 + 2 + 2 + 2, -1 - 1 - 2 - 2 - 3 - 25),
        (0 + 2 + 2 + 2 + 2 + 2 + 2 + 2, -1 - 1 - 1 - 2 - 2 - 3 - 25),
    ],
)
# encolure.print()
devant.ajouter_mixte_courbe_trapeze(
    hauteur_total_cm=22,
    largeur_bas_cm=28,
    largeur_haut_cm=None,
    largeur_haut_maille=3,
    hauteur_courbe_cm=5,
    courbe=encolure,
    rabat_de_maille=-5,
)
devant.to_csv("devant.csv")

# %%
manche = draw_pattern.PatronDroit(35, 51)
manche.ajouter_trapeze(24, 7, 24, point=draw_pattern.Point.DOUBLE_COTE)
manche.ajouter_trapeze(24, 37, 38)
manche.ajouter_depuis_une_copie(
    patron_copie=dos,
    copie_indice_operation=2,
    droite=False,
)
manche.ajouter_depuis_une_copie(
    patron_copie=devant,
    copie_indice_operation=2,
    droite=True,
    courant_indice_operation=2,
)
manche.to_csv("manche.csv")

# %% pour plus tard essayer de faire un patron français
# print("Réaliser le dos")
# print(dos)
# print("Réaliser le devant")
# print(devant)
