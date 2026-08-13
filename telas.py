# telas.py
# Interface gráfica da Cantina Escola Alegria usando Tkinter e funções

import tkinter as tk               # importa a biblioteca de interface gráfica
from tkinter import ttk, messagebox  # importa Treeview, Combobox e caixas de mensagem
from cadastro_aluno import cadastrar_aluno, listar_alunos, atualizar_aluno, excluir_aluno  # funções de aluno
from cadastro_atendente import (
    cadastrar_atendente,
    listar_atendentes,
    atualizar_atendente,
    excluir_atendente
)  # funções de atendente
from cadastro_gerente import (
    cadastrar_gerente,
    listar_gerentes,
    atualizar_gerente,
    excluir_gerente
)  # funções de gerente
from cadastro_produto import (     # funções de produto
    cadastrar_produto_perecivel,   # cadastrar perecível
    cadastrar_produto_nao_perecivel,  # cadastrar não perecível
    listar_produtos,               # listar produtos
    buscar_produto_por_id,         # buscar produto por ID
)
from pedido import (               # funções de pedido
    registrar_pedido,              # criar pedido
    adicionar_item,                # adicionar item ao pedido
    cancelar_pedido,               # cancelar pedido
    calcular_total_pedido,         # calcular total
    listar_pedidos_ativos,         # listar pedidos ativos
)
from relatorio import gerar_relatorio_diario  # função de relatório


def limpar_frame(frame):
    # Remove todos os widgets (botões, labels, etc.) de um frame
    for widget in frame.winfo_children():         # percorre cada widget dentro do frame
        widget.destroy()                         # destrói (remove) o widget


