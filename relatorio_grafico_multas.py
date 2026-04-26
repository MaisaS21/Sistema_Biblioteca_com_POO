#========================================================================================
#Arquivo exclusivo para criar o gráfico de pizza, com cores e layout personalizado.
#========================================================================================
#Bibliotecas:
import matplotlib.pyplot as plt
from datetime import date
from rich import print
from rich.panel import Panel
#========================================================================================

def gerar_grafico_multas(biblioteca):
    """
    Gera gráfico de pizza com tamanho automático conforme número de usuários;
    Possui legenda bem intuitiva;
    """

    # Dicionário para acumular multas por usuário
    multas_por_usuario = {}
    
    # Primeiro, se tiver multa registrada, adiciona ao dicionário com o nome como chave
    for usuario in biblioteca._Biblioteca__usuarios:
        if usuario.multas > 0:
            multas_por_usuario[usuario.nome] = usuario.multas
    
    # Depois, calcula as multas pendentes (usuários com livro atrasado)
    for emp in biblioteca._Biblioteca__emprestimos:
        if emp.data_devolucao is None:  # Ainda não devolveu
            dias_atraso = emp.calcular_dias_atrasados(date.today())
            if dias_atraso > 0:
                multa_pendente = emp.calcular_multa(date.today())
                nome = emp.usuario.nome
                
                if nome in multas_por_usuario:
                    multas_por_usuario[nome] += multa_pendente
                else:
                    multas_por_usuario[nome] = multa_pendente
    
    if not multas_por_usuario:
        print("\n📊 Nenhuma multa pendente ou paga!")
        return
    
    # Ordena com maior multa primeiro
    itens_ordenados = sorted(multas_por_usuario.items(), key=lambda x: x[1], reverse=True)
    
    usuarios = []
    valores = []
    for nome, valor in itens_ordenados:
        usuarios.append(nome)
        valores.append(valor)
    
    total = sum(valores)
    qtd_usuarios = len(usuarios)
    
    # ===== TAMANHO AUTOMÁTICO BASEADO NA QUANTIDADE =====
    if qtd_usuarios <= 5:           # pequeno
        figsize = (9, 5)              #-> (largura, altura)
        legend_fontsize = 8           #-> Tamanho da fonte na legenda
        title_fontsize = 11           #-> tamanho da fonte do titulo
    elif qtd_usuarios <= 8:
        figsize = (10, 6)     # médio
        legend_fontsize = 7.5
        title_fontsize = 11
    elif qtd_usuarios <= 12:
        figsize = (12, 7)     # grande
        legend_fontsize = 7
        title_fontsize = 10
    else:
        figsize = (14, 8)     # extra grande
        legend_fontsize = 6.5
        title_fontsize = 10
    
    # ===== CONFIGURAÇÃO DO GRÁFICO =====
    fig, ax = plt.subplots(figsize=figsize)
    
    # Cores de fundo
    COR_FUNDO_JANELA = '#2c2c2c'      # Cor da janela   (cinza escuro)
    COR_FUNDO_GRAFICO = '#faf0e6'     # Cor do fundo do gráfico (bege)
    
    fig.patch.set_facecolor(COR_FUNDO_JANELA)       # Aplica a cor ao fundo
    ax.set_facecolor(COR_FUNDO_GRAFICO)             # Aplica a cor à área do gráfico
    
    # Cores das fatias(se houver mais usuáriso que cores, ele repete)
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#F0A3A3', '#9B59B6', '#F39C12', '#E74C3C']
    
    # Cria o gráfico de pizza
    wedges, texts, autotexts = ax.pie(
        valores,                # Dados a serem exibidos
        labels=None,            # Não mostra labels diretamente no gráfico
        autopct='%1.1f%%',      # Mostra percentual formatado ex: '25.5%'
        startangle=90,          # Primeira fatia começa com ângulo de 90º 
        colors=cores[:qtd_usuarios],    # Seleciona cores para o números de usuários
        pctdistance=0.75,       # Distância d percentual do centro
        textprops={'fontsize': 10, 'fontweight': 'bold'}  # estilo de texto tamanho(10, negrito)
    )
    
    # Estilo das porcentagens
    for autotext in autotexts:
        autotext.set_color('#2c3e50')   # Cor do texto do percentual (azul escuro)
        autotext.set_fontsize(9)        # Tamanho da fonte 9
        autotext.set_fontweight('bold') # Texto em negrito
        autotext.set_bbox(dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none')) # Cria uma caixa branca ao redor do texto(fundo semi-transparente)
    
    # ===== LEGENDA COM NOMES COMPLETOS =====
    # Cria lita de strings para legenda com nome de usuario, valor da multa e percentual sobre o total.
    legend_labels = []
    for nome, valor in zip(usuarios, valores):  #zip juntas as 2 listas em pares nome e valor
        porcentagem = (valor / total) * 100
        legend_labels.append(f"{nome}\n   R$ {valor:.2f} ({porcentagem:.1f}%)")
    
    legend = ax.legend(             # Chama método matplotlib para criar legendas
        wedges,             # As fatias do gráfico para associar com as cores
        legend_labels,      # Texto da legenda
        title=" USUÁRIOS",  #Titulo da legenda
        loc="center left",  # Posição da legenda( lado esquerdo central)
        bbox_to_anchor=(1.0, 0.5),  # Para posicionar fora do gráfico
        fontsize=legend_fontsize,   # Define tamanho da fonte dos itens da legenda
        title_fontsize=10,          # Tamanho da fonte do título
        frameon=True,       # Borda na legenda 
        facecolor='white',  # Cor de fundo para 'white'
        edgecolor='#cccccc',    # Cor da borda da legenda (cinza claro)
        shadow=True,            #Adiciona sombra atrás da legenda ( é tipo um 3D sutil)
        handlelength=0.5,       # Quadrados coloridos de associar gráfico a legenda
        handletextpad=0.8,      # Define espaço entre quadrado colorido e texto legenda
        labelspacing=0.6       # Define espaço vertical entre um item e outro  na legenda
    )
    
    # Ajusta o título
    ax.set_title(   # Chama método do matplotlib para definir titulo do grafico
        f' MULTAS POR USUÁRIO\nTotal: R$ {total:.2f}', 
        fontsize=title_fontsize, 
        fontweight='bold',
        color='#faf9f6',        # Cor do título (branco)
        pad=15  # Adicina espaçamento entre o título e o gráfico
    )
    
    # Ajusta o layout para caber tudo
    plt.tight_layout()  
    
    # Salva e mostra
    nome_arquivo = 'grafico_multas.png'
    plt.savefig(nome_arquivo, dpi=120, bbox_inches='tight', facecolor=COR_FUNDO_JANELA) #DPI é a resolução da imagem maior para mais qualidade
    plt.show()  # Abre uma janela para o gráfico
    t = f"✅ [red]GRÁFICO DE MULTAS[/] gerado com sucesso"
    p = Panel(t, width=40, style='bold green on black')
    print(p)

#========================================================================================