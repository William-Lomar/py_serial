#Bibliotecas 
from numpy import require
import pyrebase
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from ttkthemes import*
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from xlsxwriter import*
import requests
import datetime as dt

import pandas
import sys
import os

#config Estação
ESTACAO = "01"

#config firebase
firebaseConfig = {
  'Configurações do firebase'
}

FIREBASE = pyrebase.initialize_app(firebaseConfig).database()