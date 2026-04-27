# Sistema_Biblioteca_com_POO 🕮 
--> ✨ Este é meu primeiro contato real com a Programação orientada a objetos. Antes dele, eu havia feito um sistema de biblioteca só com funções soltas, e quis refatorar tudo para entender na prática como encapsulamento, herança, abstração e polimorfismo funcionam de verdade.
<br><br>
**Segue o link da primeira biblioteca sem POO -->** [VERSÃO ANTERIOR SEM_POO](https://github.com/MaisaS21/Sistema_Biblioteca)
<br><br>


<p align="left">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/POO-Aplicado-brightgreen">
  <img src="https://img.shields.io/badge/Editor-VS_Code-0078D4?logo=visualstudiocode&logoColor=white">
  <img src="https://img.shields.io/badge/Base-Gustavo_Guanabara-FF7A00">
  <br>
  <img src="https://img.shields.io/badge/Persistência-JSON-4CAF50">
  <img src="https://img.shields.io/badge/Relatórios-PDF_&_Excel-FF5722">
  <img src="https://img.shields.io/badge/Rodando_em-ASUS_Lentinho-FFB6C1">
  <img src="https://img.shields.io/badge/Status-Concluído-008000">
</p>
<br>

### 📌 FUNCIONALIDADES
| Funcionalidade | Descrição |
|----------------|-----------|
| 👤Cadastrar Usuário |--> Registra nome e  telefone com validação de 11 dígitos |
| 📗Cadastrar Livro |--> Registra título, autor, ano e quantidade de exemplares |
| 🔄Emprestar Livro |--> Limita 3 livros por usuário e verifica multas pendentes |
| ↩️Devolver Livro |--> Calcula multa automática de R$ 0,50/dia após 7 dias | 
| 📑Relatórios |--> Listagem de usuários, livros disponíveis e empréstimos ativos |
| 📊Gráfico de Multas |--> Gráfico de pizza com tamanho adaptável e legenda |
| 🔗Exportar Excel |--> Gera planilha com abas indicado detalhes dos empréstimos |
| 🧾Exportar PDF |--> Relatório completo formatado | 
| 💸Pagamento de multas |--> Interface administrativa com senha |
| ⏰Simular tempo |--> Avança datas para testar cálculo de multas |

<br>

### 🧠Conceitos de POO aplicados
| **Conceito** | **Exemplo no código** | **O que aprendi de verdade** |
|----------|-------------------|----------------------------------|
| **ENCAPSULAMENTO** | Atributos privados(__saldo_multa e livros_emprestados)| Proteger dados diretos do usuário evita inconsistências (ex: ninguém pode zerar uma multa sem passar pelo pagamento)|
| **HERANÇA** | class Livro(ItemBiblioteca)| Economizei linha de código: *ItemBiblioteca* já tinha *título, id e exemplares* |
| **ABSTRAÇÃO** | class ItemBiblioteca(ABC) com método @abstractmethod| garante que qualquer item futuro (ex: 'Audiolivro', 'Ebook') implemente '*calcular_multa()*'|
| **POLIMORFISMO** | Método calcular_multa() implementado de forma diferente por classe| Hoje só tenho 'Livro', mas o sistema já está preparado para expansão|

<br>

### 🔧 Estrutura do Projeto (arquitetura limpa)
Sistema_Biblioteca_com_POO/ <br>
| <br>
|--main.py                                   # Interface principal e fluxo do sistema <br>
|--modelos.py                                # Classes( Usuario, Livro, Emprestimo, ItemBiblioteca. Biblioteca) <br>
|--utilidades.py                             # Funções auxiliares (validações, formatação) <br>
|--exportadores.py                           # Geração de Excel e PDF <br>
|--relatorio_graficp_multas.py               # Gráfico de pizza com (matplotlib) <br>
|--requirements.txt                          # Todas as Bibliotecas utilizadas <br>
| <br>
|--LICENCE                                   # MIT License <br>

<br>
<br>

(  📌 *Além disso, o dados ficam salvos em um arquivo json gerado automaticamente, ou seja, persistência dos dados* )

<br>
<br>

-->    **SEGUE ABAIXO O EXEMPLO DE USO (ENTRADA -> SAÍDA) E TAMBÉM PRINTS DO FUNCIONAMENTO** <br>
|    (**OBS**⚠️: Meu notebook é um ASUS com recursos bem limitados. Por isso, o sistema roda de forma mais lenta, então para não deixar exemplo visual do sistema, trouxe aqui uma sequencia dele sendoe executado)

<br>

**Explicação breve e dados utilizadas : ** <br>

1º - Primeiro passo foi realizar um cadastro, errei o telefone de propósito para simular a validação, depois, cadastrei +1 usuário; <br>
2º - Cadastrei um livro com 5 exemplares; <br>
3º - Emprestei 1 exemplar para o usuário 1 e simulei 16 dias com o livro; <br>
4º - Emprestei 1 exemplar para o usuário 2 e simulei o tempo com 32 dias e depois mais 22; <br>
5º - Fiz a devolução do empréstimo do usuário 1 com R$ 28,00 de multa total; <br>
6º - Atualizei que foi paga a multa; <br>
<br>

**USUÁRIO 1** --> Nome: Maria Joaquina Silva; <br>
**USUÁRIO 2** --> Nome: Victor Luan Silva Gomes; <br>
**LIVRO CADASTRADO** --> A negação do brasil negro com 5 exemplares; <br>

<br>

* Menu principal com 13 opções :
  
![Menu principal](screenshots/menu_principal.jpeg) <br>
<br>
* Cadastro de usuário com validação de telefone (11 dígitos) (Passo 1) :
<br>

![Cadastro de usuário](screenshots/cadastrando_usuario.jpeg) <br>
<br>
* Cadastro de livro com titulo, autor, ano de publicação e quantidade de exemplares (Passo 2) :
<br>

![Cadastro de livro](screenshots/cadastrando_livro.jpeg) <br>
<br>
* Após o empréstimo o usuário 'recebe' um comprovante (Passo 3):
<br>

![Comprovante de empréstimo](screenshots/comprovante_emprestimo.jpeg) <br>
<br>
* Exemplo de simulação de tempo (Passo 3 e 4):
<br>

![Simulação de tempo](screenshots/simulando_tempo.jpeg) <br>
<br>
* Comprovante de devolução de livro com multa (Passo 5):
<br>

![Devolução com multa](screenshots/comprovante_devolucao.jpeg) <br>
<br>
* Barra de progresso de 'salvando o arquivo' para PDF e Excel :
<br>

![Barra de progresso](screenshots/barra_de_progresso.jpeg) <br>
<br>
* Interface do administrador (registrando o pagamento de uma multa)(Passo 6) :
<br>

![Pagamento de multas](screenshots/funcao_pagar_multas.jpeg) <br>
<br>
* Gráfico de multas :
<br>

![Gráfico de multas](screenshots/grafico_multas.jpeg) <br>
<br>
* Arquivo excel :
<br>

![Exportação Excel](screenshots/excel.jpeg) <br>
<br>
* Primeira parte do PDF (estatistica geral):
<br>

![Relatório PDF - Estatísticas](screenshots/pdf_estatisticas.jpeg) <br>
<br>
* Segunda parte do PDF (Multas) :
<br>

![Relatório PDF - Multas](screenshots/pdf_multas.jpeg) <br>

<br>
<br>

---

<br>

### 💭 Pontos que quero melhorar futuramente <br>
- Adicionar buscar por título do livro <br>
- Permitir reservar o livro que está emprestado <br>
- Migrar para SQLite quando o sistema 'crescer' <br>
- Criar interface gráfica com PySide6 / PyQt6 <br>

---
<br>
📚 Base do conhecimento adquirido: Curso em Vídeo (Gustavo Guanabara)


