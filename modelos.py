# Todas as classes (Livro, usuario, etc.)
# =======================================================================================
# bibliotecas:
from abc import ABC, abstractmethod
from utilidade import carregar_dados as carregar_json, salvar_dados as salvar_json, data_para_string, string_para_data
import json
from datetime import datetime, date, timedelta
from rich.panel import Panel
from rich import print
import os

# =======================================================================================
class ItemBiblioteca(ABC):                  # Classe  ABSTRATA
    """
    Molde para todos os itens da biblioteca 
    """
    def __init__(self, titulo, autor, ano):
        self.__titulo = titulo
        self.__autor = autor
        self.__ano = ano
    
    @property
    def titulo(self):
        return self.__titulo
    
    @property
    def autor(self):
        return self.__autor
    
    @property
    def ano(self):
        return self.__ano
    
    def exibir_info(self):
        """
        Retorna uma string formatada
        """
        return f'|{self.__titulo} - {self.__autor} ({self.__ano})|'
    
    @abstractmethod                         # Método abstrato
    def calcular_multa(self, dias_atraso):
        pass
        

# =======================================================================================
class Livro(ItemBiblioteca):                # Classe FILHA 
    def __init__(self, titulo, autor, ano, id, quantidade):
        super().__init__(titulo, autor, ano)
        self.__id = id
        self.__quantidade = quantidade
        self.__emprestados = 0          # atributo extra privado com qtd de emprest.
    
    @property
    def id(self):
        return self.__id

    @property
    def quantidade(self):
        return self.__quantidade
    
    @property
    def disponiveis(self):
        return self.__quantidade - self.__emprestados

    def emprestar(self):
        """
        Tenta emprestar um exemplar aumentando o __emprestados em 1
        """
        if self.disponiveis > 0:
            self.__emprestados += 1
            return True
        return False
    
    def devolver(self):
        """
        Tenta devolver um exemplar, se tem algum no __emprestados diminui em 1
        """
        if self.__emprestados > 0:
            self.__emprestados -= 1
            return True
        return False
    
    def calcular_multa(self, dias_atraso):          # Implementando o método abstrato
        """
        Calcula multas com base nos dias de atraso, a partir de 7 dias
        """
        if dias_atraso > 7:
            multa = (dias_atraso - 7) * 0.50
            return multa
        else:
            multa = 0
            return multa


# =======================================================================================
class Usuario:                          # Classe USUÁRIO
    """
    Representar tudo que o usuário tem e faz
    """
    def __init__(self, nome, id, telefone):
        self.__nome = nome
        self.__id = id
        self.__telefone = telefone
        self.__multas = 0
        self.__livros_emprestados = []

    @property
    def nome(self):
        return self.__nome
    
    @property
    def id(self):
        return self.__id
    
    @property
    def telefone(self):
        return self.__telefone
    
    @property
    def multas(self):
        return self.__multas
    
    @property
    def livros_emprestados(self):
        return self.__livros_emprestados
    
    @telefone.setter
    def telefone(self, valor):      # Valida telefone
        valor = valor.strip().replace('-', "").replace('(', "").replace(')', "").replace(' ', "")
        if len(valor) != 11 or not valor.isdigit():
            raise ValueError('Telefone deve ter 11 dígitos')
        self.__telefone = valor
    
    #========== Adiciona multa=============
    def adicionar_multa(self, valor):
        if valor > 0:
            self.__multas += valor

    #========== Pagar multa =============
    def pagar_multa(self, valor):
        """paga o valor total"""
        if valor > 0 and valor <= self.__multas:
            self.__multas -= valor
            return True
        return False
    
    #====== Verfica se tem multa  ==========
    def tem_multa(self):
        return self.__multas > 0
    
    #======= Verifica se pode emprestar ===========
    def pode_emprestar(self):
        return not self.tem_multa() and len(self.__livros_emprestados) < 3
    
    #====== Exibe os dados formatados ==========
    def exibir_dados(self, multa_pendente=0):
        multa_total = self.__multas + multa_pendente
        return f' [pale_violet_red1]{self.id:<2}[/]   {self.nome[:38]:<40}  {self.telefone:<12}    [pale_violet_red1]R$ {multa_total:.2f}[/]'

    #===== Empresta livro ================    
    def emprestar_livro(self, livro):
        if self.pode_emprestar():
            self.__livros_emprestados.append(livro)
            return True
        return False
    
    #===== Devolver livro =============
    def devolver_livro(self, livro):
        if livro in self.__livros_emprestados:
            self.__livros_emprestados.remove(livro)
            return True   
        return False
    
