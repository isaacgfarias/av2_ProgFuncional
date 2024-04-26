

# Recebe o texto a ser mostrado no terminal como uma função input normal...
# Como tbm recebe após o texto os valores permitidos ao usuário inserir.
# Ficará mostrando o texto até o usuário digitar um valor válido.
def input_valido(texto, lista):
    while True:
        x = input(texto)
        if x.isalpha(): x = x.lower()
        for el in lista:
             if el.isalpha() : el.lower() 
             if str(el) == x : return x
        print(f"\nEntrada invalida.\nTente " + " ou ".join(map(str, lista)))

# Semelhante a input_valido(), esse só aceita strings númericas (com/sem ponto flutuante) como entrada...
# E os retorna em formato float
def input_apenas_nums(texto):
    while True:
        x = input(texto)
        if x.replace('.','',1).isdigit(): return float(x)
        print("Inválida! A entrada digitada deve ser numérica.\n")




