import tkinter as tk
from tkinter import messagebox
import utils

# Classe base para janelas
class JanelaBase(tk.Toplevel):
    def __init__(self, title, geometry="600x500"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)

# Herança: A página principal herda de JanelaBase
class PaginaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Serviço VPN")
        self.label_bem_vindo = tk.Label(self, text="Bem-vindo ao serviço VPN!", font=("Arial", 24), fg="blue")
        self.label_bem_vindo.pack(pady=40)

        self.botao_login = tk.Button(self, text="Login", width=20, height=2, command=self.abrir_login, bg="blue", fg="white")
        self.botao_login.pack(pady=20)

        self.botao_cadastro = tk.Button(self, text="Cadastro", width=20, height=2, command=self.abrir_cadastro, bg="blue", fg="white")
        self.botao_cadastro.pack(pady=20)

    def abrir_login(self):
        PaginaLogin(self)

    def abrir_cadastro(self):
        PaginaCadastro(self)

# Composição: A página de cadastro é composta pela classe de validação e cadastro
class PaginaCadastro(JanelaBase):
    def __init__(self, master=None):
        super().__init__("Cadastro")
        self.master = master
        self.label_titulo = tk.Label(self, text="Cadastro", font=("Arial",24), fg="blue")
        self.label_titulo.pack(pady=20)

        tk.Label(self, text="Usuário").pack()
        self.entrada_usuario = tk.Entry(self)
        self.entrada_usuario.pack()

        tk.Label(self, text="Senha").pack()
        self.entrada_senha = tk.Entry(self, show="*")
        self.entrada_senha.pack()

        tk.Label(self, text="Email").pack()
        self.entrada_email = tk.Entry(self)
        self.entrada_email.pack()

        self.botao_cadastrar = tk.Button(self, text="Cadastrar", width=20, height=2, command=self.tentar_cadastro, bg="blue", fg="white")
        self.botao_cadastrar.pack(pady=10)

    def tentar_cadastro(self):
        if not self.entrada_usuario.get() or not self.entrada_senha.get() or not self.entrada_email.get():
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
        elif not utils.email_valido(self.entrada_email.get()):
            messagebox.showerror("Erro", "Email inválido.", parent=self)
        elif utils.verificar_email_existente(self.entrada_email.get()):
            messagebox.showerror("Erro", "Email já cadastrado.", parent=self)
        else:
            dados = utils.carregar_dados()
            dados['users'].append({
                'username': self.entrada_usuario.get(),
                'password': self.entrada_senha.get(),
                'email': self.entrada_email.get(),
                'role': 'user'
            })
            utils.salvar_dados(dados)
            messagebox.showinfo("Sucesso", "Cadastro realizado!", parent=self)
            self.destroy()
            PaginaLogin(self.master)

# Associação: A página de login utiliza a classe utils para verificar os dados do usuário
class PaginaLogin(JanelaBase):
    def __init__(self, master=None):
        super().__init__("Login")
        self.master = master

        self.label_titulo = tk.Label(self, text="Login", font=("Arial", 24), fg="blue")
        self.label_titulo.pack(pady=20)

        self.label_usuario = tk.Label(self, text="Usuário")
        self.label_usuario.pack()

        self.entrada_usuario = tk.Entry(self)
        self.entrada_usuario.pack()

        self.label_senha = tk.Label(self, text="Senha")
        self.label_senha.pack()

        self.entrada_senha = tk.Entry(self, show="*")
        self.entrada_senha.pack()

        self.botao_entrar = tk.Button(self, text="Entrar", width=20, height=2, command=self.tentar_login, bg="blue", fg="white")
        self.botao_entrar.pack(pady=10)

    def tentar_login(self):
        usuario = utils.verificar_login(self.entrada_usuario.get(), self.entrada_senha.get())
        if usuario:
            self.destroy()
            PaginaPerfil(self.master, usuario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.", parent=self)

# Agregação: A página de perfil permite interagir com os dados dos usuários
class PaginaPerfil(JanelaBase):
    def __init__(self, master, usuario):
        super().__init__(f"Perfil de {usuario['username']}")
        self.master = master
        self.usuario = usuario

        self.label_titulo = tk.Label(self, text=f"Bem-vindo, {self.usuario['username']}!", font=("Arial", 24), fg="blue")
        self.label_titulo.pack(pady=30)

        if self.usuario.get('role') == 'admin':
            lista_botao = tk.Button(self, text="Ver lista de usuários", width=20, height=2, command=self.ver_lista_usuarios, bg="blue", fg="white")
            lista_botao.pack(pady=15)

        botao_editar = tk.Button(self, text="Editar Perfil", width=20, height=2, command=self.editar_perfil, bg="blue", fg="white")
        botao_editar.pack(pady=15)

        botao_excluir = tk.Button(self, text="Excluir Perfil", width=20, height=2, command=self.excluir_perfil, bg="blue", fg="white")
        botao_excluir.pack(pady=15)

    def ver_lista_usuarios(self):
        VerListaUsuarios(self)

    def editar_perfil(self):
        EditarPerfil(self, self.usuario)

    def excluir_perfil(self):
        resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o perfil?", parent=self)
        if resposta:
            dados = utils.carregar_dados()
            dados['users'] = [user for user in dados['users'] if user['email'] != self.usuario['email']]
            utils.salvar_dados(dados)
            messagebox.showinfo("Sucesso", "Perfil excluído!", parent=self)
            self.destroy()
            PaginaPrincipal()

# Outra página utilizando composição para lista de usuários (somente admin)
class VerListaUsuarios(JanelaBase):
    def __init__(self, master):
        super().__init__("Lista de Usuários")
        dados = utils.carregar_dados()

        label_titulo = tk.Label(self, text="Lista de usuários", font=("Arial", 24), fg="blue")
        label_titulo.pack(pady=20)

        for user in dados['users']:
            tk.Label(self, text=f"Usuário: {user['username']} | Email: {user['email']}").pack()

        botao_fechar = tk.Button(self, text="Fechar", width=20, height=2, command=self.destroy, bg="blue", fg="white")
        botao_fechar.pack(pady=20)

# Editar perfil usando herança e associação com os dados do usuário
class EditarPerfil(JanelaBase):
    def __init__(self, master, usuario):
        super().__init__("Editar Perfil")
        self.master = master
        self.usuario = usuario

        tk.Label(self, text="Novo Usuário").pack()
        self.novo_usuario = tk.Entry(self)
        self.novo_usuario.insert(0, usuario['username'])
        self.novo_usuario.pack()

        tk.Label(self, text="Nova Senha").pack()
        self.nova_senha = tk.Entry(self, show="*")
        self.nova_senha.insert(0, usuario['password'])
        self.nova_senha.pack()

        botao_salvar = tk.Button(self, text="Salvar", width=20, height=2, command=self.salvar_alteracoes, bg="blue", fg="white")
        botao_salvar.pack(pady=20)

        botao_cancelar = tk.Button(self, text="Cancelar", width=20, height=2, command=self.destroy, bg="blue", fg="white")
        botao_cancelar.pack(pady=20)

    def salvar_alteracoes(self):
        dados = utils.carregar_dados()
        for user in dados['users']:
            if user['email'] == self.usuario['email']:
                user['username'] = self.novo_usuario.get()
                user['password'] = self.nova_senha.get()
        utils.salvar_dados(dados)
        messagebox.showinfo("Sucesso", "Perfil atualizado!", parent=self)
        self.destroy()

# Iniciar o sistema
if __name__ == "__main__":
    app = PaginaPrincipal()
    app.mainloop()

