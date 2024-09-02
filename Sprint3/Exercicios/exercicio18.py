def paramentros(args):
    lista = []
    for n, m in args.items():
        lista.append(m)

    return list(set(lista))

speed = {'jan':47, 'feb':52, 'march':47, 'April':44, 'May':52, 'June':53, 'july':54, 'Aug':44, 'Sept':54}

lista = paramentros(speed)

print(lista)