# =======================================================================================
class Emprestimo:
    """
    É a ponte entre o usuário e o livro;
    """
    def __init__(self, usuario, livro, data_emprestimo):
        self.__usuario = usuario
        self.__livro = livro
        self.__data_emprestimo = data_emprestimo
        self.__data_devolucao = None

    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def livro(self):
        return self.__livro
    
    @property
    def data_emprestimo(self):
        return self.__data_emprestimo
    
    @property
    def data_devolucao(self):
        return self.__data_devolucao
    
    # ====== Calcula dias em atraso =====
    def calcular_dias_atrasados(self, data_atual):
        if self.__data_devolucao:
            data_final = self.__data_devolucao
        else:
            data_final = data_atual
        dias_com_livro = (data_final - self.__data_emprestimo).days
        dias_atraso = dias_com_livro - 7
        if dias_atraso < 0:
            return 0
        return dias_atraso

    #========= Calcula as multas de cada livro =======
    def calcular_multa(self, data_atual):
        dias_atraso = self.calcular_dias_atrasados(data_atual)
        return self.__livro.calcular_multa(dias_atraso)

    #====== Devolve com tudo feito ja =======
    def devolver(self, data_devolucao):
        self.__data_devolucao = data_devolucao
        self.__livro.devolver()
        multa = self.calcular_multa(data_devolucao)
        if multa > 0:
            self.__usuario.adicionar_multa(multa)
        return multa
        

