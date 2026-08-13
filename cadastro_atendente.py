# cadastro_atendente.py
# Funções para cadastrar, listar, buscar, atualizar e excluir atendentes no banco MySQL

from conexao import conectar  # importa a função conectar do arquivo conexao.py


def cadastrar_atendente(nome):
    # Recebe o nome e insere um novo atendente no banco
    try:  # tenta executar o cadastro
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando INSERT
            "INSERT INTO atendente (nome) VALUES (%s)",  # SQL de inserção
            (nome,),  # valor que substitui o %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(f"Atendente '{nome}' cadastrado com sucesso!")  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao cadastrar atendente: {e}")  # mostra o erro
        return False  # retorna False indicando falha


def listar_atendentes():
    # Busca e retorna todos os atendentes cadastrados, ordenados por nome
    conn = conectar()  # abre a conexão com o MySQL

    if conn is None:  # se a conexão falhou
        return []  # retorna lista vazia

    cursor = conn.cursor()  # cria um cursor para executar SQL

    cursor.execute(
        "SELECT id_atendente, nome FROM atendente ORDER BY nome"
    )  # busca todos

    resultado = cursor.fetchall()  # pega todos os registros encontrados

    cursor.close()  # fecha o cursor
    conn.close()  # fecha a conexão

    return resultado  # retorna a lista de atendentes


def buscar_atendente_por_id(id_atendente):
    # Busca um atendente específico pelo ID
    conn = conectar()  # abre a conexão com o MySQL

    if conn is None:  # se a conexão falhou
        return None  # retorna None

    cursor = conn.cursor()  # cria um cursor

    cursor.execute(  # executa a busca por ID
        "SELECT id_atendente, nome FROM atendente WHERE id_atendente = %s",
        (id_atendente,),  # valor que substitui o %s
    )

    resultado = cursor.fetchone()  # pega apenas um registro (ou None)

    cursor.close()  # fecha o cursor
    conn.close()  # fecha a conexão

    return resultado  # retorna o atendente encontrado ou None


def atualizar_atendente(id_atendente, nome):
    # Recebe o id do atendente e o novo nome, e atualiza o registro no banco
    try:  # tenta executar a atualização
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando UPDATE
            "UPDATE atendente SET nome = %s WHERE id_atendente = %s",  # SQL de atualização
            (nome, id_atendente),  # valores que substituem os %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(
            f"Atendente {id_atendente} atualizado com sucesso!"
        )  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao atualizar atendente: {e}")  # mostra o erro
        return False  # retorna False indicando falha


def excluir_atendente(id_atendente):
    # Recebe o id do atendente e remove o registro do banco
    try:  # tenta executar a exclusão
        conn = conectar()  # abre a conexão com o MySQL

        if conn is None:  # se a conexão falhou
            return False  # retorna False indicando erro

        cursor = conn.cursor()  # cria um cursor para executar SQL

        cursor.execute(  # executa o comando DELETE
            "DELETE FROM atendente WHERE id_atendente = %s",  # SQL de exclusão
            (id_atendente,),  # valor que substitui o %s
        )

        conn.commit()  # confirma (salva) a alteração no banco

        cursor.close()  # fecha o cursor
        conn.close()  # fecha a conexão com o banco

        print(
            f"Atendente {id_atendente} excluído com sucesso!"
        )  # mensagem de sucesso
        return True  # retorna True indicando sucesso

    except Exception as e:  # se ocorrer qualquer erro
        print(f"Erro ao excluir atendente: {e}")  # mostra o erro
        return False  # retorna False indicando falha