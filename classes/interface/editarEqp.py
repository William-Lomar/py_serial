from tkinter.messagebox import showinfo
from config import*

class EditarEqp:
    def atualizar(self):
        novoNS = self.valorNS.get()
        novoSerialPort = self.valorSerial.get()
        
        original = FIREBASE.child('equipamentos').order_by_child("TAG").equal_to(self.tag).get()
        
        for original in original.each():
            key = original.key()

        dados = {
            key+"/": {
                "equipamento": self.equipamento,
                "NS": novoNS,
                "serialPort": novoSerialPort,
                "TAG":self.tag,
                "estacao":ESTACAO
            }
        }
        
        FIREBASE.child('equipamentos').update(dados)
        
        self.tabela.delete(self.item)
        
        self.tabela.insert('','end',values=(self.equipamento,novoNS,novoSerialPort,self.tag))
        
        messagebox.showinfo("Update",'Usuário atualizado com sucesso!')
        self.root.destroy()
        
    def __init__(self,root,tabela):
        self.root = root
        self.tabela = tabela

        self.item = self.tabela.selection()[0]
        self.valores = self.tabela.item(self.item,'values')
        
        #Valores atuais
        self.equipamento = self.valores[0]
        self.ns = self.valores[1]
        self.serialPort = self.valores[2]
        self.tag = self.valores[3]
        
        self.root.title("Editar Equipamento")
        
        #Titulo 
        titulo = Label(self.root,text='Editar Equipamento')
        titulo.pack(padx=30,pady=30)
        
        #C1
        c1 = Frame(self.root)
        c1.pack(padx=20,pady=10)
        
        self.labelEqp = Label(c1,text="Equipamento:")
        self.labelEqp.pack(side=LEFT, padx=5,pady=5)
        
        self.labelEqp = Label(c1,text=self.equipamento)
        self.labelEqp.pack(side=LEFT, padx=5,pady=5)
        
        #C2
        c2 = Frame(self.root)
        c2.pack(padx=20,pady=10)
        
        self.labelNS = Label(c2,text="Número de Série:")
        self.labelNS.pack(side=LEFT, padx=5,pady=5)
        
        self.valorNS = Entry(c2)
        self.valorNS.insert(0,self.ns)
        self.valorNS.pack(side=LEFT, padx=5,pady=5)
        
        
        #C3
        c3 = Frame(self.root)
        c3.pack(padx=20,pady=10)
        
        self.labelSerial = Label(c3,text="Porta Serial:")
        self.labelSerial.pack(side=LEFT, padx=5,pady=5)
        
        self.valorSerial = Entry(c3)
        self.valorSerial.insert(0,self.serialPort)
        self.valorSerial.pack(side=LEFT, padx=5,pady=5)
        
        #C4
        c4 = Frame(self.root)
        c4.pack(padx=20,pady=10)
        
        self.labelTAG = Label(c4,text="TAG:")
        self.labelTAG.pack(side=LEFT, padx=5,pady=5)
        
        self.labelTAG = Label(c4,text=self.tag)
        self.labelTAG.pack(side=LEFT, padx=5,pady=5)
        
        #C5
        c5 = Frame(self.root)
        c5.pack(padx=20,pady=10)
        
        self.atualizar = Button(c5,text="Atualizar",command=self.atualizar)
        self.atualizar.pack(pady=20)