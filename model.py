from dao import connection

def consulta_alunos():
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    #cursor.execute("select * from alunos")
    cursor.execute(
        '''
        SELECT 
            *
        FROM
            alunos
        '''
    )

    dados = cursor.fetchall()

    conn.close()

    resposta = {}

    for item in dados:
        resposta[f"{len(resposta)+1}"] = item["nome"]

    return resposta

def add_aluno(nome):
    conn = connection()
    cursor = conn.cursor()

    query = '''
            insert into alunos (nome) values (%s)
            '''
    
    cursor.execute(query , (nome,))

    conn.commit()
    conn.close()