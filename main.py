import tkinter as tk
from tkinter import messagebox
import utils


# Página de perfil
def pagina_perfil(usuario):
    janela = tk.Tk()
    janela.title("Perfil de " + usuario['username'])
    janela.geometry("600x500")

    label_titulo = tk.Label(janela, text=f"Bem-vindo, {usuario['username']}!", font=("Arial", 24), fg="blue")
    label_titulo.pack(pady=30)

    if usuario.get('role') == 'admin':
        lista_botao = tk.Button(janela, text="Ver lista de usuários", width=20, height=2, command=ver_lista_usuarios, bg="blue", fg="white")
        lista_botao.pack(pady=15)

    botao_editar = tk.Button(janela, text="Editar Perfil", width=20, height=2, command=lambda: editar_perfil(usuario), bg="blue", fg="white")
    botao_editar.pack(pady=15)

    botao_excluir = tk.Button(janela, text="Excluir Perfil", width=20, height=2, command=lambda: excluir_perfil(usuario, janela), bg="blue", fg="white")
    botao_excluir.pack(pady=15)

    janela.mainloop()

# Página de Login
def criar_pagina_login():
    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("600x500")

    label_titulo = tk.Label(janela, text="Login", font=("Arial",24), fg="blue")
    label_titulo.pack(pady=20)

    label_usuario = tk.Label(janela, text="Usuário")
    label_usuario.pack()

    entrada_usuario = tk.Entry(janela)
    entrada_usuario.pack()

    label_senha = tk.Label(janela, text="Senha")
    label_senha.pack()

    entrada_senha = tk.Entry(janela, show="*")
    entrada_senha.pack()

    def tentar_login():
        usuario = utils.verificar_login(entrada_usuario.get(), entrada_senha.get())
        if usuario:
            janela.destroy()
            pagina_perfil(usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.", parent=janela)

    botao_entrar = tk.Button(janela, text="Entrar", width=20, height=2, command=tentar_login, bg="blue", fg="white")
    botao_entrar.pack(pady=10)

    janela.mainloop()

# Página de Cadastro
def criar_pagina_cadastro():
    janela = tk.Tk()
    janela.title("Cadastro")
    janela.geometry("600x500")

    label_titulo = tk.Label(janela, text="Cadastro", font=("Arial",24), fg="blue")
    label_titulo.pack(pady=20)

    tk.Label(janela, text="Usuário").pack()
    entrada_usuario = tk.Entry(janela)
    entrada_usuario.pack()

    tk.Label(janela, text="Senha").pack()
    entrada_senha = tk.Entry(janela, show="*")
    entrada_senha.pack()

    tk.Label(janela, text="Email").pack()
    entrada_email = tk.Entry(janela)
    entrada_email.pack()

    def tentar_cadastro():
        if not entrada_usuario.get() or not entrada_senha.get() or not entrada_email.get():
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=janela)
        elif not utils.email_valido(entrada_email.get()):
            messagebox.showerror("Erro", "Email inválido.", parent=janela)
        elif utils.verificar_email_existente(entrada_email.get()):
            messagebox.showerror("Erro", "Email já cadastrado.", parent=janela)
        else:
            dados = utils.carregar_dados()
            dados['users'].append({
                'username': entrada_usuario.get(),
                'password': entrada_senha.get(),
                'email': entrada_email.get(),
                'role': 'user'
            })
            utils.salvar_dados(dados)
            messagebox.showinfo("Sucesso", "Cadastro realizado!", parent=janela)
            janela.destroy()
            criar_pagina_login()

    botao_cadastrar = tk.Button(janela, text="Cadastrar", width=20, height=2, command=tentar_cadastro, bg="blue", fg="white")
    botao_cadastrar.pack(pady=10)

    janela.mainloop()

# Página principal
def criar_pagina_principal():
    janela = tk.Tk()
    janela.geometry("600x500")
    janela.title("Serviço VPN")

    label_bem_vindo = tk.Label(janela, text="Bem-vindo ao serviço VPN!", font=("Arial", 24), fg="blue")
    label_bem_vindo.pack(pady=40)
    
    botao_login = tk.Button(janela, text="Login", width=20, height=2, command=criar_pagina_login, bg="blue", fg="white")
    botao_cadastro = tk.Button(janela, text="Cadastro", width=20, height=2, command=criar_pagina_cadastro, bg='blue', fg='white')

    botao_login.pack(pady=20)
    botao_cadastro.pack(pady=20)

    janela.mainloop()

# Função para listar usuários (somente admin)
def ver_lista_usuarios():
    dados = utils.carregar_dados()
    janela = tk.Tk()
    janela.geometry("500x400")
    janela.title("Lista de Usuários")

    label_titulo = tk.Label(janela, text="Lista de usuários", font=("Arial",24), fg="blue")
    label_titulo.pack(pady=20)
    
    for user in dados['users']:
        tk.Label(janela, text=f"Usuário: {user['username']} | Email: {user['email']}").pack()

    botao_lista = tk.Button(janela, text="Fechar", width=20, height=2, command=janela.destroy, bg="blue", fg="white")
    botao_lista.pack(pady=20)

    janela.mainloop()

# Editar perfil do usuário
def editar_perfil(usuario):
    janela = tk.Tk()
    janela.title("Editar Perfil")
    janela.geometry("600x500")

    tk.Label(janela, text="Novo Usuário").pack()
    novo_usuario = tk.Entry(janela)
    novo_usuario.insert(0, usuario['username'])
    novo_usuario.pack()

    tk.Label(janela, text="Nova Senha").pack()
    nova_senha = tk.Entry(janela, show="*")
    nova_senha.insert(0, usuario['password'])
    nova_senha.pack()

    def salvar_alteracoes():
        dados = utils.carregar_dados()
        for user in dados['users']:
            if user['email'] == usuario['email']:
                user['username'] = novo_usuario.get()
                user['password'] = nova_senha.get()
        utils.salvar_dados(dados)
        messagebox.showinfo("Sucesso", "Perfil atualizado!", parent = janela)
        janela.destroy()

    botao_salvar = tk.Button(janela, text="Salvar", width=20, height=2, command=salvar_alteracoes, bg="blue", fg="white")
    botao_cancelar = tk.Button(janela, text="Cancelar", width=20, height=2, command=janela.destroy, bg="blue", fg="white")

    botao_salvar.pack(pady=20)
    botao_cancelar.pack(pady=20)

    janela.mainloop()

# Excluir perfil do usuário
def excluir_perfil(usuario, janela_antiga):
    resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o perfil?", parent=janela_antiga)
    if resposta:
        dados = utils.carregar_dados()
        dados['users'] = [user for user in dados['users'] if user['email'] != usuario['email']]
        utils.salvar_dados(dados)
        messagebox.showinfo("Sucesso", "Perfil excluído!", parent=janela_antiga)
        janela_antiga.destroy()
        criar_pagina_principal()

# Iniciar o sistema
if __name__ == "__main__":
    criar_pagina_principal()
