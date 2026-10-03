# %%
import draw_pattern

# %%

dos = draw_pattern.PatronDroit(35, 51)

print("ETAPE 1: bord de côte")
dos.ajouter_trapeze(50, 7, 50, point=draw_pattern.Point.DOUBLE_COTE)

print("ETAPE 2: corps")
dos.ajouter_trapeze(50, 24, 50)

print("ETAPE 3: raglan")
dos.ajouter_trapeze(50, 24, 15, rabat_de_maille=-5)

dos.to_csv("dos.csv")


print(dos.operations)
print(dos)


devant = draw_pattern.PatronDroit(35, 51)

print("ETAPE 1: bord de côte")
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
encolure.print()


devant.ajouter_mixte_courbe_trapeze(
    hauteur_total_cm=17,
    largeur_bas_cm=28,
    largeur_haut_cm=None,
    largeur_haut_maille=3,
    hauteur_courbe_cm=5,
    courbe=encolure,
    rabat_de_maille=-5,
)

print(devant.operations)
# print(devant)

devant.to_csv("devant.csv")
