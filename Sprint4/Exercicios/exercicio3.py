from functools import reduce

def calcula_saldo(lancamentos) -> float:
    calcular_valor = lambda x: x[0] if x[1] == 'C' else -x[0]
    
    valores = map(calcular_valor, lancamentos)
    
    saldo_final = reduce(lambda x, y: x + y, valores)
    
    return saldo_final

lancamentos = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]

print(calcula_saldo(lancamentos))