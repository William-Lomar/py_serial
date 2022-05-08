#Para de funcionar em funções
from threading import Timer,Thread,Event
import time
from app import*


#Função para colocar funções em looping 
class SetInterval():
   def __init__(self,time,function):
      self.time=time
      self.function = function
      self.thread = Timer(self.time,self.handle_function)

   def handle_function(self):
      self.function()
      self.thread = Timer(self.time,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()



