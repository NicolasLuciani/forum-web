from dao import connection

def consulta_post():
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT * FROM post
        '''
    )
    dados = cursor.fetchall()

    conn.close()
    return dados

def add_post(titulo, informacoes):
    conn = connection()
    cursor = conn.cursor()

    query = '''
            INSERT INTO post (titulo, informacoes) VALUES 
            (%s, %s)
            '''
    cursor.execute(query, (titulo, informacoes))
    conn.commit()
    conn.close()

def editar_post(id, titulo, informacoes):
    conn = connection()
    cursor = conn.cursor()

    query = '''
            UPDATE post SET titulo = %s, informacoes = %s WHERE id = %s
            '''
    cursor.execute(query, (titulo, informacoes, id))
    conn.commit()
    conn.close()

def excluir_post(id):
    conn = connection()
    cursor = conn.cursor()

    query = '''DELETE FROM post WHERE id = %s'''
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def consulta_post_por_id(id):
    conn = connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''SELECT * FROM post WHERE id = %s''', (id,))
    dado = cursor.fetchone()

    conn.close()
    return dado