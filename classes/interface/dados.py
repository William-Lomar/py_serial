from config import*

class Dados:
    def gerarJSON(self):
        filtro = self.valorEqp.get()
        if filtro == '':
            messagebox.showwarning("Erro",'Favor escolher 1 ou todos os equipamento')
        elif filtro == "Todos":
            json = requests.get('https://datalogger-bbbf4-default-rtdb.firebaseio.com/dados.json')
            json = json.content.decode()
            
            arquivo = open('dados.json','w')
            arquivo.writelines(json)
            arquivo.close()
            messagebox.showwarning("Sucesso",'Arquivo json criado com sucesso')
        else:
            json = requests.get('https://datalogger-bbbf4-default-rtdb.firebaseio.com/dados.json?orderBy=%22TAG%22&equalTo=%22'+filtro+'%22')
            json = json.content.decode()
            
            arquivo = open('dados.json','w')
            arquivo.writelines(json)
            arquivo.close()
            messagebox.showwarning("Sucesso",'Arquivo json criado com sucesso')
         
    def gerarExcel(self):
        filtro = self.valorEqp.get()
        
        if filtro == "Todos" or filtro == '':
            messagebox.showwarning("Erro",'Favor filtrar dados de 1 equipamento')
        else:
            workbook = Workbook("MeusDados.xlsx")
            planilha = workbook.add_worksheet(filtro)
            
            linhasTabela = self.tabela.get_children()
            
            planilha.write(0,0,"Data")
            planilha.write(0,1,"Valor")
            
            linha = 1
            for tabela in linhasTabela:
                tag = self.tabela.item(tabela)['values'][3]
                valor = self.tabela.item(tabela)['values'][1]
                data = self.tabela.item(tabela)['values'][0]
                if filtro != tag:
                    continue
                planilha.write(linha,0,data)
                planilha.write(linha,1,valor)
                linha += 1
            workbook.close()
            messagebox.showwarning("Sucesso",'Excel gerado com sucesso')
    
    def gerarGrafico(self):
        filtro = self.valorEqp.get()
        if filtro == "Todos" or filtro == '':
            messagebox.showwarning("Erro",'Favor filtrar dados de 1 equipamento')
        else:
            linhasTabela = self.tabela.get_children()
            x = []
            y = []
            data = []
            cont = 0
            for linhas in linhasTabela:
                tag = self.tabela.item(linhas)['values'][3]
                valor =  float(self.tabela.item(linhas)['values'][1]) 
                data += [self.tabela.item(linhas)['values'][0]]
                
                if filtro != tag:
                    continue
                x += [cont]
                y += [valor]
                cont+=1

            
            datas = [dt.datetime.strptime(d,'%m/%d/%y %H:%M') for d in data]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.plot(datas,y)
            plt.gcf().autofmt_xdate()
            plt.ylabel("Valor")
            plt.title("Dados do "+filtro)
            plt.show()
            
    def filtrarDados(self):
        filtro = self.valorEqp.get()
        
        if filtro == "Todos":
            #Limpa tabela
            linhasTabela = self.tabela.get_children()
            for linhas in linhasTabela:
                self.tabela.delete(linhas)
   
            #Inserindo valores na tabela
            eqps = FIREBASE.child("equipamentos").order_by_child("estacao").equal_to('01').get()
            
            for eqps in eqps.each():
                dados = FIREBASE.child("dados").order_by_child("TAG").equal_to(eqps.val()["TAG"]).get()
                for dados in dados.each():
                    data = dados.val()['data']
                    valor = dados.val()['valor']
                    flag = dados.val()['flag']
                    tag = dados.val()['TAG']
                    
                    self.tabela.insert('','end',values=(data,valor,flag,tag))
        else:
            linhasTabela = self.tabela.get_children()
            for linhas in linhasTabela:
                self.tabela.delete(linhas)
                
            dadosFiltro = FIREBASE.child('dados').order_by_child('TAG').equal_to(filtro).get()
            
            for dados in dadosFiltro.each():
                data = dados.val()['data']
                valor = dados.val()['valor']
                flag = dados.val()['flag']
                tag = dados.val()['TAG']
                
                self.tabela.insert('','end',values=(data,valor,flag,tag))
        
    def __init__(self,root):
        self.root = root
        self.root.title("Meus Dados") 
        
        #Ações
        c1 = Frame(self.root)
        c1.pack()
        
        labelEqp = Label(c1,text="Equipamento:")
        labelEqp.pack(side=LEFT, padx=5)
        
        equipamentos = FIREBASE.child('equipamentos').order_by_child("estacao").equal_to(ESTACAO).get()
        listaEqps = ['Todos']
        
        for eqp in equipamentos.each():
            listaEqps += [eqp.val()['TAG']]
        
        self.valorEqp = Combobox(c1,values = listaEqps)
        self.valorEqp.pack(side=LEFT, padx=5)
        
        filtrarEqp = Button(c1,text="Filtrar",command=self.filtrarDados)
        filtrarEqp.pack(side=RIGHT,padx=20,pady=20)
        
        grafico = Button(c1,text="Gráfico", command=self.gerarGrafico)
        grafico.pack(side=RIGHT,padx=20,pady=20)
        
        excel = Button(c1,text="Gerar Excel", command=self.gerarExcel)
        excel.pack(side=RIGHT,padx=20,pady=20)
        
        json = Button(c1,text="Gerar JSON", command=self.gerarJSON)
        json.pack(side=RIGHT,padx=20,pady=20)
        
        
        c2 = Frame(self.root)
        c2.pack()
        
        self.tabela = Treeview(c2,selectmode='browse',columns=('column1','column2','column3','column4'), show='headings')
        
        #configurando colunas
        self.tabela.column("column1", anchor=CENTER)    
        self.tabela.column("column2", anchor=CENTER)   
        self.tabela.column("column3", anchor=CENTER)   
        self.tabela.column("column4", anchor=CENTER)
        
        #configurando header
        self.tabela.heading("column1", text="Data")    
        self.tabela.heading("column2", text="Valor")   
        self.tabela.heading("column3", text="Flag")   
        self.tabela.heading("column4", text="TAG")   
        
        #Config barra de rolagem 
        self.sb = Scrollbar(c2, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y) 
        
        self.tabela.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.tabela.yview)
        
        #Inserindo valores na tabela
        eqps = FIREBASE.child("equipamentos").order_by_child("estacao").equal_to('01').get()
        
        for eqps in eqps.each():
            dados = FIREBASE.child("dados").order_by_child("TAG").equal_to(eqps.val()["TAG"]).get()
            for dados in dados.each():
                data = dados.val()['data']
                valor = dados.val()['valor']
                flag = dados.val()['flag']
                tag = dados.val()['TAG']
                
                self.tabela.insert('','end',values=(data,valor,flag,tag))
        
        self.tabela.pack()