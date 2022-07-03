""" Ingresar el nombre del archivo csv
Ingresar el DNI del cliente
Elegir la salida del "reporte" (pantalla o csv)
Filtros:
	Elegir el tipo de cheque (emitido o depositado)
	Elegir el estado del cheque (Pendiente, Aprobado, Rechazado) (Opcional)
	Elegir un rango de fecha xx-xx-xxxx:yy-yy-yyyy (Opcional)
Si en un reporte, se repite un número de cheque, informar el error en pantalla
Si la salida es pantalla se imprime todo en pantalla
Si la salida es csv se exporta un archivo que:
	Nombre = <DNI><TIMESTAMPS ACTUAL>.csv
	Se exporta fechaorigen, fechapago, valor y cuenta(contraria al DNI).
Si no se recibe el estado del cheque imprimir sin filtro de estado """

#Libreria
from ast import Break
import csv
from multiprocessing.reduction import duplicate
from os import dup

#Constantes y variables
filecsvdni2 = []
solicitardni = "2523"
identificarchequesrepetidos = []
chequesporpantalla = []

#Funciones

#Ingreso a la base
def readcsv():

    file = open("chequera.csv", "r")
    csvcheques = csv.reader(file)
    for linea in csvcheques:
        if linea != []:
            data = {"NroCheque":linea[0], "CodigoBanco":linea[1], "CodigoScurusal":linea[2], "NumeroCuentaOrigen":linea[3], "NumeroCuentaDestino":linea[4], "Valor":linea[5], "FechaOrigen":linea[6], "FechaPago":linea[7], "DNI":linea[8], "Estado":linea[9], "TIPO":linea[10]}
            filecsvdni2.append(data)
    file.close()

#Bienvenida
def ingresocliente():
    print("Bienvenido estimado/a. A continuación le solicitaremos el DNI para poder realizar su consulta.")

#Solicitar DNI
def solicituddni():
    while True:
        try:
            solicitardni = int(input("Ingrese el DNI: "))
            print("El DNI ingresado es el siguiente: " + str(solicitardni))
            confirmardni(solicitardni)
            print("Fin.")
            break
            
        except ValueError:
            print("Ingrese el DNI correctamente")
            solicituddni()
        False
        break

#Confirmar DNI ingresado
def confirmardni(solicitardni):
    confirmar = input("Quiere continuar (s/n): ")
    if confirmar == "s" or confirmar == "n":
        if confirmar == "s":
            identificarcliente(solicitardni)
            # Ingresar la correcta funcion
        elif confirmar == "n":
            return solicituddni()
        else:
            None
    else:
        print("El valor ingresado no es el correcto.")
        confirmardni(solicitardni)

#Buscar datos del dni ingresado e identificar cheques repetidos
def identificarcliente(solicitardni):
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"]:
                y = elem["NroCheque"]
                identificarchequesrepetidos.append(y)
                for i in range(len(identificarchequesrepetidos)):
                    for j in range(len(identificarchequesrepetidos)):
                        if i != j:
                            if identificarchequesrepetidos[i] == identificarchequesrepetidos[j] and identificarchequesrepetidos[i] not in chequesporpantalla:
                                chequesporpantalla.append(identificarchequesrepetidos[i])
                                if len(chequesporpantalla) > 0:
                                    print("Se ha encontrado dos cheques con la misma numeración...")
                                    print("Los siguientes cheques se encuentran repetidos: ")
                                    for x in chequesporpantalla: 
                                       print(x)
                                    exit()
                                else:
                                    None
                            else:
                                None
                        else:
                            None
            else:           
                None
        continuar(solicitardni)

# En caso de no encontrar cheques repetidos se continua con el proceso
def continuar(solicitardni):
    for elem in filecsvdni2:
        if str(solicitardni) == elem["DNI"]:
            y = elem["NroCheque"]
            identificarchequesrepetidos.append(y)
            for i in range(len(identificarchequesrepetidos)):
                for j in range(len(identificarchequesrepetidos)):
                    if i != j:
                        if identificarchequesrepetidos[i] == identificarchequesrepetidos[j] and identificarchequesrepetidos[i] not in chequesporpantalla:
                            chequesporpantalla.append(identificarchequesrepetidos[i])
                            if len(chequesporpantalla) > 0:
                                salida(solicitardni)
                                exit()
                            else:  
                                None
                        else:
                            None
                    else:
                        None
        else:
            None  

#Recopilar información del cliente
def salida(solicitardni):
    consultasalida = input("Ingrese la opción por la cual quiere recibir la información \n 1. Pantalla \n 2. CSV \n ")
    if consultasalida == "1":
        mostrarpantalla(solicitardni)
    elif consultasalida == "2":
        mostrarcsv(solicitardni)
    else:
        print("Ingrese la opción correcta (1/2)")
        salida()

#Mostrar resultados por pantalla
def mostrarpantalla(solicitardni):
    tipocheque = input("Ingrese la opción por la cual quiere recibir la información con respecto a los cheques \n 1. Emitido \n 2. Depositado \n ")
    if tipocheque == "1":
        print("    *******************************    ")
        print("Los datos de los cheques son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

    
    elif tipocheque == "2":
        print("    *******************************    ")
        print("Los datos de los cheques son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")
    else:
        print("Ingrese la opción que requiera")
        mostrarpantalla(solicitardni)

#Mostrar resultados por csv
def mostrarcsv(solicitardni):
    tipocheque = input("Ingrese la opción por la cual quiere recibir la información \n 1. Emitido \n 2. Depositado \n ")
    print(solicitardni)
    print("csv")


def mostrarpendiente(solicitardni):
    
    for elem in filecsvdni2:
        for x,y in elem.items():
            if x == "DNI" and y == str(solicitardni):
                print(solicitardni)
                print(elem)                
            else:
                None 
    print("pendiente")

def mostraraprobado(solicitardni):
    print("aprobado")

def mostrarrechazado(solicitardni):
    print("rechazado")

def mostrartodos(solicitardni):
    print("todos")

def rangofechas():
    print("Determinar Rango de Fechas")


if __name__ =="__main__":
    readcsv()
    ingresocliente()
    solicituddni()