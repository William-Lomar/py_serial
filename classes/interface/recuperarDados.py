from config import*
from classes.eqps.bam import*

class RecuperarDados:
    def recuperarAllDados(self):
        tag = self.selectEqps.get()
        eqp = FIREBASE.child('equipamentos').order_by_child('TAG').equal_to(tag).get()
        
        for eqp in eqp.each():
            serialPort = eqp.val()['serialPort']
        
        bam = BAM(serialPort,9600)
        dados = bam.AllDataCSV()
        
        if dados:
            arquivo = open('respostaBam.csv','w')
            arquivo.writelines(dados)
            arquivo.close()
            
            tabela = pandas.read_csv('respostaBam.csv',sep=',')
            
            qntLinhas = len(tabela)
            
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
                
            messagebox.showwarning("Sucesso",'Dados inseridos no banco com sucesso')
            self.root.destroy()
                
        else:
            messagebox.showwarning("Erro",'Falha ao comunicar com o equipamento')
            
    def recuperarFromData(self):
        data = self.selectData.get()
    
    def __init__(self,root):
        self.root = root
        self.root.title("Recuperar Dados")
        
        #Primeiro container
        c1 = Frame(self.root)
        c1.pack(padx=10,pady=10)
        
        titulo = Label(c1, text = "De qual equipamento deseja recuperar os dados?")
        titulo.pack()
        
        eqps = FIREBASE.child('equipamentos').order_by_child('estacao').equal_to(ESTACAO).get() 
        
        valuesEqp = []
        for eqps in eqps.each():
            valuesEqp += [eqps.val()['TAG']]
        
        self.selectEqps = Combobox(c1, values=valuesEqp, state = 'readonly')
        self.selectEqps.pack(pady = 20)
        
        #Segundo Container
        c2 = Frame(self.root)
        c2.pack(padx=10,pady=10)
        
        textData = Label(c2, text = "A partir de:")
        textData.pack(side = 'left', padx = 10)
        
        self.selectData = Entry(c2, width=25)
        self.selectData.insert(0,'Example: 12/12/2021 12:00')
        self.selectData.pack(side = 'left', padx = 10)
        
        buttonData = Button(c2, text = "Buscar Dados", command = self.recuperarFromData)
        buttonData.pack(side = 'left', padx = 10)
        
        #Terceiro container 
        c3 = Frame(self.root)
        c3.pack(padx=10,pady=10)
        
        buttonAllDados = Button(c3, text = "Recuperar todos os dados", command = self.recuperarAllDados)
        buttonAllDados.pack()
        
                
        