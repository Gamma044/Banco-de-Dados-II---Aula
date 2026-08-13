# pedido.py
# Funções para registrar pedidos, adicionar itens e cancelar pedidos
 
from conexao import conectar       # importa a função conectar do arquivo conexao.py
from datetime import datetime     # importa datetime para pegar data e hora atuais
 
 
def registrar_pedido(id_aluno, id_atendente, forma_pagamento):
    # Cria um novo pedido e retorna o id_pedido gerado automaticamente
    try:                                          # tenta registrar o pedido
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return None                          # retorna None indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
        horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # data/hora atual formatada
 
        cursor.execute(                           # insere o novo pedido
            """INSERT INTO pedido (horario, forma_pagamento, id_aluno, id_atendente, status)
               VALUES (%s, %s, %s, %s, 'ativo')""",
            (horario, forma_pagamento, id_aluno, id_atendente)  # valores dos %s
        )
        id_pedido = cursor.lastrowid             # pega o ID gerado automaticamente
        conn.commit()                            # confirma a inserção
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão
        print(f"Pedido {id_pedido} registrado com sucesso!")  # mensagem de sucesso
        return id_pedido                         # retorna o ID do pedido criado
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao registrar pedido: {e}")  # mostra o erro
        return None                              # retorna None indicando falha
 
 
def adicionar_item(id_pedido, id_produto, quantidade, preco_unitario):
    # Adiciona um item (produto + quantidade) a um pedido já existente
    try:                                          # tenta adicionar o item
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return False                         # retorna False indicando erro
        cursor = conn.cursor()                    # cria um cursor
        cursor.execute(                           # insere o item no pedido
            """INSERT INTO item_pedido (quantidade, preco_unitario, id_pedido, id_produto)
               VALUES (%s, %s, %s, %s)""",
            (quantidade, preco_unitario, id_pedido, id_produto)  # valores dos %s
        )
        conn.commit()                            # confirma a inserção
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão
        print(f"Item adicionado ao pedido {id_pedido}.")  # mensagem de sucesso
        return True                              # retorna True indicando sucesso
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao adicionar item: {e}")    # mostra o erro
        return False                             # retorna False indicando falha
 
 
def cancelar_pedido(id_pedido):
    # Cancela o pedido e apaga seus itens (composição: itens não existem sem o pedido)
    try:                                          # tenta cancelar o pedido
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return False                         # retorna False indicando erro
        cursor = conn.cursor()                    # cria um cursor
 
        cursor.execute(                           # marca o pedido como cancelado
            "UPDATE pedido SET status = 'cancelado' WHERE id_pedido = %s",
            (id_pedido,)                           # valor que substitui o %s
        )
 
        cursor.execute(                           # apaga todos os itens desse pedido
            "DELETE FROM item_pedido WHERE id_pedido = %s",
            (id_pedido,)                           # valor que substitui o %s
        )
 
        conn.commit()                            # confirma as alterações
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão
        print(f"Pedido {id_pedido} cancelado e seus itens removidos.")  # sucesso
        return True                              # retorna True indicando sucesso
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao cancelar pedido: {e}")   # mostra o erro
        return False                             # retorna False indicando falha
 
 
def listar_itens_do_pedido(id_pedido):
    # Retorna os itens de um pedido, incluindo o nome do produto e o subtotal
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return []                                # retorna lista vazia
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute("""
        SELECT i.id_item, p.nome, i.quantidade, i.preco_unitario,
               (i.quantidade * i.preco_unitario) AS subtotal
        FROM item_pedido i
        JOIN produto p ON i.id_produto = p.id_produto
        WHERE i.id_pedido = %s
    """, (id_pedido,))                          # busca itens ligados ao pedido
    resultado = cursor.fetchall()                 # pega todos os registros
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna a lista de itens
 
 
def calcular_total_pedido(id_pedido):
    # Soma quantidade * preco_unitario de todos os itens do pedido
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return 0                                 # retorna zero
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute("""
        SELECT COALESCE(SUM(i.quantidade * p.preco_unitario), 0)
        FROM item_pedido i
        JOIN produto p ON i.id_produto = p.id_produto
        WHERE id_pedido = %s
    """, (id_pedido,))                          # calcula a soma dos subtotais
    total = cursor.fetchone()[0]                  # pega o valor da soma
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return float(total)                          # retorna o total como número decimal
 
 
def listar_pedidos_ativos():
    # Lista todos os pedidos que ainda estão com status 'ativo'
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return []                                # retorna lista vazia
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute("""
        SELECT pe.id_pedido, pe.horario, pe.forma_pagamento,
               a.nome AS aluno, at.nome AS atendente, pe.status
        FROM pedido pe
        JOIN aluno a ON pe.id_aluno = a.id_aluno
        JOIN atendente at ON pe.id_atendente = at.id_atendente
        WHERE pe.status = 'ativo'
        ORDER BY pe.horario DESC
    """)                                      # junta pedido com aluno e atendente
    resultado = cursor.fetchall()                 # pega todos os registros
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna a lista de pedidos ativos
