import tkinter as tk
from tkinter import messagebox
from database import create_table, add_aluno, get_alunos

# Cria a tabela no banco de dados
create_table()

def adicionar_aluno():
    nome = entry_nome.get()
    nota = entry_nota.get()
    
    if nome and nota:
        try:
            nota = float(nota)
            add_aluno(nome, nota)
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
            entry_nome.delete(0, tk.END)
            entry_nota.delete(0, tk.END)
            listar_alunos()
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número.")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

def listar_alunos():
    for widget in frame_alunos.winfo_children():
        widget.destroy()
    
    alunos = get_alunos()
    for aluno in alunos:
        label = tk.Label(frame_alunos, text=f"{aluno[1]}: {aluno[2]}")
        label.pack()

# Configuração da janela principal
root = tk.Tk()
root.title("Cadastro de Notas")

frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=10)

label_nome = tk.Label(frame_cadastro, text="Nome:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1)

label_nota = tk.Label(frame_cadastro, text="Nota:")
label_nota.grid(row=1, column=0)
entry_nota = tk.Entry(frame_cadastro)
entry_nota.grid(row=1, column=1)

btn_adicionar = tk.Button(frame_cadastro, text="Adicionar Aluno", command=adicionar_aluno)
btn_adicionar.grid(row=2, columnspan=2)

frame_alunos = tk.Frame(root)
frame_alunos.pack(pady=10)

listar_alunos()

root.mainloop()