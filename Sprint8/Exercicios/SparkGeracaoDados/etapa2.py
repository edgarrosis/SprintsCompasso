# Lista de 20 animais
animais = ["gato", "cachorro", "zebra", "tigre", "elefante", "girafa", "jacare", "panda", "urso", "capivara",
           "lobo", "macaco", "cavalo", "camelo", "rinoceronte", "hipopetamo", "canguru", "pinguim", "tubarao", "golfinho"]

# Ordena a lista
animais.sort()

# Itera sobre a lista imprimindo cada animal
for animal in animais:
    print(animal)

csv = "Sprint8\Exercicios\SparkGeracaoDados\lista_animais.csv"

# Armazena a lista em um arquivo CSV
with open(csv, "w") as file:
    for animal in animais:
        file.write(animal + "\n")
