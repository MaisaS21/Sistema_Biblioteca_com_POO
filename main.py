# ARQUIVO PRINCIPAL
#=======================================================================================
#bibliotecas:
from rich import inspect
from rich import print as rprint
from rich.panel import Panel
from modelos import Biblioteca
from utilidade import carregar_dados, salvar_dados, leia_string, leia_telefone, leiaint, verificar_senha
from datetime import date
from time import sleep
from exportadores import exportar_excel, exportar_pdf
from relatorio_grafico_multas import gerar_grafico_multas

#=======================================================================================
def pagar_multas_usuario(biblioteca):
    """Função para administrador pagar multas de um usuário"""
    
    rprint("\n[bold yellow]💰 PAGAMENTO DE MULTAS - MODO ADMIN[/]")
    
    # Verifica senha
    if not verificar_senha():
        return
    
    # CALCULA MULTAS PENDENTES EM TEMPO REAL
    multas_pendentes_por_usuario = {}
    emprestimos_com_multa = []  # Guarda os empréstimos que têm multa
    
    for emp in biblioteca._Biblioteca__emprestimos:
        if emp.data_devolucao is None:
            dias_atraso = emp.calcular_dias_atrasados(date.today())
            if dias_atraso > 0:
                multa = emp.calcular_multa(date.today())
                nome = emp.usuario.nome
                if nome in multas_pendentes_por_usuario:
                    multas_pendentes_por_usuario[nome] += multa
                else:
                    multas_pendentes_por_usuario[nome] = multa
                emprestimos_com_multa.append(emp)
    
    # Adiciona multas já registradas
    for u in biblioteca._Biblioteca__usuarios:
        if u.multas > 0:
            if u.nome in multas_pendentes_por_usuario:
                multas_pendentes_por_usuario[u.nome] += u.multas
            else:
                multas_pendentes_por_usuario[u.nome] = u.multas
    
    if not multas_pendentes_por_usuario:
        rprint("\n[green][bold]✅ Nenhum usuário com multa pendente![/][/]")
        input("\nPressione Enter...")
        return
    
    # Mostra usuários com multa
    usuarios_lista = []
    p = ' '
    for i, (nome, valor) in enumerate(multas_pendentes_por_usuario.items(), 1):
        p += f"\n [blue3]{i}[/].  {nome[:35]:<38} - [blue3]MULTA[/]: R$ {valor:.2f}"
        usuarios_lista.append((nome, valor))
    
    tudo = Panel(p, title='📋 USUÁRIOS COM MULTA PENDENTE:', width=70, style='bold red on black')
    rprint(tudo)

    # Escolhe o usuário
    rprint('\n[blue3][bold]Escolha o número do usuário:[/][/] ', end=' ')
    escolha = leiaint(" ", tentativas=3)
    if escolha is None or escolha < 1 or escolha > len(usuarios_lista):
        rprint("[red]❌ Opção inválida![/]")
        input("\nPressione Enter...")
        return
    
    nome_usuario, valor_multa = usuarios_lista[escolha - 1]
    
    # Encontra o objeto usuário
    usuario = None
    for u in biblioteca._Biblioteca__usuarios:
        if u.nome == nome_usuario:
            usuario = u
            break
    
    if usuario is None:
        rprint("[red]❌ Usuário não encontrado![/]")
        input("\nPressione Enter...")
        return
    
    print(' ')
    # Confirma pagamento
    r = ' '
    r += f"[dark_cyan][bold]👤[purple] Usuário:[/] {usuario.nome[:33]:<35}[/][/]\n"
    r += f"\n 💰[dark_cyan][bold] [purple]Multa total:[/] R$ {valor_multa:<35.2f}[/][/]"
    rprint(Panel(r, width=60, style='purple on black'))
    
    rprint('\n[blue3][bold]Deseja confirmar o pagamento? (s/n):[/]', end=' ')
    confirmar = input(" ").lower()
    if confirmar == 's':
        # VERIFICA QUANTOS LIVROS O USUÁRIO TEM
        livros_com_usuario = 0
        for emp in biblioteca._Biblioteca__emprestimos:
            if emp.usuario.id == usuario.id and emp.data_devolucao is None:
                livros_com_usuario += 1
        
        # Paga as multas registradas
        if usuario.multas > 0:
            usuario.pagar_multa(usuario.multas)
        
        # Ajusta a data dos empréstimos atrasados (zera a multa pendente)
        for emp in biblioteca._Biblioteca__emprestimos:
            if emp.usuario.id == usuario.id and emp.data_devolucao is None:
                dias_atraso = emp.calcular_dias_atrasados(date.today())
                if dias_atraso > 0:
                    nova_data = date.today()
                    emp._Emprestimo__data_emprestimo = nova_data
        
        biblioteca.salvar_dados()
        rprint(f"[green]✅ Pagamento de R$ {valor_multa:.2f} realizado com sucesso![/]")
        
        if livros_com_usuario >= 3:
            rprint(f"[yellow]⚠️ {usuario.nome} ainda tem {livros_com_usuario}/3 livros emprestados![/]")
            rprint(f"[yellow]Para pegar outro livro, deve devolver pelo menos 1 primeiro.[/]")
        else:
            rprint(f"[green]✅ Agora [bold]{usuario.nome}[/] está [bold]autorizado[/] a pegar livros novamente![/]")
    else:
        rprint('              [red][bold]======> Pagamento cancelado <======[/][/]\n')

