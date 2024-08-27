def imprime_parametros(*sem_nome, **nomeado):
    for i in sem_nome:
        print(i)

    for i, y in nomeado.items():
        print(y)

imprime_parametros(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
