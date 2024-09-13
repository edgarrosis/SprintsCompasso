import csv

def processar_notas(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        
        estudantes = []
        for linha in leitor_csv:
            nome = linha[0]
            notas = list(map(int, linha[1:]))  
            tres_maiores_notas = sorted(notas, reverse=True)[:3] 
            media_tres_maiores = round(sum(tres_maiores_notas) / 3, 2) 

            estudantes.append((nome, tres_maiores_notas, media_tres_maiores))
        
        estudantes_ordenados = sorted(estudantes, key=lambda x: x[0])
        
        def formatar_media(media):
           return f"{media:.1f}" if media.is_integer() else f"{media:.2f}"
        
        for estudante in estudantes_ordenados:
            nome, notas, media = estudante
            media_formatada = formatar_media(media)
            print(f"Nome: {nome} Notas: {notas} Média: {media_formatada}")

processar_notas('estudantes.csv')