# Definindo variáveis
DIR_ECOMMERCE="ecommerce"
DIR_VENDAS="$DIR_ECOMMERCE/vendas"
DIR_BACKUP="$DIR_VENDAS/backup"
ARQUIVO_ORIGINAL="dados_de_vendas.csv"
DATA_EXEC=$(date +"%Y%m%d")

# Criação de diretórios
mkdir -p "$DIR_BACKUP"

# Movendo o arquivo para o diretório vendas
mv "$DIR_ECOMMERCE/$ARQUIVO_ORIGINAL" "$DIR_VENDAS/"

# Copiando o arquivo para o diretório de backup com data
cp "$DIR_VENDAS/$ARQUIVO_ORIGINAL" "$DIR_BACKUP/dados-$DATA_EXEC.csv"

# Renomeando o arquivo no diretório de backup
mv "$DIR_BACKUP/dados-$DATA_EXEC.csv" "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv"

# Criando o arquivo relatório.txt
{
    echo "Data do sistema: $(date '+%Y/%m/%d %H:%M')"
    echo "Data do primeiro registro de venda: $(head -2 "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv" | tail -1 | cut -d',' -f5)"
    echo "Data do último registro de venda: $(tail -1 "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv" | cut -d',' -f5)"
    echo "Quantidade total de itens diferentes vendidos: $(cut -d',' -f2 "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv" | sort | uniq | wc -l)"
    echo "Primeiras 10 linhas do arquivo backup-dados-$DATA_EXEC.csv:"
    head -11 "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv"
} > "$DIR_BACKUP/relatorio.txt"

# Comprimindo o arquivo
zip "$DIR_BACKUP/backup-dados-$DATA_EXEC.zip" "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv" "$DIR_BACKUP/relatorio.txt"

# Removendo o arquivo original de backup e o arquivo de vendas
rm "$DIR_BACKUP/backup-dados-$DATA_EXEC.csv" "$DIR_VENDAS/$ARQUIVO_ORIGINAL"
