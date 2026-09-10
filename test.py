# %%
import draw_pattern

# %%

dos = draw_pattern.PatronDroit(35, 51)

print("ETAPE 1: bord de côte")
dos.ajouter_trapeze(50, 7, 50)

print("ETAPE 2: corps")
dos.ajouter_trapeze(50, 24, 50)

print("ETAPE 3: raglan")
dos.ajouter_trapeze(50, 24, 15, rabat_de_maille=-5)

dos.to_csv("dos.csv")
