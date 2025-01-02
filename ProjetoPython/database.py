import sqlite3

def create_table():
    conn = sqlite3.connect('notas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS alunos
                 (id INTEGER PRIMARY KEY,
                  nome TEXT,
                  nota REAL)''')
    conn.commit()
    conn.close()

def add_aluno(nome, nota):
    conn = sqlite3.connect('notas.db')
    c = conn.cursor()
    c.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
    conn.commit()
    conn.close()

def get_alunos():
    conn = sqlite3.connect('notas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM alunos ORDER BY nota DESC")
    alunos = c.fetchall()
    conn.close()
    return alunos

def remover_aluno_do_db(aluno_id=None):
    conn = sqlite3.connect('notas.db')
    c = conn.cursor()
    if aluno_id:  # Se o aluno_id for passado, remove o aluno específico
        c.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
    else:  # Se nenhum aluno_id for passado, remove todos os alunos
        c.execute("DELETE FROM alunos")
    conn.commit()
    conn.close()