def tela_cadastrar_aluno(frame_conteudo):
    # Monta a tela de cadastro de aluno dentro do frame_conteudo
    limpar_frame(frame_conteudo)                  # limpa o conteúdo anterior da tela

    tk.Label(frame_conteudo, text="Cadastrar Aluno", font=("Arial", 14, "bold")).pack(pady=10)  # título

    tk.Label(frame_conteudo, text="Nome:").pack()  # rótulo do campo nome
    entry_nome = tk.Entry(frame_conteudo, width=40)  # campo de texto para o nome
    entry_nome.pack(pady=3)                       # posiciona o campo na tela

    tk.Label(frame_conteudo, text="Matrícula:").pack()  # rótulo do campo matrícula
    entry_mat = tk.Entry(frame_conteudo, width=40)  # campo de texto para a matrícula
    entry_mat.pack(pady=3)                        # posiciona o campo na tela

    id_selecionado = {"id": None}                 # guarda o id do aluno selecionado na lista (None = novo cadastro)

    def limpar_campos():                          # limpa os campos e desmarca a seleção
        entry_nome.delete(0, tk.END)             # limpa o campo nome
        entry_mat.delete(0, tk.END)              # limpa o campo matrícula
        id_selecionado["id"] = None              # reseta a seleção
        for item in tree.selection():            # percorre itens selecionados na tabela
            tree.selection_remove(item)          # remove a seleção visual

    def salvar():                                 # função interna chamada pelo botão Salvar
        nome = entry_nome.get().strip()           # pega o texto do campo nome
        mat = entry_mat.get().strip()             # pega o texto do campo matrícula
        if not nome or not mat:                   # se algum campo estiver vazio
            messagebox.showwarning("Atenção", "Preencha todos os campos.")  # avisa
            return                               # interrompe a função
        if cadastrar_aluno(nome, mat):            # tenta cadastrar no banco
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")  # sucesso
            tela_cadastrar_aluno(frame_conteudo) # recarrega a tela para atualizar lista

    def atualizar():                              # função interna chamada pelo botão Atualizar
        if id_selecionado["id"] is None:          # precisa ter um aluno selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um aluno na lista para atualizar.")
            return
        nome = entry_nome.get().strip()           # pega o texto do campo nome
        mat = entry_mat.get().strip()             # pega o texto do campo matrícula
        if not nome or not mat:                   # se algum campo estiver vazio
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if atualizar_aluno(id_selecionado["id"], nome, mat):  # tenta atualizar no banco
            messagebox.showinfo("Sucesso", f"Aluno {nome} atualizado!")  # sucesso
            tela_cadastrar_aluno(frame_conteudo) # recarrega a tela para atualizar lista

    def excluir():                                # função interna chamada pelo botão Excluir
        if id_selecionado["id"] is None:          # precisa ter um aluno selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um aluno na lista para excluir.")
            return
        nome = entry_nome.get().strip() or "selecionado"  # nome para exibir na confirmação
        if messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir o aluno '{nome}'?"):
            if excluir_aluno(id_selecionado["id"]):  # tenta excluir no banco
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                tela_cadastrar_aluno(frame_conteudo)  # recarrega a tela para atualizar lista

    frame_botoes = tk.Frame(frame_conteudo)       # frame para agrupar os botões lado a lado
    frame_botoes.pack(pady=10)
    tk.Button(frame_botoes, text="Salvar", command=salvar,
              bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=3)  # botão salvar (novo)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar,
              bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=3)  # botão atualizar
    tk.Button(frame_botoes, text="Excluir", command=excluir,
              bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=3)  # botão excluir
    tk.Button(frame_botoes, text="Limpar", command=limpar_campos,
              bg="#9E9E9E", fg="white", width=12).pack(side=tk.LEFT, padx=3)  # botão limpar campos

    tk.Label(frame_conteudo, text="Alunos cadastrados:", font=("Arial", 11, "bold")).pack(pady=(15, 5))  # subtítulo
    tk.Label(frame_conteudo, text="(clique em um aluno na lista para editar ou excluir)",
             font=("Arial", 9), fg="#666").pack()  # dica de uso
    tree = ttk.Treeview(frame_conteudo, columns=("id", "nome", "mat"), show="headings", height=8)  # tabela
    tree.heading("id", text="ID")                 # cabeçalho da coluna ID
    tree.heading("nome", text="Nome")             # cabeçalho da coluna Nome
    tree.heading("mat", text="Matrícula")         # cabeçalho da coluna Matrícula
    tree.column("id", width=50)                   # largura da coluna ID
    tree.column("nome", width=200)                # largura da coluna Nome
    tree.column("mat", width=120)                 # largura da coluna Matrícula
    for a in listar_alunos():                     # percorre cada aluno do banco
        tree.insert("", tk.END, values=a)         # insere a linha na tabela
    tree.pack(pady=5)                             # posiciona a tabela na tela

    def ao_selecionar_linha(event):               # chamado quando o usuário clica em uma linha da tabela
        selecionado = tree.selection()            # pega a(s) linha(s) selecionada(s)
        if not selecionado:                       # se nada estiver selecionado
            return
        valores = tree.item(selecionado[0], "values")  # pega os valores (id, nome, mat) da linha
        id_selecionado["id"] = int(valores[0])    # guarda o id do aluno selecionado
        entry_nome.delete(0, tk.END)             # limpa o campo nome
        entry_nome.insert(0, valores[1])          # preenche com o nome do aluno selecionado
        entry_mat.delete(0, tk.END)              # limpa o campo matrícula
        entry_mat.insert(0, valores[2])           # preenche com a matrícula do aluno selecionado

    tree.bind("<<TreeviewSelect>>", ao_selecionar_linha)  # associa o clique na tabela à função acima


