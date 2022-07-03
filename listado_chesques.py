#Libreria
from ast import Break
import csv
from multiprocessing.reduction import duplicate
from os import dup
from sqlite3 import Timestamp
from datetime import date, datetime

#Constantes y variables
filecsvdni2 = []
solicitardni = ""
identificarchequesrepetidos = []
chequesporpantalla = []

#Funciones

#Ingreso a la base
def readcsv(archivoabrir):
    if archivoabrir == "chequera":
        file = open("chequera.csv", "r")
        csvcheques = csv.reader(file)
        for linea in csvcheques:
            if linea != []:
                data = {"NroCheque":linea[0], "CodigoBanco":linea[1], "CodigoScurusal":linea[2], "NumeroCuentaOrigen":linea[3], "NumeroCuentaDestino":linea[4], "Valor":linea[5], "FechaOrigen":linea[6], "FechaPago":linea[7], "DNI":linea[8], "Estado":linea[9], "TIPO":linea[10]}
                filecsvdni2.append(data)
        file.close()
        print("A continuación le solicitaremos el DNI para poder realizar su consulta.")
    elif archivoabrir != "chequera":
        print("El archivo no se encuentra")
        selectoption = input("1. Intenta nuevamente... \n2. Salir \n")
        if selectoption == "1":
            elegirarchivo()
        else:
            finalsaludo()
            exit()


#Bienvenida
def ingresocliente():
    print("Bienvenido estimado/a.")

def elegirarchivo():
    archivoabrir = input("Ingrese el nombre del archivo al cual quiere ingresar... \n")
    readcsv(archivoabrir)

#Solicitar DNI
def solicituddni():
    while True:
        try:
            solicitardni = int(input("Ingrese el DNI: "))
            print("El DNI ingresado es el siguiente: " + str(solicitardni))
            confirmardni(solicitardni)
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
                                    finalsaludo()
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
        print("No se encontraron datos relacionados al DNI ingresado.")
        finalsaludo()
        exit()

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
                                finalsaludo()
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
        estado = input("Ingrese la opción con respecto al estado de los cheques que requiera:\n 1.Cheques Pendientes\n 2.Cheques Rechazados\n 3.Cheques Aprobados\n")
        if estado == "1":
            mostrarpendienteemitido(solicitardni)
        elif estado == "2":
            mostrarrechazadoemitido(solicitardni)
        elif estado == "3":
            mostraraprobadoemitido(solicitardni)
        else:
            print("    *******************************    ")
            print("Los datos de todos los cheques emitidos son los siguienes: ")
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
        estado = input("Ingrese la opción con respecto al estado de los cheques que requiera:\n 1.Cheques Pendientes\n 2.Cheques Rechazados\n 3.Cheques Aprobados\n")
        if estado == "1":
            mostrarpendientedepositado(solicitardni)
        elif estado == "2":
            mostrarrechazadodepositado(solicitardni)
        elif estado == "3":
            mostraraprobadodepositado(solicitardni)
        else:
            print("    *******************************    ")
            print("Los datos de todos los cheques depositados son los siguienes: ")
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
    estado = input("Ingrese la opción con respecto al estado de los cheques que requiera:\n1.Cheques Pendientes\2.Cheques Rechazados\3.Cheques Aprobados\n")
    if tipocheque == "1":
        if estado == "1":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Pendiente":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        elif estado == "2":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Rechazado":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        elif estado == "3":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Aprobado":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        else:
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
    elif tipocheque == "2":
        if estado == "1":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Pendiente":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        elif estado == "2":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Rechazado":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        elif estado == "3":
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Aprobado":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
        else:
            dt = datetime.now()
            tiempo = datetime.timestamp(dt)
            f = open(str(solicitardni) + "_" + str(tiempo) + ".csv", "a")
            csvcliente = csv.writer(f)
            for elem in filecsvdni2:
                if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado":
                    csvcliente.writerow([elem["NumeroCuentaDestino"],elem["Valor"],elem["FechaOrigen"],elem["FechaPago"]])
                else:
                    None 
            f.close()
    else:
        print("Ingrese la opción que requiera")
        mostrarcsv(solicitardni)
    print("Hemos generado un archivo con los datos solicitados")


def mostrarpendienteemitido(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques pendientes emitidos son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Pendiente":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def mostraraprobadoemitido(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques aprobados emitidos son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Aprobado":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def mostrarrechazadoemitido(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques rechazados emitidos son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Emitido" and elem["Estado"] == "Rechazado":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def mostrarpendientedepositado(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques depositados pendientes son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Pendiente":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def mostraraprobadodepositado(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques depositados aprobados son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Aprobado":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def mostrarrechazadodepositado(solicitardni):
        print("    *******************************    ")
        print("Los datos de los cheques depositados rechazados son los siguienes: ")
        i = 0
        for elem in filecsvdni2:
            if str(solicitardni) == elem["DNI"] and elem["TIPO"] == "Depositado" and elem["Estado"] == "Rechazado":
                i += 1
                print("------------Cheque N°" + str(i) + "--------------")
                int(i)
                for x, y in elem.items():
                    print(x + ": " + y)
            else:
                None 
        print("    *******************************    ")

def rangofechas():
    print("Determinar Rango de Fechas")

def finalsaludo():
    print("Muchas gracias por su tiempo!\nQue tenga un buen dia!")

if __name__ =="__main__":
    ingresocliente()
    elegirarchivo()
    solicituddni()
    finalsaludo()