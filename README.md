# Sistema_Biblioteca_com_POO
--> Versão atualizada do sistema bibliotecario desenvolvido utilizando programação orientada a objetos.
Trata-se de um sistema feito para praticar os conhecimentos adquiridos com a POO.


### Conceitos de POO aplicados
| **Conceito** | **Exemplo no código** |
|----------|-------------------|
| **ENCAPSULAMENTO** | Atributos privados(__titulo, __saldo) com getters/setters|
| **HERANÇA** | class Livro(ItemBiblioteca)|
| **ABSTRAÇÃO** | class ItemBiblioteca(ABC) com método @abstractmethod|
| **POLIMORFISMO** | Método calcular_multa() implementado de forma diferente por classe|




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





| Pagamento de multas | Interface administrativa com senha ('admin123') |
| Simular tempo | Avança datas para testar cálculo de multas |