def tela_cadastrar_atendente(frame_conteudo):
    # Monta a tela de cadastro de atendente
    limpar_frame(frame_conteudo)                  # limpa o conteúdo anterior

    tk.Label(frame_conteudo, text="Cadastrar Atendente", font=("Arial", 14, "bold")).pack(pady=10)  # título

    tk.Label(frame_conteudo, text="Nome:").pack()  # rótulo
    entry_nome = tk.Entry(frame_conteudo, width=40)  # campo de texto
    entry_nome.pack(pady=3)                       # posiciona o campo

    id_selecionado = {"id": None}                 # guarda o id do atendente selecionado na lista

    def limpar_campos():                          # limpa os campos e desmarca a seleção
        entry_nome.delete(0, tk.END)
        id_selecionado["id"] = None
        for item in tree.selection():
            tree.selection_remove(item)

    def salvar():                                 # função do botão salvar
        nome = entry_nome.get().strip()           # pega o nome digitado
        if not nome:                              # se estiver vazio
            messagebox.showwarning("Atenção", "Informe o nome.")  # avisa
            return                               # interrompe
        if cadastrar_atendente(nome):             # tenta cadastrar
            messagebox.showinfo("Sucesso", f"Atendente {nome} cadastrado!")  # sucesso
            tela_cadastrar_atendente(frame_conteudo)  # recarrega a tela

    def atualizar():                              # função do botão atualizar
        if id_selecionado["id"] is None:          # precisa ter um atendente selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um atendente na lista para atualizar.")
            return
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome.")
            return
        if atualizar_atendente(id_selecionado["id"], nome):  # tenta atualizar no banco
            messagebox.showinfo("Sucesso", f"Atendente {nome} atualizado!")
            tela_cadastrar_atendente(frame_conteudo)  # recarrega a tela

    def excluir():                                # função do botão excluir
        if id_selecionado["id"] is None:          # precisa ter um atendente selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um atendente na lista para excluir.")
            return
        nome = entry_nome.get().strip() or "selecionado"
        if messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir o atendente '{nome}'?"):
            if excluir_atendente(id_selecionado["id"]):  # tenta excluir no banco
                messagebox.showinfo("Sucesso", "Atendente excluído com sucesso!")
                tela_cadastrar_atendente(frame_conteudo)  # recarrega a tela

    frame_botoes = tk.Frame(frame_conteudo)       # frame para agrupar os botões
    frame_botoes.pack(pady=10)
    tk.Button(frame_botoes, text="Salvar", command=salvar,
              bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar,
              bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Excluir", command=excluir,
              bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Limpar", command=limpar_campos,
              bg="#9E9E9E", fg="white", width=12).pack(side=tk.LEFT, padx=3)

    tk.Label(frame_conteudo, text="Atendentes cadastrados:", font=("Arial", 11, "bold")).pack(pady=(15, 5))
    tk.Label(frame_conteudo, text="(clique em um atendente na lista para editar ou excluir)",
             font=("Arial", 9), fg="#666").pack()
    tree = ttk.Treeview(frame_conteudo, columns=("id", "nome"), show="headings", height=8)  # tabela
    tree.heading("id", text="ID")                 # cabeçalho ID
    tree.heading("nome", text="Nome")             # cabeçalho Nome
    tree.column("id", width=50)                   # largura ID
    tree.column("nome", width=250)                # largura Nome
    for a in listar_atendentes():                 # percorre os atendentes
        tree.insert("", tk.END, values=a)         # insere na tabela
    tree.pack(pady=5)                             # posiciona a tabela

    def ao_selecionar_linha(event):               # chamado ao clicar em uma linha
        selecionado = tree.selection()
        if not selecionado:
            return
        valores = tree.item(selecionado[0], "values")
        id_selecionado["id"] = int(valores[0])
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])

    tree.bind("<<TreeviewSelect>>", ao_selecionar_linha)


