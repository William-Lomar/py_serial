#Configurando subdiretorios
from config import*

sys.path.append('classes')
sys.path.append('classes/interface')
sys.path.append('classes/eqps')

#Minhas classes
from app import*

class Login:
    #Tela de login
    def __init__(self,root):
        self.root = root
        self.root.title('Datalogger Py 2.0')
        
        #container Titulo
        containerTitulo = Frame(root)
        containerTitulo.pack(padx=30,pady=30)
        
        titulo = Label(containerTitulo,text="Bem vindo, favor informar usuário e senha")
        titulo.pack(side='top')
        
        #Primeiro container 
        containerOne = Frame(root)
        containerOne.pack(padx=20,pady=10)
        
        usuarioText = Label(containerOne,text="Login:")
        usuarioText.pack(side='left',padx = 15)
        
        self.usuario = Entry(containerOne)
        self.usuario.pack(side='left')
        
        #Segundo container   
        containerDois = Frame(root)
        containerDois.pack(padx=20,pady=20)
                     
        senhaText = Label(containerDois,text="Senha:")
        senhaText.pack(side='left',padx = 15)
        
        self.senha = Entry(containerDois,show='*')
        self.senha.pack(side='left')
        
        #terceiro container
        containerTres = Frame(root)
        containerTres.pack(pady=20)
        
        enviar = Button(containerTres,text="Enviar",command=self.logar)
        enviar.pack(side='top')
        
    def logar(self):
        pegarUsuario = self.usuario.get()
        pegarSenha = self.senha.get()
        
        verificarUsuario = FIREBASE.child('users').order_by_child('usuario').equal_to(pegarUsuario).get()
        contador = len(verificarUsuario.val())
        
        if contador == 0:
            messagebox.showwarning("Erro",'Usuário ou senha incorretos')
        else:
            for users in verificarUsuario.each():
                if users.val()['usuario'] == pegarUsuario and users.val()['senha'] == pegarSenha:
                    self.root.destroy()
            
                    #App
                    app = Tk()
                    App(app)
                    app.mainloop()
                else:
                    messagebox.showwarning("Erro",'Usuário ou senha incorretos')

#Login
login = Tk()
Login(login)
login.mainloop()