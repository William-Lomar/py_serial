from config import*
from classes.interface.editarEqp import*

class Equipamentos:
    def AddEqp(self):
        eqp = self.valorEqp.get()
        ns = self.valorNS.get()
        portSerial = self.valorSerial.get()
        tag = self.valorTAG.get()
        
        if eqp == "" or ns == "" or portSerial == '' or tag == '':
            messagebox.showwarning("Erro","Favor preencher todos os campos solicitados")
            return
        
        eqp = {
            "equipamentos/"+FIREBASE.generate_key(): {
                "equipamento": eqp,
                "NS":ns,
                "serialPort":portSerial,
                "TAG":tag,
                "estacao":ESTACAO 
            }
        }        
        
        #Verifica se já existe alguma tag cadastrada no banco
        verificaTag = FIREBASE.child('equipamentos').order_by_child('TAG').equal_to(tag).get()
        
        #Verifica se já existe porta com cadastrada na estação
        verificaCOM = FIREBASE.child('equipamentos').order_by_child('serialPort').equal_to(portSerial).get()
        jaExisteCom = False
        
        for com in verificaCOM.each():
            if com.val()['estacao'] == ESTACAO:
                jaExisteCom = True
        
        
        if len(verificaTag.val()) == 0 and not jaExisteCom:
            FIREBASE.child().update(eqp)
            #Inserindo valores na tabela
            dados = FIREBASE.child("equipamentos").order_by_child("TAG").equal_to(tag).get()
            
            for eqps in dados.each():
                equipamento = eqps.val()["equipamento"]
                ns = eqps.val()["NS"]
                serialPort = eqps.val()["serialPort"]
                tag = eqps.val()["TAG"]
                
                self.tabela.insert('','end',values=(equipamento,ns,serialPort,tag))
                self.tabelaBase.insert('','end',values=(tag,'','','','Serviço Parado'),iid=tag)
                
            
            self.valorEqp.delete(0,'end')
            self.valorNS.delete(0,'end')
            self.valorSerial.delete(0,'end')
            self.valorTAG.delete(0,'end')
        else:
            if not len(verificaTag.val()) == 0:
                messagebox.showwarning("Erro","TAG já existe no banco")
            elif jaExisteCom:
                messagebox.showwarning("Erro","Porta COM selecionada já está sendo utilizada")
        
    def EditarEqp(self):
        editarEqp = Toplevel(self.root)
        EditarEqp(editarEqp,self.tabela)
    
    def ApagarEqp(self):
        continuar = messagebox.askyesno("Apagar Equipamento", "Ao apagar equipamento todos os dados do equipamento serão deletados, deseja continuar?")
        
        if continuar:
            item = self.tabela.selection()[0]
            tag = self.tabela.item(item,'values')[3]
            
            self.tabela.delete(item)
            self.tabelaBase.delete(tag)
            
            #Remover dados com a msm tag
            dados = FIREBASE.child('dados').order_by_child("TAG").equal_to(tag).get()
            for dados in dados.each():
                key = dados.key()
                FIREBASE.child('dados').child(key).remove()
            
            equipamento = FIREBASE.child('equipamentos').order_by_child('TAG').equal_to(tag).get()
            for eqp in equipamento.each():
                FIREBASE.child('equipamentos').child(eqp.key()).remove()
    
    def __init__(self,root,tabelaBase):
        self.tabelaBase = tabelaBase
        self.root = root
        self.root.title("Configurar Equipamentos")  
        
        #Botão adicionar equipamento
        c1 = Frame(self.root)
        c1.pack(fill=X)
        
        self.labelEqp = Label(c1,text="Equipamento:")
        self.labelEqp.pack(side=LEFT, padx=5)
        
        self.valorEqp = Combobox(c1,values=['BAM1020'],state='readonly')
        self.valorEqp.pack(side=LEFT, padx=5)
        
        self.labelNS = Label(c1,text="Número de Série:")
        self.labelNS.pack(side=LEFT, padx=5)
        
        self.valorNS = Entry(c1)
        self.valorNS.pack(side=LEFT, padx=5)
        
        self.labelSerial = Label(c1,text="Porta Serial:")
        self.labelSerial.pack(side=LEFT, padx=5)
        
        self.valorSerial = Entry(c1)
        self.valorSerial.pack(side=LEFT, padx=5)
        
        self.labelTAG = Label(c1,text="TAG:")
        self.labelTAG.pack(side=LEFT, padx=5)
        
        self.valorTAG = Entry(c1)
        self.valorTAG.pack(side=LEFT, padx=5)
        
        self.addEquipamento = Button(c1,text="Adicionar Equipamento",command=self.AddEqp)
        self.addEquipamento.pack(side=RIGHT,padx=10,pady=20)
        
        #Editar e Apagar falta config
        self.editarEquipamento = Button(c1,text="Editar Equipamento",command=self.EditarEqp)
        self.editarEquipamento.pack(side=RIGHT,padx=10,pady=20)
        
        self.apagarEquipamento = Button(c1,text="Apagar Equipamento",command=self.ApagarEqp)
        self.apagarEquipamento.pack(side=RIGHT,padx=10,pady=20)
        
        #tabela
        c2 = Frame(self.root)
        c2.pack()
        
        self.tabela = Treeview(c2,selectmode='browse',columns=('column1','column2','column3','column4'), show='headings')
        
        #configurando colunas
        self.tabela.column("column1", anchor=CENTER)    
        self.tabela.column("column2", anchor=CENTER)   
        self.tabela.column("column3", anchor=CENTER)   
        self.tabela.column("column4", anchor=CENTER)
        
        #configurando header
        self.tabela.heading("column1", text="Equipamento")    
        self.tabela.heading("column2", text="NS")   
        self.tabela.heading("column3", text="Porta Serial")   
        self.tabela.heading("column4", text="TAG")   
        
        #Config barra de rolagem 
        self.sb = Scrollbar(c2, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y) 
        
        self.tabela.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.tabela.yview)
        
        #Inserindo valores na tabela
        dados = FIREBASE.child("equipamentos").order_by_child("estacao").equal_to(ESTACAO).get()
        
        for eqps in dados.each():
            equipamento = eqps.val()["equipamento"]
            ns = eqps.val()["NS"]
            serialPort = eqps.val()["serialPort"]
            tag = eqps.val()["TAG"]
            
            self.tabela.insert('','end',values=(equipamento,ns,serialPort,tag))

        self.tabela.pack(side=LEFT)
      