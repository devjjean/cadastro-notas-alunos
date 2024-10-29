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
    c.execute("SELECT * FROM alunos")
    alunos = c.fetchall()
    conn.close()
    return alunos