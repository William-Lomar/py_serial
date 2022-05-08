from config import*

#Minhas classes
from classes.setInterval import*
from classes.interface.dados import*
from classes.interface.recuperarDados import*
from classes.interface.equipamentos import*
from classes.interface.ftp import*
from classes.interface.terminal import*
from classes.eqps.bam import*

class App:
    #Funções de chamada de classe
    def sair(self):
        self.root.destroy()
        
    def pgDados(self):
        janelaDados = Toplevel(self.root)
        Dados(janelaDados)
    
    def pgRecuperarDados(self):
        janelaRecuperarDados = Toplevel(self.root)
        RecuperarDados(janelaRecuperarDados)
        
    def pgEquipamentos(self):
        janelaEquipamentos = Toplevel(self.root)
        Equipamentos(janelaEquipamentos,self.tabela)
    
    def pgFTP(self):
        janelaFTP = Toplevel(self.root)
        Ftp(janelaFTP)
        
    def terminal(self):
        janelaTerminal = Toplevel(self.root)
        Terminal(janelaTerminal)
    
    #Config Coleta
    def coletarDados(self):
        if self.realizarColeta:
            itens = self.tabela.get_children()
            for tag in itens:
                info = FIREBASE.child('equipamentos').order_by_child('TAG').equal_to(tag).get()
                for info in info.each():
                    serialPort = info.val()['serialPort']

                bam = BAM(serialPort,9600)
                dados = bam.coletarDadosCSV()
                
                if dados:
                    arquivo = open('respostaBam.csv','w')
                    arquivo.writelines(dados)
                    arquivo.close()
                    
                    tabela = pandas.read_csv('respostaBam.csv',sep=',')
                    qntLinhas = len(tabela)

                    if qntLinhas == 0:
                        lastData = bam.lastDataCSV()
                        arquivo = open('respostaBam.csv','w')
                        arquivo.writelines(lastData)
                        arquivo.close()
                        
                        tabela = pandas.read_csv('respostaBam.csv',sep=',')

                        self.tabela.item(tag,values=(tag,tabela['Conc(mg/m3)'][0],tabela['Time'][0],"V","Coletando dados"))
                    else:
                        for i in range(qntLinhas):
                            #Validar se já existe data no sistema
                            jaExiste = False
                            dataBanco = FIREBASE.child('dados').order_by_child("data").equal_to(tabela['Time'][i]).get()
                            
                            for dataBanco in dataBanco.each():
                                if dataBanco.val()['data'] == tabela['Time'][i] and dataBanco.val()['TAG'] == tag:
                                    jaExiste = True

                            if jaExiste:
                                continue
                            
                            data = {
                                FIREBASE.generate_key():{
                                    "TAG": tag,
                                    "data": tabela['Time'][i],
                                    "flag": 'V',
                                    "valor":tabela['Conc(mg/m3)'][i]
                                }
                            }
                            
                            FIREBASE.child('dados').update(data)
                        
                        #Inserindo last data
                        lastData = bam.lastDataCSV()
                        arquivo = open('respostaBam.csv','w')
                        arquivo.writelines(lastData)
                        arquivo.close()
                        
                        tabela = pandas.read_csv('respostaBam.csv',sep=',')

                        self.tabela.item(tag,values=(tag,tabela['Conc(mg/m3)'][0],tabela['Time'][0],"V","Coletando dados"))
                    
                else:
                    #Falha de comunicação
                    self.tabela.item(tag,values=(tag,'','','',"Equipamento não encontrado"))
                        
        else:
            itens = self.tabela.get_children()
            for tag in itens:
                self.tabela.item(tag,values=(tag,'','','',"Serviço parado"))
                
                
    def iniciarColeta(self):
        self.menuColeta.entryconfig(1,state=DISABLED)
        self.menuColeta.entryconfig(2,state=NORMAL)
        
        self.realizarColeta = True

    def finalizarColeta(self):
        self.menuColeta.entryconfig(1,state=NORMAL)
        self.menuColeta.entryconfig(2,state=DISABLED)
        
        self.realizarColeta = False
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Deseja realmente sair?"):
            self.root.destroy()
            os._exit(1)

    #App principal
    def __init__(self,root):
        #root
        self.root = root
        self.root.title("Datalogger Py 2.0")
        
        #Config fechamento de janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #Config coleta 
        self.coleta = SetInterval(10,self.coletarDados)
        self.coleta.start()
        self.realizarColeta = False
        
        #Definindo styles
        style = Style()
        style.theme_use('default')
        
        #Menu
        menuBar = Menu(self.root)
        self.root.config(menu=menuBar)
        #Falta criar comandos do Menu
        
        #Coleta
        self.menuColeta = Menu(menuBar)
        self.menuColeta.add_command(label="Iniciar Coleta",command=self.iniciarColeta)
        self.menuColeta.add_command(label='Encerrar Coleta',command=self.finalizarColeta)
        self.menuColeta.entryconfig(2,state=DISABLED)
        menuBar.add_cascade(label="Coleta",menu=self.menuColeta)
        
        #Dados
        menuDados = Menu(menuBar)
        menuDados.add_command(label='Meus Dados',command=self.pgDados)
        menuDados.add_command(label='Recuperar Dados',command=self.pgRecuperarDados)
        
        menuBar.add_cascade(label='Dados',menu=menuDados)
        
        #Equipamentos
        menuEqp = Menu(menuBar)
        menuEqp.add_command(label='Configurar Equipamentos',command=self.pgEquipamentos)
        
        menuBar.add_cascade(label='Equipamentos',menu=menuEqp)
        
        #FTP
        menuFTP = Menu(menuBar)
        menuFTP.add_command(label='Enviar dados',command=self.pgFTP)
        
        menuBar.add_cascade(label='FTP',menu=menuFTP)
        
        #Terminal
        menuTerminal = Menu(menuBar)
        menuTerminal.add_command(label='Novo Terminal',command=self.terminal)
        
        menuBar.add_cascade(label='Terminal',menu=menuTerminal)
        
        #Fim menu
        
        #tabela
        self.tabela = Treeview(self.root,selectmode='none',columns=('column1','column2','column3','column4','column5'), show='headings')
        
        #configurando colunas
        self.tabela.column("column1", anchor=CENTER)    
        self.tabela.column("column2", anchor=CENTER)   
        self.tabela.column("column3", anchor=CENTER)
        self.tabela.column("column4", anchor=CENTER)
        self.tabela.column("column5", anchor=CENTER)  
        
        #configurando header
        self.tabela.heading("column1", text="Equipamento")    
        self.tabela.heading("column2", text="Valor")   
        self.tabela.heading("column3", text="Hora")   
        self.tabela.heading("column4", text="Flag")
        self.tabela.heading("column5", text="Status")  
        
        #Config barra de rolagem 
        self.sb = Scrollbar(self.root, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y) 
        
        self.tabela.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.tabela.yview)
        
        #Inserindo valores na tabela
        eqps = FIREBASE.child('equipamentos').order_by_child('estacao').equal_to('01').get()
        for eqps in eqps.each():
            self.tabela.insert('','end',values=(eqps.val()['TAG'],'','',''),iid=eqps.val()['TAG'])
        
        self.tabela.pack(side=LEFT)   