# =======================================================================================
class Biblioteca:
    """
    Classe principal que gerencia toda  a biblioteca
    """
    def __init__(self, nome):
        self.__nome = nome
        self.__livros = []
        self.__usuarios = []
        self.__emprestimos = []
        self.__prox_id_usuario = 1
        self.__prox_id_livro = 1
        self.carregar_dados()
    
    #==================================================
    def cadastrar_usuario(self, nome, telefone):
        usuario = Usuario(nome, self.__prox_id_usuario, telefone)
        self.__usuarios.append(usuario)
        self.__prox_id_usuario += 1
        self.salvar_dados()
        return usuario
    
    #==================================================
    def buscar_usuario(self, id):
        for usuario in self.__usuarios:
            if usuario.id == id:
                return usuario
        return None
    
    #==================================================
    def listar_usuarios(self, apenas_disponiveis=False):

        if not self.__usuarios:
            return 'Nenhum usuário cadastrado'
        
        # Calcula multas pendentes
        multas_pendentes = {}
        for emp in self.__emprestimos:
            if emp.data_devolucao is None:
                dias = emp.calcular_dias_atrasados(date.today())
                if dias > 0:
                    multa = emp.calcular_multa(date.today())
                    uid = emp.usuario.id
                    multas_pendentes[uid] = multas_pendentes.get(uid, 0) + multa
        
        resultado = f' [pale_violet_red1]{'ID:':<10} {'NOME:':<36} {'TELEFONE:':<13}   {'MULTAS'}[/]\n'
        
        for usuario in self.__usuarios:
            if apenas_disponiveis:
                if usuario.multas > 0 or len(usuario.livros_emprestados) >= 3:
                    continue
            
            # USA O exibir_dados COM A MULTA PENDENTE
            resultado += f'{usuario.exibir_dados(multas_pendentes.get(usuario.id, 0))}\n'
        
        return Panel(resultado, title='👥 USUÁRIOS CADASTRADOS:', width=80, style='bold blue on black')
    
    #================================================        
    def cadastrar_livro(self, titulo, autor, ano, quantidade):
        livro = Livro(titulo, autor, ano, self.__prox_id_livro, quantidade)
        self.__livros.append(livro)
        self.__prox_id_livro += 1
        self.salvar_dados()
        return livro
    
    #=================================================
    def buscar_livro(self, id):
        for liv in self.__livros:
            if liv.id == id:
                return liv
        return None
    
    #====================================================
    def listar_livros_disponiveis(self):

        resultado = ' '
        if not self.__livros:
            resultado += 'Nenhum livro cadastrado'
        
        disponiveis = []
        for liv in self.__livros:
            if liv.disponiveis > 0:
                disponiveis.append(liv)
        
        if not disponiveis:
            resultado += 'Nenhum livro disponível no momento'
        
        resultado = f'[blue1]{'ID'}  {'TÍTULO':<35}  {'AUTOR':<25}{'DISPONIVEL'} [/]\n'
        resultado += '[deep_pink4][bold]_[/][/]' * 75
        
        for livr in disponiveis:
            # Truncar título e autor
            titulo = livr.titulo[:30]
            autor = livr.autor[:20]
            
            resultado += f'\n[blue1]{livr.id}[/].  {titulo:<35}  {autor:<25}    [blue1]{livr.disponiveis}[/]\n'
            resultado += '[deep_pink4][bold]-[/][/]' * 75
        
        c = Panel(resultado, title='📚 LIVROS DISPONÍVEIS:', width=80, style='bold magenta on black')
        print(c)
    
    #=================================================
    def listar_emprestimos_ativos(self):
        ativos = [emp for emp in self.__emprestimos if emp.data_devolucao is None]
        resultado = ' '
        if not ativos:
            resultado += "Nenhum empréstimo ativo"

        resultado += f"[orange4]{'ID.'}    {' USUÁRIO':<27}{'LIVRO':<27}{'EMPRÉSTIMO':<13}[/]\n"
        for emp in ativos:
            id_livro = emp.livro.id
            usuario = emp.usuario.nome[:27]
            livro = emp.livro.titulo[:27]
            data = emp.data_emprestimo.strftime('%d/%m/%Y')
            resultado += f"\n [orange4][bold]{id_livro}[/][/]. {usuario:<28}[orange4]   {livro:<27}[/] {data:<13}\n"
            resultado += '[orange4][bold]-[/][/]'*73

        print(Panel(resultado, title='📋 EMPRÉSTIMOS ATIVOS', width=80, style='bold cyan on black'))
    
    #====================================================
    def emprestar_livro(self, usuario_id, livro_id, data):
    
        usuario = self.buscar_usuario(usuario_id)
        livro = self.buscar_livro(livro_id)
        
        if usuario is None:
            return None, '[yellow1][bold]Usuário não encontrado[/][/]'
        if livro is None:
            return None, '[yellow1][bold]Livro não encontrado[/][/]'
        
        # CALCULA MULTAS PENDENTES EM 'TEMPO REAL'
        multas_pendentes = 0.0
        for emp in self.__emprestimos:
            if emp.usuario.id == usuario_id and emp.data_devolucao is None:
                dias_atraso = emp.calcular_dias_atrasados(date.today())
                if dias_atraso > 0:
                    multa = emp.calcular_multa(date.today())
                    multas_pendentes += multa
        
        if multas_pendentes > 0:
            return None, f'[red]Usuário com multa pendente de R$ {multas_pendentes:.2f}! Não pode emprestar.[/]'
        
        # CONTA QUANTOS LIVROS O USUÁRIO TEM EMPRESTADOS EM TEMPO REAL
        quantidade_livros_usuario = 0
        for emp in self.__emprestimos:
            if emp.usuario.id == usuario_id and emp.data_devolucao is None:
                quantidade_livros_usuario += 1
        
        if quantidade_livros_usuario >= 3:
            return None, '[red][bold]Usuário já tem 3 livros emprestados! Não pode pegar mais.[/][/]'
        
        if livro.disponiveis <= 0:
            return None, '[red][bold]Livro sem exemplares disponíveis[/][/]'
        
        # Realiza o empréstimo
        livro.emprestar()
        emprestimo = Emprestimo(usuario, livro, data)
        usuario.emprestar_livro(livro)
        self.__emprestimos.append(emprestimo)
        self.salvar_dados()
        
        return emprestimo, f'Empréstimo realizado com sucesso para [bold]{usuario.nome}[/]'

    #=========================================================
    def devolver_livro(self, usuario_id, livro_id, data_devolucao):
        """Devolve um livro verificando o usuário também"""
        livro = self.buscar_livro(livro_id)
        usuario = self.buscar_usuario(usuario_id)
        
        if livro is None:
            return None, '[yellow1][bold]Livro não encontrado[/][/]'
        if usuario is None:
            return None, '[yellow1][bold]Usuário não encontrado[/][/]'
    
        # Procura o empréstimo ativo deste usuário com este livro
        for emp in self.__emprestimos:
            if (emp.livro.id == livro_id and 
                emp.usuario.id == usuario_id and 
                emp.data_devolucao is None):
                
                multa = emp.devolver(data_devolucao)
                self.__emprestimos.remove(emp)
                livro.devolver()
                emp.usuario.devolver_livro(livro)
                # print(f'debug: mult calculada = {multa}')
                # print(f'debug: multa do usuario agora= {emp.usuario.multas}')
                self.salvar_dados()
                return multa, f'[bold]Devolução realizada! Multa: R$ {multa:.2f}[/]\n'
        
        return None, '[yellow1][bold]Empréstimo não encontrado para este usuário e livro[/][/]'
    
    #=================================================
    def salvar_dados(self):

        usuarios_dict = []
        for usuario in self.__usuarios:
            usuarios_dict.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'telefone': usuario.telefone,
                'multas': usuario.multas
            })
        
        livros_dict = []
        for livro in self.__livros:
            livros_dict.append({
                'id': livro.id,
                'titulo': livro.titulo,
                'autor': livro.autor,
                'ano': livro.ano,
                'quantidade': livro.quantidade
            })
        
        emprestimos_dict = []
        for emp in self.__emprestimos:
            data_emp_str = emp.data_emprestimo.strftime('%Y-%m-%d') if emp.data_emprestimo else None
            data_dev_str = emp.data_devolucao.strftime('%Y-%m-%d') if emp.data_devolucao else None
            emprestimos_dict.append({
                'usuario_id': emp.usuario.id,
                'livro_id': emp.livro.id,
                'data_emprestimo': data_emp_str,
                'data_devolucao': data_dev_str
            })
        
        dados = {
            'usuarios': usuarios_dict,
            'livros': livros_dict,
            'emprestimos': emprestimos_dict,
            'prox_id_usuario': self.__prox_id_usuario,
            'prox_id_livro': self.__prox_id_livro
        }
        
        salvar_json(dados, 'biblioteca.json')
    
    #====================================================
    def carregar_dados(self):

        dados = carregar_json('biblioteca.json')
        if not dados:
            return
        
        # Carregar usuários
        for u in dados.get('usuarios', []):
            usuario = Usuario(u['nome'], u['id'], u['telefone'])
            usuario._Usuario__multas = u.get('multas', 0.0)
            self.__usuarios.append(usuario)
            # print(f'debug= carregando usuario {usuario.nome} com multa {usuario.multas}')
        
        # Carregar livros 
        for l in dados.get('livros', []):
            livro = Livro(l['titulo'], l['autor'], l['ano'], l['id'], l['quantidade'])
            self.__livros.append(livro)
        
        # Carregar empréstimos
        for e in dados.get('emprestimos', []):
            usuario = self.buscar_usuario(e['usuario_id'])
            livro = self.buscar_livro(e['livro_id'])
            if usuario and livro:
                data_emp = datetime.strptime(e['data_emprestimo'], '%Y-%m-%d').date()
                emprestimo = Emprestimo(usuario, livro, data_emp)
                if e.get('data_devolucao'):
                    data_dev = datetime.strptime(e['data_devolucao'], '%Y-%m-%d').date()
                    emprestimo._Emprestimo__data_devolucao = data_dev
                self.__emprestimos.append(emprestimo)
        
        self.__prox_id_usuario = dados.get('prox_id_usuario', 1)
        self.__prox_id_livro = dados.get('prox_id_livro', 1)

    #=================================================
    def simular_tempo(self, dias):
        """
        AVANÇA a data dos empréstimos para testar multas.
        Soma os dias aos empréstimos existentes.
        """
        
        if not self.__emprestimos:
            return "Nenhum empréstimo ativo para simular"
        
        # Mostra situação atual
        print("\n📊 SITUAÇÃO ATUAL DOS EMPRÉSTIMOS:")
        for emp in self.__emprestimos:
            dias_atual = emp.calcular_dias_atrasados(datetime.now().date())
            status = "🔴 ATRASADO" if dias_atual > 0 else "🟢 NO PRAZO"
            print(f"   {emp.livro.titulo:<30} - {dias_atual} dias - {status}")
        
        # Avança os dias (subtrai da data de empréstimo para simular passagem de tempo)
        for emp in self.__emprestimos:
            nova_data = emp.data_emprestimo - timedelta(days=dias)
            emp._Emprestimo__data_emprestimo = nova_data
        
        self.salvar_dados()
        
        # Mostra situação nova
        print(f"\n✅ SIMULAÇÃO REALIZADA! +{dias} dias")
        print("\n📊 NOVA SITUAÇÃO DOS EMPRÉSTIMOS:")
        for emp in self.__emprestimos:
            dias_novo = emp.calcular_dias_atrasados(datetime.now().date())
            multa = emp.calcular_multa(datetime.now().date())
            print(f"   {emp.livro.titulo:<30} - {dias_novo} dias - Multa: R$ {multa:.2f}")
        
        return "Simulação concluída"
    
    #=========================================================
    def verificar_multas(self):
        """ para teste"""

        print('\n Verificando...')
        # for u in self.__usuarios:
            # print(f'usuario: {u.nome} | Multa: R${u.multas:.2f}')

    #======================================================
    def gerar_etiqueta_emprestimo(self, usuario, livro, data):

        data_formatada = data.strftime("%d/%m/%Y")
        hora_formatada = datetime.now().strftime("%H:%M:%S")
    
        etiqueta = f"""
   
    | [red]Usuário:[/] {usuario.nome[:35]}                             
    | [red]ID Usuário:[/] {usuario.id}                                    
    | [red]Livro:[/] {livro.titulo[:35]}                                  
    | [red]ID Livro:[/] {livro.id}                                        
    | [red]Data:[/] {data_formatada}
    | [red]Hora:[/] {hora_formatada} 
                                           
    """
        p = Panel(etiqueta, title='COMPROVANTE DE EMPRÉSTIMO', width=50, style='bold on black')
        return p
    
    #===============================================
    def gerar_etiqueta_devolucao(self, usuario, livro, multa, data_devolucao):
        """Gera uma etiqueta/recibo de devolução"""
        
        data_formatada = data_devolucao.strftime("%d/%m/%Y")
        hora_formatada = datetime.now().strftime("%H:%M:%S")
        
        if multa > 0:
            status_multa = f"[red]💰 MULTA APLICADA: R$ {multa:.2f}[/]"
            status_livro = "[yellow]📖 LIVRO DEVOLVIDO COM ATRASO[/]"
        else:
            status_multa = "[green]✅ NENHUMA MULTA APLICADA[/]"
            status_livro = "[green]📖 LIVRO DEVOLVIDO NO PRAZO[/]"
        
        etiqueta = f"""
    [bold cyan]| USUÁRIO:[/] {usuario.nome[:48]}                        
    [bold cyan]| ID DO USUÁRIO:[/] {usuario.id}
    [bold cyan]| LIVRO:[/] {livro.titulo[:48]}
    [bold cyan]| ID DO LIVRO:[/] {livro.id}
    [bold cyan]| DATA DA DEVOLUÇÃO:[/] {data_formatada}
    [bold cyan]| HORA:[/] {hora_formatada}
    [bold cyan]|[/]   {status_livro}
    [bold cyan]|[/]   {status_multa}
    """
        return Panel(etiqueta, title="📋COMPROVANTE DE DEVOLUÇÃO", width=50, style="bold on black")
    
#=======================================================================================