#========================================================================================
def mostrar_menu():
    """
    Mostra o menu estilizado em formato de painel
    """

    menu = """

        [red]1[/]  -->  Cadastrar Usuário
        [red]2[/]  -->  Cadastrar Livro
        [red]3[/]  -->  Emprestar Livro
        [red]4[/]  -->  Devolver Livro
        [red]5[/]  -->  Listar Usuários
        [red]6[/]  -->  Listar Livros Disponíveis
        [red]7[/]  -->  Listar Empréstimos Ativos
        [red]8[/]  -->  Exportar Excel
        [red]9[/]  -->  Exportar PDF
        [red]10[/] -->  Gráfico de Multas
        [red]11[/] -->  Simular tempo
        [red]12[/] -->  Pagar multa(adm)
        [red]0[/]  -->  Sair
        """
    xo = Panel(menu,title='[bold]📚 SISTEMA DE BIBLIOTECA (POO)[/]', width=60, style='bold green on black')
    rprint(xo)

# ======================================================================================
def main():
    """
    Função principal, organiza o menu de forma a jogar a informação/ação conforme a escolha do usuário;
    """

    
    # Cria a biblioteca
    biblioteca = Biblioteca("Minha Biblioteca")
    
    while True:
        sleep(1)
        mostrar_menu()
        rprint('[yellow1]\nEscolha uma opção:[/] ', end=' ')
        opcao = input().strip()
        
        # ===== OPÇÃO 1: CADASTRAR USUÁRIO =====
        if opcao == "1":
            rprint('\n[deep_pink1]NOME:[/] ',end=' ' )
            nome = leia_string(' ').title()
            if nome == None:
                rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')
            else:
                rprint("[deep_pink1]TELEFONE ([bold]11 dígitos[/]):[/] ", end=' ')
                telefone = leia_telefone(' ')
                if telefone == None:
                    rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')
                else:
                    try:
                        usuario = biblioteca.cadastrar_usuario(nome, telefone)
                        rprint(f"\n[green]✅ Usuário {usuario.nome} cadastrado com ID {usuario.id}![/]\n")
                        rprint('Pressione Enter...', end=' ')
                        input()
                    except:
                        rprint('[navajo_white3]Voltando ao menu...[/]')
        
        # ===== OPÇÃO 2: CADASTRAR LIVRO =====
        elif opcao == "2":
            rprint("[blue3][bold]TÍTULO:[/][/]  ",end=' ')
            titulo = leia_string(" ").title()
            if titulo == None:
                rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')            
            else:
                rprint("[blue3][bold]AUTOR:[/][/]  ",end=' ')
                autor = leia_string(" ").title()
                if autor == None:
                    rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')
                else:
                    rprint("[blue3][bold]ANO:[/][/]  ",end=' ')
                    ano = leiaint(" ")
                    if ano == None:
                        rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')
                    else:
                        rprint("[blue3][bold]QUANTIDADE:[/][/]  ",end=' ')
                        quantidade = leiaint(' ')
                        if quantidade == None:
                            rprint('              [red][bold]======> Cadastro cancelado <======[/][/]\n')
                        else:
            
                            livro = biblioteca.cadastrar_livro(titulo, autor, ano,quantidade)
                            rprint(f"[green]✅ Livro '{livro.titulo}' cadastrado com ID {livro.id}![/]")
                            rprint('Pressione Enter...', end=' ')
                            input()
                
        
        # ===== OPÇÃO 3: EMPRESTAR LIVRO =====
        elif opcao == "3":
            resultado = biblioteca.listar_usuarios()
            rprint(resultado)
            rprint("\n[spring_green3][bold]ID do usuário:[/][/] ",end=' ')
            usuario_id = leiaint(' ')
            if usuario_id == None:
                rprint('              [red][bold]======> Operação cancelada <======[/][/]\n')
            else:
                resultado = biblioteca.listar_livros_disponiveis()
                rprint(resultado)
                rprint("[spring_green3][bold]ID do livro:[/][/] ", end=' ')
                livro_id = leiaint(' ')
                if livro_id == None:
                    rprint('              [red][bold]======> Operação cancelada <======[/][/]\n')
                else:
                    data = date.today()
            
                    emprestimo, mensagem = biblioteca.emprestar_livro(usuario_id, livro_id, data)
            
                    if emprestimo:
                        rprint('\nGuarde o comprovante de empréstimo, você necessitará destes IDs.\n')
                        usuario = biblioteca.buscar_usuario(usuario_id)
                        livro = biblioteca.buscar_livro(livro_id)
                        rprint(biblioteca.gerar_etiqueta_emprestimo(usuario, livro, data))
                        rprint('\nPressione Enter...', end=' ')
                        input()
                    else:
                        rprint(f"[red]❌ {mensagem}[/]\n")
                        rprint('\nPressione Enter...', end=' ')
                        input()
        
        # ===== OPÇÃO 4: DEVOLVER LIVRO =====
        elif opcao == "4":
            print(' ')
            resultado = biblioteca.listar_usuarios()
            rprint(resultado)
            rprint('\n[dark_slate_gray2][bold]ID do usuário que está devolvendo:[/][/] ',end=' ')
            usuario_id = leiaint(' ')
            if usuario_id is None:
                rprint('              [red][bold]======> Operação cancelada <======[/][/]\n')
            else:
                print(' ')
                biblioteca.listar_emprestimos_ativos()
                rprint("[dark_slate_gray2][bold]ID do livro:[/][/] ", end=' ')
                livro_id = leiaint(' ')
                print(' ')
                if livro_id is None:
                    rprint('              [red][bold]======> Operação cancelada <======[/][/]\n')
                else:
                    data = date.today()
                    multa, mensagem = biblioteca.devolver_livro(usuario_id, livro_id, data)
                    
                    if multa is not None:
                        rprint(f"[green]✅ {mensagem}[/]")
                        usuario = biblioteca.buscar_usuario(usuario_id)
                        livro = biblioteca.buscar_livro(livro_id)
                        if usuario and livro:
                            rprint(biblioteca.gerar_etiqueta_devolucao(usuario, livro , multa, data))
                    else:
                        rprint(f"[red]❌ {mensagem}[/]")
        
        # ===== OPÇÃO 5: LISTAR USUÁRIOS =====
        elif opcao == "5":
            print(' ')
            resultado = biblioteca.listar_usuarios()
            rprint(resultado)
            print(' ')
            input('Pressione Enter...')
        
        # ===== OPÇÃO 6: LISTAR LIVROS DISPONÍVEIS =====
        elif opcao == "6":
            print(' ')
            biblioteca.listar_livros_disponiveis()
            print(' ')
            input('Pressione Enter...')
            
        
        # ===== OPÇÃO 7: LISTAR EMPRÉSTIMOS ATIVOS =====
        elif opcao == "7":
            print(' ')
            biblioteca.listar_emprestimos_ativos()
            rprint('\nPressione Enter...',end=' ')
            input()

        # ===== OPÇÃO 0: SAIR =====
        elif opcao == "0":
            rprint("\n[bold green]📚 Dados salvos! Saindo do sistema...[/]")
            break

        #===== OPÇÃO 8: EXPORTAR PARA EXCEL ======
        elif opcao == "8":
            print(' ')
            exportar_excel(biblioteca)
            print(' ')
            input('Pressione Enter...')

        #===== OPÇÃO 9: EXPORTAR PARA PDF ===========
        elif opcao == "9":
            print(' ')
            exportar_pdf(biblioteca)

            print(' ')
            input('Pressione Enter...')

        #====== OPÇÃO 10: GERA O GRÁFICO DE MULTAS =========
        elif opcao == "10":
            print(' ')
            gerar_grafico_multas(biblioteca)
            print(' ')
            input('Pressione Enter...')

        #======= Autorizar liberação de multa==========
        elif opcao == '12':
            pagar_multas_usuario(biblioteca)
        
        # ===== OPÇÃO INVÁLIDA =====
        elif opcao == "11":
            try:
                dias = int(input("Quantos dias deseja avançar? "))
                if dias <= 0:
                    rprint("[red]❌ Digite um número positivo![/]")
                else:
                    resultado = biblioteca.simular_tempo(dias)
                    rprint(f"[yellow]📅 {resultado}[/]")
                    
                    # Mostrar multas pendentes após simulação
                    print("\n📊 MULTAS PENDENTES APÓS SIMULAÇÃO:")
                    for emp in biblioteca._Biblioteca__emprestimos:
                        if emp.data_devolucao is None:
                            dias_atraso = emp.calcular_dias_atrasados(date.today())
                            if dias_atraso > 0:
                                multa = emp.calcular_multa(date.today())
                                print(f"   {emp.usuario.nome} deve R$ {multa:.2f} pelo livro {emp.livro.titulo}")
            except ValueError:
                rprint("[red]❌ Digite um número válido![/]")
        else:
            rprint('\n [red][bold]Opção inválida, escolha o que quer fazer digitando entre 0 e 11![/][/]n')

# =======================================================================================
# EXECUTAR O PROGRAMA
if __name__ == "__main__":
    main()
#========================================================================================