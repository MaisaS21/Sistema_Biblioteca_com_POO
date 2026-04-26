#=======================================================================================
# Arquivo exclusivo para criar os exportadores de PDF e EXCEL personalizados
#=======================================================================================
# Bibliotecas
import pandas as pd
from fpdf import FPDF
from rich.panel import Panel
from datetime import date, datetime
from rich import print
import os
from rich.progress import track  
import time 
 
#========================================================================================
def exportar_pdf(biblioteca, nome_arquivo="relatorio_biblioteca.pdf"):
    """Exporta os dados da biblioteca para PDF (completo)"""
    
    #  BARRA DE PROGRESSO (SÓ VISUAL - ANTES DE COMEÇAR)
    print('\n[green]Preparando arquivo...[/]\n')
    for i in track(range(40), description="[cyan]📄 Gerando PDF..."):
        time.sleep(0.02)  
        if i == 15:
            print("[yellow]   ⏳ Coletando dados...[/]")
        if i == 30:
            print("[yellow]   ⏳ Montando páginas...[/]")
    
    #  CALCULA MULTAS PENDENTES EM TEMPO REAL (SEM PRECISAR DEVOLVER)
    multas_pendentes_por_usuario = {}
    for emp in biblioteca._Biblioteca__emprestimos:
        if emp.data_devolucao is None:
            dias_atraso = emp.calcular_dias_atrasados(date.today())
            if dias_atraso > 0:
                multa = emp.calcular_multa(date.today())
                uid = emp.usuario.id
                multas_pendentes_por_usuario[uid] = multas_pendentes_por_usuario.get(uid, 0) + multa
    
    pdf = FPDF()
    pdf.add_page()      # Adiciona uma página ao PDF
    
    # ===== TÍTULO =====
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "RELATÓRIO DA BIBLIOTECA", ln=True, align="C")  # Cria uma célula com largura automática e altura de 10mm, após célula pula p/ próxima linha, alinha centralizado.
    pdf.ln(5)   # Pula 5mm para baixo
    
    # ===== DATA =====
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 5, f"Gerado em: {date.today().strftime('%d/%m/%Y')}", ln=True, align="R")
    pdf.ln(10)
    
    # ===== ESTATÍSTICAS GERAIS =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "ESTATÍSTICAS GERAIS", ln=True)
    pdf.set_font("Arial", "", 10)

    # Calcula total de usuários cadastrados, soma qtd de exemplares, conta qtd de títulos diferentes tem, soma multas, empréstimos ativos.
    total_usuarios = len(biblioteca._Biblioteca__usuarios)
    total_livros = sum(l.quantidade for l in biblioteca._Biblioteca__livros)
    total_titulos = len(biblioteca._Biblioteca__livros)
    total_emprestimos = len([e for e in biblioteca._Biblioteca__emprestimos if e.data_devolucao is None])
    total_multas_registradas = sum(u.multas for u in biblioteca._Biblioteca__usuarios)
    total_multas_pendentes = sum(multas_pendentes_por_usuario.values())
    total_multas_geral = total_multas_registradas + total_multas_pendentes
    
    pdf.cell(0, 6, f"Total de usuários cadastrados: {total_usuarios}", ln=True)
    pdf.cell(0, 6, f"Total de livros no acervo: {total_livros} exemplares", ln=True)
    pdf.cell(0, 6, f"Total de títulos: {total_titulos}", ln=True)
    pdf.cell(0, 6, f"Empréstimos ativos: {total_emprestimos}", ln=True)
    pdf.cell(0, 6, f"Total de multas (registradas + pendentes): R$ {total_multas_geral:.2f}", ln=True)
    pdf.ln(10)
    
    # ===== LIVROS CADASTRADOS =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "LIVROS CADASTRADOS", ln=True)
    pdf.set_font("Arial", "B", 9)
    
    pdf.cell(15, 8, "ID", 1)
    pdf.cell(70, 8, "TÍTULO", 1)
    pdf.cell(50, 8, "AUTOR", 1)
    pdf.cell(20, 8, "ANO", 1)
    pdf.cell(25, 8, "DISP./TOTAL", 1)
    pdf.ln()
    
    pdf.set_font("Arial", "", 8)
    for l in biblioteca._Biblioteca__livros:
        pdf.cell(15, 7, str(l.id), 1)
        pdf.cell(70, 7, l.titulo[:30], 1)
        pdf.cell(50, 7, l.autor[:20], 1)
        pdf.cell(20, 7, str(l.ano), 1)
        pdf.cell(25, 7, f"{l.disponiveis}/{l.quantidade}", 1)
        pdf.ln()
    pdf.ln(8)
    
    # ===== USUÁRIOS CADASTRADOS (COM MULTAS PENDENTES) =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "USUÁRIOS CADASTRADOS", ln=True)
    pdf.set_font("Arial", "B", 9)
    
    pdf.cell(15, 8, "ID", 1)
    pdf.cell(70, 8, "NOME", 1)
    pdf.cell(50, 8, "TELEFONE", 1)
    pdf.cell(30, 8, "MULTAS", 1)
    pdf.ln()
    
    pdf.set_font("Arial", "", 8)
    for u in biblioteca._Biblioteca__usuarios:
        multa_total = u.multas + multas_pendentes_por_usuario.get(u.id, 0)
        pdf.cell(15, 7, str(u.id), 1)
        pdf.cell(70, 7, u.nome[:25], 1)
        pdf.cell(50, 7, u.telefone, 1)
        pdf.cell(30, 7, f"R$ {multa_total:.2f}", 1)
        pdf.ln()
    pdf.ln(8)
    
    # ===== EMPRÉSTIMOS ATIVOS =====
    ativos = [e for e in biblioteca._Biblioteca__emprestimos if e.data_devolucao is None]
    if ativos:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "EMPRÉSTIMOS ATIVOS", ln=True)
        pdf.set_font("Arial", "B", 9)
        
        pdf.cell(60, 8, "USUÁRIO", 1)
        pdf.cell(60, 8, "LIVRO", 1)
        pdf.cell(40, 8, "DATA EMPRÉSTIMO", 1)
        pdf.ln()
        
        pdf.set_font("Arial", "", 8)
        for e in ativos:
            pdf.cell(60, 7, e.usuario.nome[:25], 1)
            pdf.cell(60, 7, e.livro.titulo[:25], 1)
            pdf.cell(40, 7, e.data_emprestimo.strftime("%d/%m/%Y"), 1)
            pdf.ln()
    
    # Salvar PDF
    pdf.output(nome_arquivo)
    t = f"✅ [red]PDF[/] gerado: {nome_arquivo}"
    p = Panel(t, width=40, style='bold green on black')
    print(p)
 
