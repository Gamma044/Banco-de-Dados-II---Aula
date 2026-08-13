# cadastro_produto.py
# Funções para cadastrar e listar produtos perecíveis e não perecíveis
 
from conexao import conectar       # importa a função conectar do arquivo conexao.py
 
 
def cadastrar_produto_perecivel(nome, preco, codigo_barras, data_validade):
    # Cadastra produto perecível: insere em produto e depois em produto_perecivel
    try:                                          # tenta executar o cadastro
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return None                          # retorna None indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
 
        cursor.execute(                           # insere na tabela base produto
            "INSERT INTO produto (nome, preco, codigo_barras) VALUES (%s, %s, %s)",
            (nome, preco, codigo_barras)          # valores que substituem os %s
        )
        id_produto = cursor.lastrowid            # pega o ID gerado automaticamente
 
        cursor.execute(                           # insere na tabela especializada
            "INSERT INTO produto_perecivel (id_produto, data_validade) VALUES (%s, %s)",
            (id_produto, data_validade)          # usa o mesmo ID do produto
        )
 
        conn.commit()                            # confirma as duas inserções
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão
        print(f"Produto perecível '{nome}' cadastrado! (ID {id_produto})")  # sucesso
        return id_produto                        # retorna o ID do produto criado
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao cadastrar produto perecível: {e}")  # mostra o erro
        return None                              # retorna None indicando falha
 
 
def cadastrar_produto_nao_perecivel(nome, preco, codigo_barras):
    # Cadastra produto não perecível: insere em produto e em produto_nao_perecivel
    try:                                          # tenta executar o cadastro
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return None                          # retorna None indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
 
        cursor.execute(                           # insere na tabela base produto
            "INSERT INTO produto (nome, preco, codigo_barras) VALUES (%s, %s, %s)",
            (nome, preco, codigo_barras)          # valores que substituem os %s
        )
        id_produto = cursor.lastrowid            # pega o ID gerado automaticamente
 
        cursor.execute(                           # insere na tabela especializada
            "INSERT INTO produto_nao_perecivel (id_produto) VALUES (%s)",
            (id_produto,)                         # usa o mesmo ID do produto
        )
 
        conn.commit()                            # confirma as duas inserções
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão
        print(f"Produto não perecível '{nome}' cadastrado! (ID {id_produto})")  # sucesso
        return id_produto                        # retorna o ID do produto criado
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao cadastrar produto não perecível: {e}")  # mostra o erro
        return None                              # retorna None indicando falha
 
 
def listar_produtos():
    # Retorna todos os produtos com indicação se é perecível ou não
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return []                                # retorna lista vazia
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute("""
        SELECT p.id_produto, p.nome, p.preco, p.codigo_barras,
               CASE
                   WHEN pp.id_produto IS NOT NULL THEN 'Perecível'
                   WHEN pnp.id_produto IS NOT NULL THEN 'Não Perecível'
                   ELSE 'Desconhecido'
               END AS tipo,
               pp.data_validade
        FROM produto p
        LEFT JOIN produto_perecivel pp ON p.id_produto = pp.id_produto
        LEFT JOIN produto_nao_perecivel pnp ON p.id_produto = pnp.id_produto
        ORDER BY p.nome
    """)                                      # junta produto com suas especializações
    resultado = cursor.fetchall()                 # pega todos os registros
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna a lista de produtos
 
 
def buscar_produto_por_id(id_produto):
    # Busca um produto específico pelo id_produto e retorna seus dados
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return None                              # retorna None
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute(                               # executa a busca por ID
        "SELECT id_produto, nome, preco, codigo_barras FROM produto WHERE id_produto = %s",
        (id_produto,)                            # valor que substitui o %s
    )
    resultado = cursor.fetchone()                 # pega apenas um registro (ou None)
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna o produto encontrado ou None
