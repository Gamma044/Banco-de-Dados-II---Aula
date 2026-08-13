# cadastro_aluno.py
# Funções para cadastrar, listar e buscar alunos no banco MySQL
 
from conexao import conectar       # importa a função conectar do arquivo conexao.py
 
 
def cadastrar_aluno(nome, matricula):
    # Recebe nome e matrícula e insere um novo aluno no banco
    try:                                          # tenta executar o cadastro
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return False                         # retorna False indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
        cursor.execute(                           # executa o comando INSERT
            "INSERT INTO aluno (nome, matricula) VALUES (%s, %s)",  # SQL de inserção
            (nome, matricula)                   # valores que substituem os %s
        )
        conn.commit()                            # confirma (salva) a alteração no banco
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão com o banco
        print(f"Aluno '{nome}' cadastrado com sucesso!")  # mensagem de sucesso
        return True                              # retorna True indicando sucesso
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao cadastrar aluno: {e}")   # mostra o erro
        return False                             # retorna False indicando falha
 
 
def listar_alunos():
    # Busca e retorna todos os alunos cadastrados, ordenados por nome
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return []                                # retorna lista vazia
    cursor = conn.cursor()                        # cria um cursor para executar SQL
    cursor.execute("SELECT id_aluno, nome, matricula FROM aluno ORDER BY nome")  # busca todos
    resultado = cursor.fetchall()                 # pega todos os registros encontrados
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna a lista de alunos
 
 
def buscar_aluno_por_id(id_aluno):
    # Busca um aluno específico pelo id_aluno e retorna seus dados
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return None                              # retorna None
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute(                               # executa a busca por ID
        "SELECT id_aluno, nome, matricula FROM aluno WHERE id_aluno = %s",
        (id_aluno,)                              # valor que substitui o %s
    )
    resultado = cursor.fetchone()                 # pega apenas um registro (ou None)
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna o aluno encontrado ou None
 
 
def buscar_aluno_por_matricula(matricula):
    # Busca um aluno específico pela matrícula e retorna seus dados
    conn = conectar()                             # abre a conexão com o MySQL
    if conn is None:                              # se a conexão falhou
        return None                              # retorna None
    cursor = conn.cursor()                        # cria um cursor
    cursor.execute(                               # executa a busca por matrícula
        "SELECT id_aluno, nome, matricula FROM aluno WHERE matricula = %s",
        (matricula,)                            # valor que substitui o %s
    )
    resultado = cursor.fetchone()                 # pega apenas um registro (ou None)
    cursor.close()                               # fecha o cursor
    conn.close()                                 # fecha a conexão
    return resultado                             # retorna o aluno encontrado ou None
 
 
def atualizar_aluno(id_aluno, nome, matricula):
    # Recebe o id do aluno e os novos dados, e atualiza o registro no banco
    try:                                          # tenta executar a atualização
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return False                         # retorna False indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
        cursor.execute(                           # executa o comando UPDATE
            "UPDATE aluno SET nome = %s, matricula = %s WHERE id_aluno = %s",  # SQL de atualização
            (nome, matricula, id_aluno)         # valores que substituem os %s
        )
        conn.commit()                            # confirma (salva) a alteração no banco
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão com o banco
        print(f"Aluno {id_aluno} atualizado com sucesso!")  # mensagem de sucesso
        return True                              # retorna True indicando sucesso
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao atualizar aluno: {e}")   # mostra o erro
        return False                             # retorna False indicando falha
 
 
def excluir_aluno(id_aluno):
    # Recebe o id do aluno e remove o registro do banco
    try:                                          # tenta executar a exclusão
        conn = conectar()                         # abre a conexão com o MySQL
        if conn is None:                          # se a conexão falhou
            return False                         # retorna False indicando erro
        cursor = conn.cursor()                    # cria um cursor para executar SQL
        cursor.execute(                           # executa o comando DELETE
            "DELETE FROM aluno WHERE id_aluno = %s",  # SQL de exclusão
            (id_aluno,)                          # valor que substitui o %s
        )
        conn.commit()                            # confirma (salva) a alteração no banco
        cursor.close()                           # fecha o cursor
        conn.close()                             # fecha a conexão com o banco
        print(f"Aluno {id_aluno} excluído com sucesso!")  # mensagem de sucesso
        return True                              # retorna True indicando sucesso
    except Exception as e:                       # se ocorrer qualquer erro
        print(f"Erro ao excluir aluno: {e}")     # mostra o erro
        return False                             # retorna False indicando falha
