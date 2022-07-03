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
import csv

#Constantes y variables
filecsvdni2 = []
solicitardni = "2523"

#Funciones

#Ingreso a la base
def readcsv(solicitardni):

    file = open("chequera.csv", "r")
    csvcheques = csv.reader(file)
    for linea in csvcheques:
        if linea != []:
            data = {"NroCheque":linea[0], "CodigoBanco":linea[1], "CodigoScurusal":linea[2], "NumeroCuentaOrigen":linea[3], "NumeroCuentaDestino":linea[4], "Valor":linea[5], }
            filecsvdni2.append(data)
    file.close()

    for elem in filecsvdni2:
        for x,y in elem.items():
            if x == "CodigoBanco" and y == str(solicitardni):
                salida()                
            else:
                None
    print("No se encontraron datos")

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
            readcsv(solicitardni)
            # Ingresar la correcta funcion
        elif confirmar == "n":
            return solicituddni()
        else:
            None
    else:
        print("El valor ingresado no es el correcto.")
        confirmardni(solicitardni)


def salida():
    print("Salida")    

#Mostrar resultados por pantalla
def mostraspantalla():

    print("pantalla")

#Mostrar resultados por csv
def mostrarcsv():

    print("csv")

if __name__ =="__main__":
    ingresocliente()
    solicituddni()