def tela_cadastrar_gerente(frame_conteudo):
    # Monta a tela de cadastro de gerente
    limpar_frame(frame_conteudo)                  # limpa o conteúdo anterior

    tk.Label(frame_conteudo, text="Cadastrar Gerente", font=("Arial", 14, "bold")).pack(pady=10)  # título

    tk.Label(frame_conteudo, text="Nome:").pack()  # rótulo
    entry_nome = tk.Entry(frame_conteudo, width=40)  # campo de texto
    entry_nome.pack(pady=3)                       # posiciona

    id_selecionado = {"id": None}                 # guarda o id do gerente selecionado na lista

    def limpar_campos():                          # limpa os campos e desmarca a seleção
        entry_nome.delete(0, tk.END)
        id_selecionado["id"] = None
        for item in tree.selection():
            tree.selection_remove(item)

    def salvar():                                 # função do botão salvar
        nome = entry_nome.get().strip()           # pega o nome
        if not nome:                              # se vazio
            messagebox.showwarning("Atenção", "Informe o nome.")
            return
        if cadastrar_gerente(nome):               # tenta cadastrar
            messagebox.showinfo("Sucesso", f"Gerente {nome} cadastrado!")
            tela_cadastrar_gerente(frame_conteudo)  # recarrega

    def atualizar():                              # função do botão atualizar
        if id_selecionado["id"] is None:          # precisa ter um gerente selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um gerente na lista para atualizar.")
            return
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome.")
            return
        if atualizar_gerente(id_selecionado["id"], nome):  # tenta atualizar no banco
            messagebox.showinfo("Sucesso", f"Gerente {nome} atualizado!")
            tela_cadastrar_gerente(frame_conteudo)  # recarrega

    def excluir():                                # função do botão excluir
        if id_selecionado["id"] is None:          # precisa ter um gerente selecionado na lista
            messagebox.showwarning("Atenção", "Selecione um gerente na lista para excluir.")
            return
        nome = entry_nome.get().strip() or "selecionado"
        if messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir o gerente '{nome}'?"):
            if excluir_gerente(id_selecionado["id"]):  # tenta excluir no banco
                messagebox.showinfo("Sucesso", "Gerente excluído com sucesso!")
                tela_cadastrar_gerente(frame_conteudo)  # recarrega

    frame_botoes = tk.Frame(frame_conteudo)       # frame para agrupar os botões
    frame_botoes.pack(pady=10)
    tk.Button(frame_botoes, text="Salvar", command=salvar,
              bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar,
              bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Excluir", command=excluir,
              bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=3)
    tk.Button(frame_botoes, text="Limpar", command=limpar_campos,
              bg="#9E9E9E", fg="white", width=12).pack(side=tk.LEFT, padx=3)

    tk.Label(frame_conteudo, text="Gerentes cadastrados:", font=("Arial", 11, "bold")).pack(pady=(15, 5))
    tk.Label(frame_conteudo, text="(clique em um gerente na lista para editar ou excluir)",
             font=("Arial", 9), fg="#666").pack()
    tree = ttk.Treeview(frame_conteudo, columns=("id", "nome"), show="headings", height=6)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.column("id", width=50)
    tree.column("nome", width=250)
    for g in listar_gerentes():                   # percorre os gerentes
        tree.insert("", tk.END, values=g)         # insere na tabela
    tree.pack(pady=5)

    def ao_selecionar_linha(event):               # chamado ao clicar em uma linha
        selecionado = tree.selection()
        if not selecionado:
            return
        valores = tree.item(selecionado[0], "values")
        id_selecionado["id"] = int(valores[0])
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])

    tree.bind("<<TreeviewSelect>>", ao_selecionar_linha)


