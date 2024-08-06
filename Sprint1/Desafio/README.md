# 1. Instruções
Para a reprodução do que foi feito no Desafio Final, é necessario: criar os scripts `processamento_de_vendas.sh` e `consolidador_de_processamenteo_de_vendas.sh` no diretorio do usuario do Linux, em seguida criar um diretório `ecommerce` com o comando
```sh
mkdir ecommerce
```
e adicionar o arquivo `dados_de_vendas.csv` contendo as informações das vendas. O arquivo pode ser movido com o comando, caso ele esteja na pasta do usuario:

``` sh
mv dados_vendas.csv ecommerce/
```

## 1.1 Criação do Script de Processamento de Vendas

### Arquivo `processamento_de_vendas.sh`

Este script realiza as seguintes tarefas:

1. **Criação de Diretórios e Cópia de Arquivos**:
    - Cria um diretório `vendas` e copia o arquivo `dados_vendas.csv` para dentro dele.
    - Cria um subdiretório `backup` dentro do diretório `vendas` e faz uma cópia do arquivo `dados_vendas.csv` para dentro dele com a data de execução no nome do arquivo.

2. **Renomeação e Criação de Relatório**:
    - Renomeia o arquivo de backup.
    - Cria um arquivo `relatorio.txt` contendo:
        - Data do sistema operacional.
        - Data do primeiro registro de venda.
        - Data do último registro de venda.
        - Quantidade total de itens diferentes vendidos.
    - Adiciona as primeiras 10 linhas do arquivo de backup no `relatorio.txt`.

3. **Compressão e Limpeza**:
    - Comprime o arquivo de backup e o relatorio gerado no dia. (linha 31)
    - Apaga o arquivo original de backup e o arquivo `dados_vendas.csv` do diretório `vendas`.

É necessario que o pacote **.zip** esteja instalado, caso contrario, pode ser solucionado utilizando o comando:
```sh
sudo apt-get install zip
```

### Código do Script
- A linhas referenciadas se encontram no codigo a seguir: 
```sh
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

```

## 2.2 Criação do Script Consolidação do Processamento de Vendas

O Script realiza a seguinte tarefa:

- Localiza o diretório em que o relatório é armazenado
- Cria uma variavel que recebe `relatorio_final.txt` como argumento
- Agrega os relatorios gerados em um mesmo arquivo `relatorio_final.txt`

### Codigo do Script
- A linha referenciada se encontra no codigo a seguir: 
``` sh
# Diretório onde os relatórios estão armazenados
DIR_BACKUP="ecommerce/vendas/backup"

# Nome do arquivo final
ARQUIVO_FINAL="relatorio_final.txt"

# Consolidar os relatórios
cat "$DIR_BACKUP"/relatorio.txt > "$DIR_BACKUP/$ARQUIVO_FINAL" 
```

## 2.3 Agendamento
 Para realizar o agendamento para execução diária, às 15:27 e as 15:28 utiliza-se o `crontab -e`, seguido dos seguintes comandos:
```sh
27 15 * * * cd /home/nomeUsuario && ./processamento_de_vendas.sh >> /home/nomeUsuario/processamento_de_vendas.log 2>&1

28 15 * * * cd /home/nomeUsuario && ./consolidador_de_processamento_de_vendas.sh
```
Em que 27 15 se refere ao horario em que sera executado, e os * representam respectivamente, da esqueda para a direita, o ano, mês e dia da semana em que o programa deve realizar a tarefa (0 a 7). 
 
Em seguida é necessario se movimentar da raiz do diretório até o diretório em que está o script, que deve ser executado utilizando o comando `cd /home/nomeUsuario`, seguido da execução do mesmo com `./processamento_de_vendas.sh`, e gerar um log mostrando que o mesmo foi executado.

Quanto ao segundo agendamento , é referente ao segundo script, que agrega os relatorios gerados diariamente em um relatorio final, segue a mesma logica do agendamento anterior.

Após serem executados automaticamente, os logs gerados podem ser observados  no `processamento_de_vendas.log` ou, a partir da pagina raiz do sistema (`cd /`), navegar para `cd var/logs; cat syslog` para anilizar se houve ou não a execução agendada.

- Exemplo ![Agendamento Crontab](/Sprint1/evidencias/crontab.png) 
![Log de Execução](/Sprint1/evidencias/processamento_venda_log.png)