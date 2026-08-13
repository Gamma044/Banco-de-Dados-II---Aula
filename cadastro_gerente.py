# cadastro_gerente.py
# Funções para cadastrar, listar, buscar, atualizar e excluir gerentes no banco MySQL

from conexao import conectar  # importa a função conectar do arquivo conexao.py


def cadastrar_gerente(nome):
    # Recebe o nome e insere um novo gerente no banco
    try:  # tenta executar o cadastro
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando INSERT
            "INSERT INTO gerente (nome) VALUES (%s)",  # SQL de inserção
            (nome,)  # valor que substitui o %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(f"Gerente '{nome}' cadastrado com sucesso!")  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao cadastrar gerente: {e}")  # mostra o erro
        return False  # retorna False indicando falha


def listar_gerentes():
    # Busca e retorna todos os gerentes cadastrados, ordenados por nome
    conn = conectar()  # abre a conexão com o MySQL

    if conn is None:  # se a conexão falhou
        return []  # retorna lista vazia

    cursor = conn.cursor()  # cria um cursor para executar SQL

    cursor.execute("SELECT id_gerente, nome FROM gerente ORDER BY nome")  # busca todos

    resultado = cursor.fetchall()  # pega todos os registros encontrados

    cursor.close()  # fecha o cursor
    conn.close()  # fecha a conexão

    return resultado  # retorna a lista de gerentes


def buscar_gerente_por_id(id_gerente):
    # Busca um gerente específico pelo ID
    conn = conectar()  # abre a conexão com o MySQL

    if conn is None:  # se a conexão falhou
        return None  # retorna None

    cursor = conn.cursor()  # cria um cursor

    cursor.execute(  # executa a busca por ID
        "SELECT id_gerente, nome FROM gerente WHERE id_gerente = %s",
        (id_gerente,)  # valor que substitui o %s
    )

    resultado = cursor.fetchone()  # pega apenas um registro (ou None)

    cursor.close()  # fecha o cursor
    conn.close()  # fecha a conexão

    return resultado  # retorna o gerente encontrado ou None


def atualizar_gerente(id_gerente, nome):
    # Recebe o id do gerente e o novo nome, e atualiza o registro no banco
    try:  # tenta executar a atualização
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando UPDATE
            "UPDATE gerente SET nome = %s WHERE id_gerente = %s",  # SQL de atualização
            (nome, id_gerente)  # valores que substituem os %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(f"Gerente {id_gerente} atualizado com sucesso!")  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao atualizar gerente: {e}")  # mostra o erro
        return False  # retorna False indicando falha


def excluir_gerente(id_gerente):
    # Recebe o id do gerente e remove o registro do banco
    try:  # tenta executar a exclusão
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando DELETE
            "DELETE FROM gerente WHERE id_gerente = %s",  # SQL de exclusão
            (id_gerente,)  # valor que substitui o %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(f"Gerente {id_gerente} excluído com sucesso!")  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao excluir gerente: {e}")  # mostra o erro
        return False  # retorna False indicando falha