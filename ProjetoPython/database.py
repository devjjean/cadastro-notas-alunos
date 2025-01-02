import sqlite3

# Função para criar a tabela 'alunos' caso não exista
def create_table():
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS alunos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     nome TEXT NOT NULL,
                     nota REAL NOT NULL CHECK(nota BETWEEN 0 AND 10)
                     )''')
        conn.commit()

# Função para adicionar um aluno à tabela
def add_aluno(nome, nota):
    if not nome or not (0 <= nota <= 10):
        raise ValueError("Nome não pode ser vazio e a nota deve estar entre 0 e 10.")
    
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
        conn.commit()

# Função para obter a lista de alunos ordenada pela nota (decrescente)
def get_alunos():
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM alunos ORDER BY nota DESC")
        return c.fetchall()

# Função para remover alunos do banco de dados
def remover_aluno_do_db(aluno_id=None):
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        if aluno_id:  # Remove um aluno específico
            c.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
        else:  # Remove todos os alunos
            c.execute("DELETE FROM alunos")
        conn.commit()

# Função para editar o nome ou a nota de um aluno
def editar_aluno(aluno_id, novo_nome=None, nova_nota=None):
    if not novo_nome and nova_nota is None:
        raise ValueError("É necessário informar um novo nome ou uma nova nota.")
    
    with sqlite3.connect('notas.db') as conn:
        c = conn.cursor()
        if novo_nome:
            c.execute("UPDATE alunos SET nome=? WHERE id=?", (novo_nome, aluno_id))
        if nova_nota is not None:
            if 0 <= nova_nota <= 10:
                c.execute("UPDATE alunos SET nota=? WHERE id=?", (nova_nota, aluno_id))
            else:
                raise ValueError("Nota deve estar entre 0 e 10.")
        conn.commit()
