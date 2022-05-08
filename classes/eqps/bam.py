import serial
import time
import numpy
import os 

class BAM:
    def __init__(self,porta,velocidade):
        self.porta = porta
        self.velocidade = velocidade

    def enviarComando(self,comando):
        #Entradas -> porta(int): numero da porta serial conectada / comando(str): comando a ser enviado para o bam
        
        print("Tentando acessar porta "+self.porta)
        ser = serial.Serial(self.porta,self.velocidade)
        for i in range(4):
            enter = '\r'.encode('utf-8')
            ser.write(enter)
            time.sleep(1)
        if ser.in_waiting > 0:
            print("Obteve uma resposta na porta "+self.porta)
            #Envia o comando desejado para o BAM 
            dados = comando.encode('utf-8')
            ser.write(dados)
            time.sleep(1)
            #Loop para verificar se ainda há dados sendo enviados pelo BAM
            oldBits = 0
            newBits = ser.in_waiting 

            while oldBits != newBits:
                time.sleep(1)
                oldBits = newBits
                newBits = ser.in_waiting
            
            quantDados = ser.in_waiting

            retorno = ''
            #Grava dados enviados pelo BAM em uma variavel
            while ser.in_waiting != 0:
                x = ser.read()
                x = x.decode('utf-8')
                retorno += x

            return retorno
        else:
            return False
   
    def enviarComandoCSV(self,comando):
        #Entradas -> porta(int): numero da porta serial conectada / comando(str): comando a ser enviado para o bam
        print("Tentando acessar porta "+self.porta)
        ser = serial.Serial(self.porta,self.velocidade)
        for i in range(4):
            enter = '\r'.encode('utf-8')
            ser.write(enter)
            time.sleep(1)
        if ser.in_waiting > 0:
            print("Obteve uma resposta na porta "+self.porta)
            #Envia o comando desejado para o BAM 
            menuCSV = "6".encode('utf-8')
            ser.write(menuCSV)
            time.sleep(1)
            
            #Limpar buffer
            ser.flushInput()
            
            enviar = comando.encode('utf-8')
            ser.write(enviar)
            time.sleep(1)
            
            #Loop para verificar se ainda há dados sendo enviados pelo BAM
            oldBits = 0
            newBits = ser.in_waiting 

            while oldBits != newBits:
                time.sleep(1)
                oldBits = newBits
                newBits = ser.in_waiting
            
            if ser.in_waiting > 0:
                limpaPrimeiraLinha = ser.readline()
                limpaSegundaLinha = ser.readline()

            #Grava dados enviados pelo BAM em uma variavel
            retorno = ''
            while ser.in_waiting != 0:
                x = ser.read()
                x = x.decode('utf-8')
                retorno += x
                
            return retorno
        else:
            return False
    
    def coletarDadosCSV(self):
        return self.enviarComandoCSV('3')

    def lastDataCSV(self):
        return self.enviarComandoCSV('4')
    
    def AllDataCSV(self):
        return self.enviarComandoCSV('2')

    def resetNewData(self,tempoReset):
        #porta(int) -> porta com conectada / tempoReset(str) -> tempo a ser resetado
        comando = "\u001B3 "+tempoReset+"\r"
        return self.enviarComando(comando)
    
    def migris(self,dados,destino):
        #Método depreciado 
        #parametros: dados(str) -> Resposta do bam / destino(str) -> local onde será armazenado os arquivos migris 
        #Salva retorno do BAM em um arquivo
        arquivo = open('respostaBam.txt','w')
        arquivo.writelines(dados)
        arquivo.close()
        
        #Lê o arquivo resposta do BAM e salva em formato Migris
        arquivo = open('respostaBam.txt','r')

        dados = arquivo.readlines()

        qntLinhas = numpy.size(dados)

        for i in range(qntLinhas):
            if "Report for" in dados[i]:
                StationID = dados[i][66:67]
                data = dados[i][13:23]
                data = data.split('/')
                dia = data[1]
                mes = data[0]
                ano = data[2]
            if dados[i][0].isdigit():
                hora = dados[i][0:5]
                conc = dados[i][19:25]
                if " " in conc:
                    conc = conc[1:6]
                
                flag = dados[i][6:18]
                
                if flag.count('-') == 12:
                    flag = "V"
                else:
                    flag = "I"
                
                dataFormatada = ano+'-'+mes+'-'+dia+'T'+hora+':00-03:00'
                
                migris = dataFormatada+';'+StationID+';'+flag+';'+conc
                print(migris)
                
                #Verifica se o diretorio existe, se não existir é criado 
                if os.path.isdir(destino+StationID):
                    arquivo = open(destino+StationID+"/"+dataFormatada+'.txt','w')
                    arquivo.writelines(migris)
                    arquivo.close()
                else:
                    os.mkdir(destino+StationID)
                    arquivo = open(destino+StationID+"/"+dataFormatada+'.txt','w')
                    arquivo.writelines(migris)
                    arquivo.close()	
                    
        os.unlink('respostaBam.txt')
