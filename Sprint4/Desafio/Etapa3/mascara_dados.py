import hashlib

while True:
    # Receber input do usuário
    entrada = input("Digite uma string para mascarar (ou 'exit()' para encerrar): ")
    if entrada.lower() == 'exit()':
        break
    
    # Gerar a hash SHA-1
    hash_object = hashlib.sha1(entrada.encode())
    hex_dig = hash_object.hexdigest()

    # Imprimir a hash
    print(f"Hash SHA-1: {hex_dig}")
