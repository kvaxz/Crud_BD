import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="db_usuario"
)

cursor = conexao.cursor()

def limpar_campos():
    input_id.delete(0, tk.END)
    input_nome.delete(0, tk.END)
    input_email.delete(0, tk.END)
    input_endereco.delete(0, tk.END)

def carregar_usuarios():

    tabela.delete(*tabela.get_children())

    cursor.execute("SELECT * FROM usuarios")

    resultados = cursor.fetchall()

    for linha in resultados:
        tabela.insert("", "end", values=linha)

def novo_usuario():

    nome = input_nome.get()
    email = input_email.get()
    endereco = input_endereco.get()

    if nome == "" or email == "" or endereco == "":
        messagebox.showwarning("Aviso", "Nome, Email e Endereço são obrigatórios")
        return

    sql = "INSERT INTO usuarios (nome, email, endereco) VALUES (%s, %s, %s)"

    valores = (nome, email, endereco)

    cursor.execute(sql, valores)

    conexao.commit()

    messagebox.showinfo("Sucesso", "Usuário cadastrado!")
    carregar_usuarios()
    limpar_campos()

def editar_usuario():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning("Aviso!","Selecionar um Usuário")
        return
    id_usuario = input_id.get()
    nome = input_nome.get()
    email = input_email.get()
    endereco = input_endereco.get()

    sql = """
    UPDATE usuarios
    SET nome = %s, email = %s, endereco = %s
    WHERE id = %s
    """

    valores = (nome, email, endereco, id_usuario)
    cursor.execute(sql, valores)

    conexao.commit()
    carregar_usuarios()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Usuário atualizado!")
    

def excluir_usuario():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning("Aviso!", "Selecionar um Usuário")
        return

    valores = tabela.item(selecionado, "values")
    id_usuario = valores[0]

    sql = "DELETE FROM usuarios WHERE id = %s"

    cursor.execute(sql, (id_usuario,))
    conexao.commit()

    limpar_campos()
    carregar_usuarios()

    messagebox.showinfo("Sucesso", "Usuário excluído!")

def selecionar_usuario(event):
    selecionado = tabela.selection()

    if selecionado:
        limpar_campos()
        valores = tabela.item(selecionado, "values")

        input_id.config(state="normal")
        input_id.delete(0, tk.END)
        input_id.insert(0, valores[0])
        input_id.config(state="readonly")

        input_nome.delete(0, tk.END)
        input_nome.insert(0, valores[1])

        input_email.delete(0, tk.END)
        input_email.insert(0, valores[2])

        input_endereco.delete(0, tk.END)
        input_endereco.insert(0, valores[3])


janela = tk.Tk()
janela.title("Cadastro de usuario")
janela.geometry("750x450")



#Formulario 
frame_form = tk.Frame(janela)
frame_form.pack(pady=10)

tk.Label(frame_form, text="ID: ").grid(row=0, column=0, padx=5, sticky="e")
input_id = tk.Entry(frame_form, width=20)
input_id.grid(row=0, column=1, padx=5)
input_id.config(state="readonly")

tk.Label(frame_form, text="Nome:").grid(row=0, column=2, padx=5, sticky="e")
input_nome = tk.Entry(frame_form, width=40)
input_nome.grid(row=0, column=3, padx=5)

tk.Label(frame_form, text="Email:").grid(row=1, column=0, padx=5, sticky="e")
input_email = tk.Entry(frame_form, width=20)
input_email.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Endereço:").grid(row=1, column=2, padx=5, sticky="e")
input_endereco = tk.Entry(frame_form, width=40)
input_endereco.grid(row=1, column=3, padx=5)

#BOTÕES
frame_button = tk.Frame(janela)
frame_button.pack(pady=10)

btn_novo = tk.Button(frame_button, text="Novo", width=10, command=novo_usuario).grid(row=0, column=0, padx=5)
btn_editar = tk.Button(frame_button, text="Editar", width=10, command=editar_usuario).grid(row=0, column=1, padx=5)
btn_excluir = tk.Button(frame_button, text="Excluir", width=10, command=excluir_usuario).grid(row=0, column=2, padx=5)
btn_limpar = tk.Button(frame_button, text="Limpar", width=10, command=limpar_campos).grid(row=0, column=3, padx=5)

#TABELA
colunas = ("ID", "NOME", "EMAIL", "ENDEREÇO")

tabela = ttk.Treeview(janela, columns=colunas, show="headings")

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=170)

tabela.pack(fill="both", expand=True, padx=20, pady=20)
tabela.bind("<<TreeviewSelect>>", selecionar_usuario)


carregar_usuarios()
janela.mainloop()