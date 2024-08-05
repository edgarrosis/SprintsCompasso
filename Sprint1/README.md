# Sprint 01

# 1. Introdução

Esta sprint utilizou a prática dos comandos Linux e Markdown, envolvendo a criação de scripts para processar e gerar relatórios de vendas. O projeto inclui a automação de tarefas utilizando cron jobs. O objetivo final em realizar backups dos relatorios diarios e agrupa-los em um relatorio final.

Para alcançar esse objetivo, foi utilizado como material de apoio dois cursos compostos por videoaulas e questionários. O primeiro curso, [Linux para Desenvolvedores](https://compassuol.udemy.com/course/linux-para-desenvolvedores-com-terminal-shell-apache/learn/lecture/29391082?course_portion_id=390134&learning_path_id=5948466#overview), forneceu instruções e comandos básicos para navegação no ambiente Linux. A experiência com o mesmo foi documentada em [anotações](/Sprint1/Cursos/Linux/anotacoesLinux.txt). O segundo curso, [Git e Github do básico ao avançado](https://compassuol.udemy.com/course/git-e-github-do-basico-ao-avancado-c-gist-e-github-pages/learn/lecture/21922906?course_portion_id=390132&learning_path_id=5948466#overview), forneceu conhecimentos sobre Markdown e a organização de repositórios, ampliando os conhecimentos adquiridos na matéria de Gerencia de Configuração de Software do curso de Engenharia de Software, UFMS.

# 2. Resolução do Desafio
A resolução do desafio final da sprint foi iniciada no dia 29/07/2024 até o dia 31/07/2024 com o desenvolvimento dos scripts `processamento_de_vendas.sh` e `consolidador_de_processamento_de_vendas.sh`

Seu desenvolvimento e como executá-los está detalhado em [Resolução Desafio](/Sprint1/Desafio/README.md)

# 3. Resultados do Desafio
Apos testes unitários simples dos scripts e dos agendamentos, seguiram-se as execuções referentes ao desafio final. Devido os desencontros de informações, as execuções foram agendadaspara os dias da semana quinta, sexta, sábado e domingo (respectivamente dias 01, 02, 03 e 04), ao contrário do proposto pelo desafio, de segunda a quarta.

**a) Relatorio 1**
- Primeiro relatório proveniente dos agendamentos, quinta-feira dia 01/08;
- Evidencias:
    - [Relatorio 1](/Sprint1/evidencias/relatorio1.png)
    - [Log agendamento dia 1, processamento](/Sprint1/evidencias/log_processamento1.png)
    - [Log agendamento dia 1, consolidaçao](/Sprint1/evidencias/log_consolidacao1.png)
    - [Relatorio Final do dia 1](/Sprint1/evidencias/relatorio_final_dia1.png)

**b) Relatorio 2**
- Segundo relatório proveniente dos agendamentos, sexta-feira dia 02/08;
- Evidencias:
    - [Relatorio 2](/Sprint1/evidencias/relatorio2.png)
    - [Log agendamento dia 2](/Sprint1/evidencias/log_agendamento2.png)
    - [Relatorio Final do dia 2](/Sprint1/evidencias/relatorio_final_dia12.png)

**c) Relatorio 3**
- Primeiro relatório proveniente dos agendamentos, sábado dia 03/08;
- Evidencias:
    - [Relatorio 3](/Sprint1/evidencias/relatorio1.png)
    - [Log agendamento dia 3](/Sprint1/evidencias/log_agendamento3.png)
    - [Relatorio Final do dia 3](/Sprint1/evidencias/relatorio_final_dia3.png)

**d) Relatorio 4**
- Quarto relatório proveniente dos agendamentos, domingo dia 04/08
- Evidencias:
    - [Relatorio 4](/Sprint1/evidencias/relatorio4.png)
    - [Log agendamento dia 4](/Sprint1/evidencias/log_agendamento4.png)
    - [Relatorio Final do dia 4](/Sprint1/evidencias/relatorio_final_dia4.png) 

## 3.1 Resultados Finais
Os scripts funcionam conforme esperado, criando backups, gerando relatórios detalhados e consolidando os dados de vendas de forma eficiente. A automação com crontab garantiu a execução periódica e sem falhas dos scripts. Os arquivos gerados são armazenados em arquivos .zip para minimizar a ocupação dos mesmos na memória.

![Backsups gerados](/Sprint1/evidencias/backups_relatorios.png)

# 4. Conclusão

A prática dos comandos Linux e o uso do crontab se mostraram ferramentas eficientes para a automação de tarefas, como6 a criação de relatórios de dados. Através do uso dessas tecnologias, foi possível desenvolver um script eficiente que processa e organiza informações de vendas, automatizando a geração de relatórios diários. Houveram desafios ao longo do desenvolvimento, quanto a utilização dos parâmetros corretos para selecionar as informações exigidas para o relatório, essas dificuldades foram superadas a paritr das reuniões técnicas. 

O conhecimento adquirido sobre Linux e automação de tarefas possibilitou a execução de processos repetitivos de maneira mais eficiente e organizada, contribuindo significativamente para a otimização das atividades de gestão de dados.

# 5. Certificados da Sprint
- [Certificado do Curso de Linux para Desenvolvedores(c/ terminal, Shell, Apache e +)](/Sprint1/Certificados/Certificado_cursoLinux.jpg)
- [Certificado do Curso de Git e GitHub do básico ao avançado (c/ gist e GitHub Pages)](/Sprint1/Certificados/Certificado_cursoGit.jpg)
- [Certificado de Conclusão Data & Analytics - PB - AWS - Novo - 1/10](/Sprint1/Certificados/Certificado_Sprint1.jpg)