def tela_cadastrar_produto(frame_conteudo):
    # Monta a tela de cadastro de produto
    limpar_frame(frame_conteudo)                  # limpa a tela

    tk.Label(frame_conteudo, text="Cadastrar Produto", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(frame_conteudo, text="Nome do produto:").pack()
    entry_nome = tk.Entry(frame_conteudo, width=40)  # campo nome
    entry_nome.pack(pady=2)

    tk.Label(frame_conteudo, text="Preço (ex: 5.50):").pack()
    entry_preco = tk.Entry(frame_conteudo, width=40)  # campo preço
    entry_preco.pack(pady=2)

    tk.Label(frame_conteudo, text="Código de barras:").pack()
    entry_cod = tk.Entry(frame_conteudo, width=40)  # campo código
    entry_cod.pack(pady=2)

    tipo_var = tk.StringVar(value="perecivel")    # variável do tipo de produto
    tk.Radiobutton(frame_conteudo, text="Perecível", variable=tipo_var, value="perecivel").pack()  # opção 1
    tk.Radiobutton(frame_conteudo, text="Não Perecível", variable=tipo_var, value="nao_perecivel").pack()  # opção 2

    tk.Label(frame_conteudo, text="Data de validade (AAAA-MM-DD) — só para perecíveis:").pack()
    entry_val = tk.Entry(frame_conteudo, width=40)  # campo validade
    entry_val.pack(pady=2)

    def salvar():                                 # função do botão salvar
        nome = entry_nome.get().strip()           # pega o nome
        try:
            preco = float(entry_preco.get().replace(",", "."))  # converte preço para número
        except ValueError:
            messagebox.showwarning("Atenção", "Preço inválido.")
            return
        cod = entry_cod.get().strip()             # pega o código de barras
        if not nome:                              # se nome vazio
            messagebox.showwarning("Atenção", "Informe o nome.")
            return

        if tipo_var.get() == "perecivel":         # se for perecível
            val = entry_val.get().strip()         # pega a data de validade
            if not val:                           # se validade vazia
                messagebox.showwarning("Atenção", "Informe a data de validade.")
                return
            idp = cadastrar_produto_perecivel(nome, preco, cod, val)  # função
        else:                                     # se for não perecível
            idp = cadastrar_produto_nao_perecivel(nome, preco, cod)  # função

        if idp:                                   # se cadastrou com sucesso
            messagebox.showinfo("Sucesso", f"Produto cadastrado com ID {idp}")
            tela_cadastrar_produto(frame_conteudo)  # recarrega a tela

    tk.Button(frame_conteudo, text="Salvar Produto", command=salvar, bg="#4CAF50", fg="white", width=18).pack(pady=10)

    tk.Label(frame_conteudo, text="Produtos cadastrados:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
    tree = ttk.Treeview(frame_conteudo, columns=("id", "nome", "preco", "tipo", "val"), show="headings", height=7)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("preco", text="Preço")
    tree.heading("tipo", text="Tipo")
    tree.heading("val", text="Validade")
    tree.column("id", width=40)
    tree.column("nome", width=150)
    tree.column("preco", width=70)
    tree.column("tipo", width=100)
    tree.column("val", width=100)
    for prod in listar_produtos():                # percorre os produtos
        tree.insert("", tk.END, values=(prod[0], prod[1], f"R$ {float(prod[2]):.2f}", prod[4], prod[5] or "—"))
    tree.pack(pady=5)


def tela_registrar_pedido(frame_conteudo):
    # Monta a tela para registrar um novo pedido com itens
    limpar_frame(frame_conteudo)                  # limpa a tela

    tk.Label(frame_conteudo, text="Registrar Pedido", font=("Arial", 14, "bold")).pack(pady=8)

    tk.Label(frame_conteudo, text="Aluno:").pack()
    alunos = listar_alunos()                      # busca alunos no banco
    aluno_var = tk.StringVar()                    # variável do combobox de aluno
    opcoes_aluno = [f"{a[0]} - {a[1]}" for a in alunos]  # monta lista "ID - Nome"
    cb_aluno = ttk.Combobox(frame_conteudo, textvariable=aluno_var, values=opcoes_aluno, width=40, state="readonly")
    cb_aluno.pack(pady=2)                         # posiciona o combobox

    tk.Label(frame_conteudo, text="Atendente:").pack()
    atendentes = listar_atendentes()              # busca atendentes
    atend_var = tk.StringVar()                    # variável do combobox de atendente
    opcoes_atend = [f"{a[0]} - {a[1]}" for a in atendentes]  # monta lista "ID - Nome"
    cb_atend = ttk.Combobox(frame_conteudo, textvariable=atend_var, values=opcoes_atend, width=40, state="readonly")
    cb_atend.pack(pady=2)

    tk.Label(frame_conteudo, text="Forma de pagamento:").pack()
    pag_var = tk.StringVar(value="dinheiro")      # variável da forma de pagamento
    frame_pag = tk.Frame(frame_conteudo)          # frame para os radio buttons
    frame_pag.pack()
    for op in ["dinheiro", "cartao", "saldo"]:    # cria um radio para cada opção
        tk.Radiobutton(frame_pag, text=op.capitalize(), variable=pag_var, value=op).pack(side=tk.LEFT, padx=5)

    tk.Label(frame_conteudo, text="Produto:").pack()
    produtos = listar_produtos()                  # busca produtos
    prod_var = tk.StringVar()                     # variável do combobox de produto
    opcoes_prod = [f"{p[0]} - {p[1]} (R$ {float(p[2]):.2f})" for p in produtos]  # "ID - Nome (preço)"
    cb_prod = ttk.Combobox(frame_conteudo, textvariable=prod_var, values=opcoes_prod, width=40, state="readonly")
    cb_prod.pack(pady=2)

    tk.Label(frame_conteudo, text="Quantidade:").pack()
    entry_qtd = tk.Entry(frame_conteudo, width=10)  # campo quantidade
    entry_qtd.insert(0, "1")                      # valor inicial 1
    entry_qtd.pack(pady=2)

    itens_temp = []                               # lista temporária de itens do pedido

    frame_lista = tk.Frame(frame_conteudo)        # frame para a tabela de itens
    frame_lista.pack(pady=5)
    tree_itens = ttk.Treeview(frame_lista, columns=("prod", "qtd", "preco", "sub"), show="headings", height=5)
    tree_itens.heading("prod", text="Produto")
    tree_itens.heading("qtd", text="Qtd")
    tree_itens.heading("preco", text="Preço Unit.")
    tree_itens.heading("sub", text="Subtotal")
    tree_itens.column("prod", width=180)
    tree_itens.column("qtd", width=50)
    tree_itens.column("preco", width=80)
    tree_itens.column("sub", width=80)
    tree_itens.pack()

    lbl_total = tk.Label(frame_conteudo, text="Total: R$ 0.00", font=("Arial", 12, "bold"))
    lbl_total.pack(pady=5)                        # label que mostra o total

    def adicionar_item_temp():                    # adiciona item na lista temporária
        if not prod_var.get():                    # se nenhum produto selecionado
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        try:
            qtd = int(entry_qtd.get())            # converte quantidade para inteiro
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade inválida.")
            return

        id_prod = int(prod_var.get().split(" -")[0])  # extrai o ID do produto
        prod_dados = buscar_produto_por_id(id_prod)  # busca dados
        if not prod_dados:
            return
        nome = prod_dados[1]                     # nome do produto
        preco = float(prod_dados[2])              # preço unitário
        sub = qtd * preco                         # calcula subtotal
        itens_temp.append({"id_produto": id_prod, "nome": nome, "qtd": qtd, "preco": preco})  # adiciona na lista
        tree_itens.insert("", tk.END, values=(nome, qtd, f"R$ {preco:.2f}", f"R$ {sub:.2f}"))  # mostra na tabela
        total = sum(i["qtd"] * i["preco"] for i in itens_temp)  # recalcula total
        lbl_total.config(text=f"Total: R$ {total:.2f}")  # atualiza o label

    def finalizar_pedido():                       # grava o pedido e os itens no banco
        if not aluno_var.get() or not atend_var.get():  # valida seleções
            messagebox.showwarning("Atenção", "Selecione aluno e atendente.")
            return
        if not itens_temp:                        # precisa ter pelo menos 1 item
            messagebox.showwarning("Atenção", "Adicione pelo menos um item.")
            return

        id_aluno = int(aluno_var.get().split(" -")[0])  # extrai ID do aluno
        id_atend = int(atend_var.get().split(" -")[0])  # extrai ID do atendente
        id_ped = registrar_pedido(id_aluno, id_atend, pag_var.get())  # cria o pedido
        if id_ped:                                # se criou com sucesso
            for item in itens_temp:               # percorre cada item temporário
                adicionar_item(id_ped, item["id_produto"], item["qtd"], item["preco"])  # grava no banco
            total = calcular_total_pedido(id_ped)  # calcula o total final
            messagebox.showinfo("Sucesso", f"Pedido {id_ped} registrado!\nTotal: R$ {total:.2f}")
            tela_registrar_pedido(frame_conteudo)  # limpa e reinicia a tela

    frame_btn = tk.Frame(frame_conteudo)          # frame dos botões
    frame_btn.pack(pady=8)
    tk.Button(frame_btn, text="+ Adicionar Item", command=adicionar_item_temp, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Finalizar Pedido", command=finalizar_pedido, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)


def tela_cancelar_pedido(frame_conteudo):
    # Monta a tela para cancelar um pedido ativo
    limpar_frame(frame_conteudo)                  # limpa a tela

    tk.Label(frame_conteudo, text="Cancelar Pedido", font=("Arial", 14, "bold")).pack(pady=10)

    pedidos = listar_pedidos_ativos()             # busca pedidos ativos
    if not pedidos:                               # se não houver pedidos
        tk.Label(frame_conteudo, text="Nenhum pedido ativo no momento.").pack(pady=20)
        return

    tk.Label(frame_conteudo, text="Selecione o pedido para cancelar:").pack()
    ped_var = tk.StringVar()                      # variável do combobox
    opcoes = [f"{p[0]} | {p[1]} | {p[3]} | {p[4]}" for p in pedidos]  # monta opções
    cb = ttk.Combobox(frame_conteudo, textvariable=ped_var, values=opcoes, width=55, state="readonly")
    cb.pack(pady=5)

    def confirmar():                              # função do botão cancelar
        if not ped_var.get():                     # se nada selecionado
            messagebox.showwarning("Atenção", "Selecione um pedido para cancelar.")
            return
        id_ped = int(ped_var.get().split(" |")[0])  # extrai o ID do pedido
        if messagebox.askyesno("Confirmar", f"Cancelar o pedido {id_ped}?\nOs itens serão removidos."):
            if cancelar_pedido(id_ped):           # cancela no banco
                messagebox.showinfo("OK", f"Pedido {id_ped} cancelado.")
                tela_cancelar_pedido(frame_conteudo)  # recarrega a tela

    tk.Button(frame_conteudo, text="Cancelar Pedido Selecionado", command=confirmar,
              bg="#f44336", fg="white", width=25).pack(pady=15)


def tela_relatorio(frame_conteudo):
    # Monta a tela do relatório diário
    limpar_frame(frame_conteudo)                  # limpa a tela

    tk.Label(frame_conteudo, text="Relatório Diário", font=("Arial", 14, "bold")).pack(pady=10)

    r = gerar_relatorio_diario()                  # gera o relatório do dia

    tk.Label(frame_conteudo, text=f"Data: {r['data']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(frame_conteudo, text=f"Pedidos realizados: {r['quantidade_pedidos']}", font=("Arial", 12)).pack(pady=3)
    tk.Label(frame_conteudo, text=f"Valor total arrecadado: R$ {r['valor_total']:.2f}",
             font=("Arial", 14, "bold"), fg="#1B5E20").pack(pady=8)

    if r["por_forma_pagamento"]:                  # se houver detalhamento
        tk.Label(frame_conteudo, text="Por forma de pagamento:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
        for forma, qtd, total in r["por_forma_pagamento"]:  # percorre cada forma
            tk.Label(frame_conteudo,
                     text=f"  {str(forma).capitalize()}: {qtd} pedido(s) — R$ {float(total):.2f}").pack()

    def atualizar():                              # recarrega o relatório
        tela_relatorio(frame_conteudo)

    tk.Button(frame_conteudo, text="Atualizar Relatório", command=atualizar,
              bg="#2196F3", fg="white", width=18).pack(pady=15)


def iniciar_sistema():
    # Cria a janela principal e o menu de navegação lateral
    janela = tk.Tk()                              # cria a janela principal
    janela.title("Cantina Escola Alegria — Sistema de Atendimento (MySQL)")  # título da janela
    janela.geometry("700x620")                    # tamanho inicial da janela
    janela.resizable(True, True)                  # permite redimensionar

    frame_menu = tk.Frame(janela, bg="#1F4E79", width=180)  # barra lateral azul
    frame_menu.pack(side=tk.LEFT, fill=tk.Y)      # posiciona à esquerda
    frame_menu.pack_propagate(False)              # mantém a largura fixa

    tk.Label(frame_menu, text="CANTINA\\nALEGRIA", bg="#1F4E79", fg="white",
             font=("Arial", 12, "bold"), pady=15).pack()  # logo/texto no topo do menu

    frame_conteudo = tk.Frame(janela, bg="white")  # área de conteúdo à direita
    frame_conteudo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    botoes = [                                    # lista de botões do menu
        ("Cadastrar Aluno", lambda: tela_cadastrar_aluno(frame_conteudo)),
        ("Cadastrar Atendente", lambda: tela_cadastrar_atendente(frame_conteudo)),
        ("Cadastrar Gerente", lambda: tela_cadastrar_gerente(frame_conteudo)),
        ("Cadastrar Produto", lambda: tela_cadastrar_produto(frame_conteudo)),
        ("Registrar Pedido", lambda: tela_registrar_pedido(frame_conteudo)),
        ("Cancelar Pedido", lambda: tela_cancelar_pedido(frame_conteudo)),
        ("Relatório Diário", lambda: tela_relatorio(frame_conteudo)),
    ]

    for texto, comando in botoes:                 # cria cada botão do menu
        tk.Button(frame_menu, text=texto, command=comando,
                  bg="#2E75B6", fg="white", activebackground="#1565C0",
                  font=("Arial", 10), width=18, pady=6, relief=tk.FLAT).pack(pady=3, padx=8)

    tk.Button(frame_menu, text="Sair", command=janela.destroy,
              bg="#C62828", fg="white", font=("Arial", 10), width=18, pady=6, relief=tk.FLAT).pack(side=tk.BOTTOM, pady=15, padx=8)  # botão sair

    tk.Label(frame_conteudo, text="Bem-vindo ao Sistema da Cantina!",
             font=("Arial", 16, "bold"), fg="#1F4E79").pack(pady=40)  # mensagem inicial
    tk.Label(frame_conteudo, text="Use o menu à esquerda para navegar.\\nBanco: MySQL",
             font=("Arial", 11), fg="#666").pack()

    janela.mainloop()                             # inicia o loop da interface gráfica


if __name__ == "__main__":                        # se este arquivo for executado diretamente
    iniciar_sistema()                             # chama a função que inicia o sistema
