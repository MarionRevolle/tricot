# %%
import draw_pattern

# %%

dos = draw_pattern.PatronDroit(35, 51)

print("ETAPE 1: bord de côte")
dos.ajouter_trapeze(50, 7, 50, commencer_tout_de_suite=False, finir_tout_de_suite=False)

print("ETAPE 2: corps")
dos.ajouter_trapeze(
    50, 24, 50, commencer_tout_de_suite=False, finir_tout_de_suite=False
)

print("ETAPE 3: raglan")
dos.ajouter_trapeze(
    50, 24, 15, commencer_tout_de_suite=False, finir_tout_de_suite=False
)

dos.to_csv("dos.csv")