#========================================================================================
def exportar_excel(biblioteca, nome_arquivo="relatorio_biblioteca.xlsx"):
    """Exporta os dados da biblioteca para Excel (sempre dados atuais desconsiderando a nova data de geração de multa caso o usuário pague , mas não devolva ainda)"""

    #  BARRA DE PROGRESSO (ANTES DE COMEÇAR)
    print('\n[green]Preparando arquivo Excel...[/]\n')
    for i in track(range(40), description="[cyan]📊 Gerando Excel..."):
        time.sleep(0.02)
        if i == 15:
            print("[yellow]   ⏳ Coletando dados...[/]")
        if i == 30:
            print("[yellow]   ⏳ Formatando planilhas...[/]")
    

    # Coletar dados atualizados dos empréstimos ativos
    emprestimos_ativos = []
    for emp in biblioteca._Biblioteca__emprestimos:
        if emp.data_devolucao is None:
            emprestimos_ativos.append({
                "Usuário": emp.usuario.nome,
                "ID Usuário": emp.usuario.id,
                "Livro": emp.livro.titulo,
                "ID Livro": emp.livro.id,
                "Autor": emp.livro.autor,
                "Data Empréstimo": emp.data_emprestimo.strftime("%d/%m/%Y"),
                "Status": "Ativo"
            })
    
    # Coletar dados de usuários (atuais)
    usuarios = []
    for u in biblioteca._Biblioteca__usuarios:
        usuarios.append({
            "ID": u.id,
            "Nome": u.nome,
            "Telefone": u.telefone,
            "Multas": u.multas
        })
    
    # Coletar dados de livros (atuais)
    livros = []
    for l in biblioteca._Biblioteca__livros:
        livros.append({
            "ID": l.id,
            "Título": l.titulo,
            "Autor": l.autor,
            "Ano": l.ano,
            "Disponíveis": l.disponiveis,
            "Total": l.quantidade
        })
    
    # Coletar histórico de devoluções
    historico = []
    for emp in biblioteca._Biblioteca__emprestimos:
        if emp.data_devolucao is not None:
            historico.append({
                "Usuário": emp.usuario.nome,
                "Livro": emp.livro.titulo,
                "Data Empréstimo": emp.data_emprestimo.strftime("%d/%m/%Y"),
                "Data Devolução": emp.data_devolucao.strftime("%d/%m/%Y"),
            })
    
    # Criar DataFrames 
    df_emprestimos = pd.DataFrame(emprestimos_ativos)
    df_usuarios = pd.DataFrame(usuarios)
    df_livros = pd.DataFrame(livros)
    df_historico = pd.DataFrame(historico)
    
    # FORÇA A SOBRESCRITA DO ARQUIVO
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)  # Deleta o antigo
    
    # Exportar para Excel com todas as abas
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        df_emprestimos.to_excel(writer, sheet_name="Empréstimos Ativos", index=False)
        df_usuarios.to_excel(writer, sheet_name="Usuários", index=False)
        df_livros.to_excel(writer, sheet_name="Livros", index=False)
        if not df_historico.empty:
            df_historico.to_excel(writer, sheet_name="Histórico", index=False)
    
    t = f"✅ [red]EXCEL[/] gerado: {nome_arquivo}"
    p = Panel(t, width=40, style='bold green on black')
    print(p)

#========================================================================================