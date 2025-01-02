import tkinter as tk
from tkinter import messagebox
from database import create_table, add_aluno, get_alunos, remover_aluno_do_db

# Cria a tabela no banco de dados
create_table()

def adicionar_aluno():
    nome = entry_nome.get()
    nota = entry_nota.get()
    
    if nome and nota:
        try:
            nota = float(nota)
            if 0 <= nota <= 10:
                add_aluno(nome, nota)
                messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
                entry_nome.delete(0, tk.END)
                entry_nota.delete(0, tk.END)
                listar_alunos()
            else:
                messagebox.showerror("Erro", "Nota deve ser entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número.")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos.")

def listar_alunos():
    for widget in frame_alunos.winfo_children():
        widget.destroy()
    
    alunos = get_alunos()
    if alunos:
        for aluno in alunos:
            label = tk.Label(frame_alunos, text=f"{aluno[1]}: {aluno[2]}", font=("Helvetica", 14), bg="#eaeaea", anchor="w")
            label.pack(fill="x", padx=20, pady=10)

            btn_remover = tk.Button(frame_alunos, text="Remover", command=lambda aluno_id=aluno[0]: remover_aluno(aluno_id), 
                                    bg="#d32f2f", fg="white", font=("Helvetica", 12), relief="flat")
            btn_remover.pack(pady=5, padx=20, fill="x")
    else:
        messagebox.showinfo("Aviso", "Não há alunos para exibir.")

# Função para limpar todos os alunos
def limpar_todos():
    alunos = get_alunos()
    if alunos:
        if messagebox.askyesno("Confirmação", "Você tem certeza que deseja remover todos os alunos?"):
            remover_aluno_do_db()  # Limpa todos os alunos
            listar_alunos()
    else:
        messagebox.showinfo("Aviso", "Não há alunos para limpar.")

# Função para remover um aluno específico
def remover_aluno(aluno_id=None):
    if aluno_id:
        remover_aluno_do_db(aluno_id)  # Remove o aluno com o ID especificado
        listar_alunos()

# Configuração da janela principal
root = tk.Tk()
root.title("Cadastro de Notas")
root.configure(bg="#f5f5f5")

# Centraliza a janela na tela
window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Frame para cadastro de aluno
frame_cadastro = tk.Frame(root, bg="#f5f5f5")
frame_cadastro.pack(pady=30)

# Estilizando as labels e entradas
label_nome = tk.Label(frame_cadastro, text="Nome:", font=("Helvetica", 14), fg="#333", bg="#f5f5f5")
label_nome.grid(row=0, column=0, pady=10, sticky="e", padx=10)
entry_nome = tk.Entry(frame_cadastro, font=("Helvetica", 12), relief="solid", bd=2)
entry_nome.grid(row=0, column=1, pady=10, padx=10, ipadx=10, ipady=5)

label_nota = tk.Label(frame_cadastro, text="Nota:", font=("Helvetica", 14), fg="#333", bg="#f5f5f5")
label_nota.grid(row=1, column=0, pady=10, sticky="e", padx=10)
entry_nota = tk.Entry(frame_cadastro, font=("Helvetica", 12), relief="solid", bd=2)
entry_nota.grid(row=1, column=1, pady=10, padx=10, ipadx=10, ipady=5)

# Botão para adicionar aluno
btn_adicionar = tk.Button(frame_cadastro, text="Adicionar Aluno", command=adicionar_aluno, 
                          bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="flat", width=20)
btn_adicionar.grid(row=2, columnspan=2, pady=20)

# Frame para listar alunos
frame_alunos = tk.Frame(root, bg="#f5f5f5")
frame_alunos.pack(pady=10, fill="both", expand=True)

# Botão para limpar todos os alunos
btn_limpar_todos = tk.Button(root, text="Limpar Todos", command=limpar_todos, bg="#d32f2f", fg="white", font=("Helvetica", 12), relief="flat", width=20)
btn_limpar_todos.pack(pady=20)

# Chama a função listar alunos para exibir a lista ao abrir a aplicação
listar_alunos()

root.mainloop()
