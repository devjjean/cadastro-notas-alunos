import tkinter as tk
from tkinter import messagebox, simpledialog
from database import create_table, add_aluno, get_alunos, remover_aluno_do_db, editar_aluno

# Cria a tabela no banco de dados
create_table()

# Variável global para controlar o modo escuro
modo_escuro = False

def toggle_modo_escuro():
    global modo_escuro
    modo_escuro = not modo_escuro
    aplicar_estilo()

def aplicar_estilo():
    bg_color = "#333" if modo_escuro else "#f5f5f5"
    fg_color = "#f5f5f5" if modo_escuro else "#333"
    btn_color = "#444" if modo_escuro else "#4CAF50"
    btn_rm_color = "#aa2222" if modo_escuro else "#d32f2f"

    root.configure(bg=bg_color)
    frame_cadastro.configure(bg=bg_color)
    frame_alunos.configure(bg=bg_color)

    for widget in frame_cadastro.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
            widget.configure(bg=bg_color, fg=fg_color)

    btn_adicionar.configure(bg=btn_color, fg=fg_color)
    btn_limpar_todos.configure(bg=btn_rm_color, fg=fg_color)
    btn_toggle_modo.configure(bg=btn_color, fg=fg_color)

    listar_alunos()

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
            frame = tk.Frame(frame_alunos, bg=root.cget("bg"))
            frame.pack(fill="x", padx=10, pady=5)

            label = tk.Label(frame, text=f"{aluno[1]}: {aluno[2]}", font=("Helvetica", 14), anchor="w", bg=root.cget("bg"), fg="#f5f5f5" if modo_escuro else "#333")
            label.pack(side="left", fill="x", expand=True)

            btn_editar = tk.Button(frame, text="Editar", command=lambda aluno_id=aluno[0]: editar_aluno_ui(aluno_id), bg="#2196F3", fg="white", relief="flat", font=("Helvetica", 12))
            btn_editar.pack(side="right", padx=5)

            btn_remover = tk.Button(frame, text="Remover", command=lambda aluno_id=aluno[0]: remover_aluno(aluno_id), bg="#d32f2f", fg="white", relief="flat", font=("Helvetica", 12))
            btn_remover.pack(side="right", padx=5)
    else:
        label = tk.Label(frame_alunos, text="Não há alunos para exibir.", font=("Helvetica", 14), bg=root.cget("bg"), fg="#f5f5f5" if modo_escuro else "#333")
        label.pack(pady=20)

def limpar_todos():
    alunos = get_alunos()
    if alunos:
        if messagebox.askyesno("Confirmação", "Você tem certeza que deseja remover todos os alunos?"):
            remover_aluno_do_db()
            listar_alunos()
    else:
        messagebox.showinfo("Aviso", "Não há alunos para limpar.")

def remover_aluno(aluno_id=None):
    if aluno_id:
        remover_aluno_do_db(aluno_id)
        listar_alunos()

def editar_aluno_ui(aluno_id):
    aluno = next((a for a in get_alunos() if a[0] == aluno_id), None)
    if aluno:
        novo_nome = simpledialog.askstring("Editar Nome", "Novo nome:", initialvalue=aluno[1])
        nova_nota = simpledialog.askstring("Editar Nota", "Nova nota:", initialvalue=aluno[2])
        try:
            nova_nota = float(nova_nota)
            if novo_nome and 0 <= nova_nota <= 10:
                editar_aluno(aluno_id, novo_nome, nova_nota)
                listar_alunos()
                messagebox.showinfo("Sucesso", "Aluno editado com sucesso!")
            else:
                messagebox.showerror("Erro", "Nota deve ser entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser um número.")
    else:
        messagebox.showerror("Erro", "Aluno não encontrado.")

# Configuração da janela principal
root = tk.Tk()
root.title("Cadastro de Notas")

# Centraliza a janela na tela
window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Frame para cadastro de aluno
frame_cadastro = tk.Frame(root)
frame_cadastro.pack(pady=30)

label_nome = tk.Label(frame_cadastro, text="Nome:", font=("Helvetica", 14))
label_nome.grid(row=0, column=0, pady=10, sticky="e", padx=10)
entry_nome = tk.Entry(frame_cadastro, font=("Helvetica", 12))
entry_nome.grid(row=0, column=1, pady=10, padx=10)

label_nota = tk.Label(frame_cadastro, text="Nota:", font=("Helvetica", 14))
label_nota.grid(row=1, column=0, pady=10, sticky="e", padx=10)
entry_nota = tk.Entry(frame_cadastro, font=("Helvetica", 12))
entry_nota.grid(row=1, column=1, pady=10, padx=10)

btn_adicionar = tk.Button(frame_cadastro, text="Adicionar Aluno", command=adicionar_aluno, font=("Helvetica", 12))
btn_adicionar.grid(row=2, columnspan=2, pady=20)

# Frame para listar alunos
frame_alunos = tk.Frame(root)
frame_alunos.pack(pady=10, fill="both", expand=True)

# Botão para limpar todos os alunos
btn_limpar_todos = tk.Button(root, text="Limpar Todos", command=limpar_todos, font=("Helvetica", 12))
btn_limpar_todos.pack(pady=10)

# Botão para alternar o modo escuro
btn_toggle_modo = tk.Button(root, text="Alternar Modo Escuro", command=toggle_modo_escuro, font=("Helvetica", 12))
btn_toggle_modo.pack(pady=10)

# Aplica estilo inicial e exibe alunos
aplicar_estilo()

root.mainloop()
