def calcular_valor_maximo(operadores, operandos) -> float:
    calcular = lambda op, valores: valores[0] + valores[1] if op == '+' else \
                                   valores[0] - valores[1] if op == '-' else \
                                   valores[0] * valores[1] if op == '*' else \
                                   valores[0] / valores[1] if op == '/' else \
                                   valores[0] % valores[1]
    
    # Usar zip para combinar operadores e operandos, e map para aplicar a função de cálculo
    resultados = map(lambda x: calcular(x[0], x[1]), zip(operadores, operandos))
    
    # Retornar o maior valor da lista de resultados
    return max(resultados)

# Exemplo de uso
operadores = ['+','-','*','/','+']
operandos  = [(3,6), (-7,4.9), (8,-8), (10,2), (8,4)]

print(calcular_valor_maximo(operadores, operandos))  # Saída: 12
