# Diretório onde os relatórios estão armazenados
DIR_BACKUP="ecommerce/vendas/backup"

# Nome do arquivo final
ARQUIVO_FINAL="relatorio_final.txt"

# Consolidar os relatórios
cat "$DIR_BACKUP"/relatorio.txt > "$DIR_BACKUP/$ARQUIVO_FINAL" 