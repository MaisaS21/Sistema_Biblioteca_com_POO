# Sistema_Biblioteca_com_POO
--> Este é meu primeiro contato real com a Programação orientada a objetos. Antes dele, eu havia feito um sistema de biblioteca só com funções soltas, e quis refatorar tudo para entender na prática como encapsulamento, herança, abstração e polimorfismo funcionam de verdade.
<br>
Segue o link da primeira biblioteca sem POO --> ...
<br><br>

### FUNCIONALIDADES
| Funcionalidade | Descrição |
|----------------|-----------|
| Cadastrar Usuário |--> Registra nome e  telefone com validação de 11 dígitos |
| Cadastrar Livro |--> Registra título, autor, ano e quantidade de exemplares |
| Emprestar Livro |--> Limita 3 livros por usuário e verifica multas pendentes |
| Devolver Livro |--> Calcula multa automática de R$ 0,50/dia após 7 dias | 
| Relatórios |--> Listagem de usuários, livros disponíveis e empréstimos ativos |
| Gráfico de Multas |--> Gráfico de pizza com tamanho adaptável e legenda |
| Exportar Excel |--> Gera planilha com abas indicado detalhes dos empréstimos |
| Exportar PDF |--> Relatório completo formatado | 
| Pagamento de multas | Interface administrativa com senha |
| Simular tempo | Avança datas para testar cálculo de multas |

<br>

### Conceitos de POO aplicados
| **Conceito** | **Exemplo no código** | **O que aprendi de verdade** |
|----------|-------------------|----------------------------------|
| **ENCAPSULAMENTO** | Atributos privados(__saldo_multa e livros_emprestados)| Proteger dados diretos do usuário evita inconsistências (ex: ninguém pode zerar uma multa sem passar pelo pagamento)|
| **HERANÇA** | class Livro(ItemBiblioteca)| Economizei linha de código: *ItemBiblioteca* já tinha *título, id e exemplares* |
| **ABSTRAÇÃO** | class ItemBiblioteca(ABC) com método @abstractmethod| garante que qualquer item futuro (ex: 'Audiolivro', 'Ebook') implemente '*calcular_multa()*'|
| **POLIMORFISMO** | Método calcular_multa() implementado de forma diferente por classe| Hoje só tenho 'Livro', mas o sistema já está preparado para expansão|

<br>

### Estrutura do Projeto(arquiteteura limpa)
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

( *Além disso, o dados ficam salvos em um arquivo json gerando automaticamente, ou seja, persistência dos dados* )

<br>
<br>

-->    **SEGUE ABAIXO O EXEMPLO DE USO (ENTRADA -> SAÍDA) E TAMBÉM PRINTS DO FUNCIONAMENTO** <br>
|    (**OBS**: Meu notebook é um ASUS com recursos bem limitados. Por isso, o sistema roda de forma mais lenta, então para não deixar exemplo visual do sistema, trouxe aqui uma sequencia dele sendoe executado)
<br>
<br>
![Menu Principal](...)
* Menu principal com todas as opções do sistema *

<br>

![

<br>
<br>

#### Pontos que quero melhorar futuramente <br>
- Adicionar buscar por título do livro <br>
- Permitir reservar o livro que está emprestado <br>
- Migrar para SQLite quando o sistema 'crescer' <br>
- Criar interface gráfica com PySide6 / PyQt6 <br>


