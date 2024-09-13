def conta_vogais(texto: str) -> int:
    is_vogal = lambda x: x.lower() in 'aeiou'
    
    return len(list(filter(is_vogal, texto)))

print(conta_vogais("Exemplo de texto"))
