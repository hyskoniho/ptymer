# Suponha que esta seja a sua lista
lista = [
    ["item0_1", "item0_2"],
    ["item1_1", "item1_2"],
    ["item2_1", "item2_2"]
]

# Criação do dicionário
dicionario = {indice: (sublista[0], sublista[1]) for indice, sublista in enumerate(lista)}

print(dicionario)


