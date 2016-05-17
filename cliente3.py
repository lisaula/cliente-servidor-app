#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      cliente3.py
from __future__ import division
from socket import socket
import os
import math
import time
band_width = 1024
def recibir(tipo, nombre, s):
    if(tipo != 'mensaje'):
        while True:
            f = open(nombre, "wb")
            content = conn.recv(band_width)
            cont =1
            while content:
                # Enviar contenido.
                f.write(content)
                #print content
                content = conn.recv(band_width)
                cont +=1
            f.close()
            break
    else:
        comando=''

        while True:
           # print 'dentro While'
            try:
                # Recibir datos del cliente.
                input_data = s.recv(band_width)
                #print 'input data', input_data
            except:
                print("Error de lectura.")
                break
            else:

                if input_data:
                   # print ' 1 else'
                    if input_data == ' salir':
                        break
                    # Compatibilidad con Python 3.
                    if isinstance(input_data, bytes):
                        fvar = input_data.find("*")
                        if(fvar >0):
                            input_data = buffer(input_data,0,fvar)
                            end = True
                        elif(fvar==0):
                            end = True;
                        else:
                            end = False
                     #   print ' is isinstance', end
                    else:
                        end = input_data == chr(1)
                        #print 'else isinstance', end
                    input_data = str(input_data)
                    if not end:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                          #  print 'exit de ultimo'
                        elif(var ==0):
                            input_data=''
                          #  print'exit de primero'
                            break;
                        # Almacenar datos.
                        if(tipo != 'mensaje'):
                            f.write(input_data)
                        else:
                            comando+=input_data
                        #print 'if not end'
                    else:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                            salir = True
                       #     print 'exit de ultimo'
                        elif(var ==0):
                            input_data=''
                            salir=True
                       #     print'exit de primero'
                            break;
                        if(tipo != 'mensaje'):
                            f.write(input_data)
                        else:
                            comando += str(input_data)
                        #print 'end'
                        break;
                else:
                    break
                    #print 'no hay nada'
            
        print 'El archivo se ha recibido exitosamente'
        print comando
        return comando
def recibir3(nombre, size, conn):
    size = int(size)
    cant = float(size/band_width)
    cant = math.ceil(cant)
    while True:
        f = open(nombre, "wb")
        content = conn.recv(band_width)
        f.write(content)
        cant -=1
        bytes_recv=band_width
        #print 'uno'
        while cant>=0:
            # Enviar contenido.
            left = min(size - bytes_recv,band_width)
            if(left ==0):
                break;
            content = conn.recv(left)
            f.write(content)
            bytes_recv += len(content)
            cant -=1
            #print 'dos', cant
        f.close()
        break
    print 'Recibido correctamente'

def enviar(nombre, tipo, s):
    init =0;
    while True:
        if(tipo == 'mensaje'):
            while True:
                #f = open("archivo.jpg", "rb")
                while True:
                    message = raw_input('Mensaje a enviar: ')
                    if('put' in message): 
                        temp1 = message.split(' ')
                        temp =[]
                        temp.append(temp1[0])
                        dir_name=''
                        for i in range(len(temp1)-1):
                            i+=1
                            dir_name+=temp1[i]
                            if(i != (len(temp1)-1)):
                                dir_name+=' '
                        temp.append(dir_name)
                        if(len(temp)>1):
                            if(os.path.exists(temp[1])):
                                size=os.path.getsize(temp[1])
                                message+= ' '+str(size)
                                break
                            else:
                                print 'El archivo que estas intentando enviar NO EXISTE'
                        else:
                            print 'Error de comando'
                    else:
                        break
                message+="*"
                if(len(message)>band_width):
                    while True:
                        if(init >= len(message)):
                            break;    
                        if((len(message)-init)>=band_width):
                            content = buffer(message,init,band_width)
                            s.send(content)
                            #print content
                            init +=band_width
                        else:
                            content = buffer(message, init,len(message)-init)
                            s.send(content)
                            #print content
                            init += len(message)-init
                else:
                    s.send(message)
                    #print message
                break
        else:
            size = os.path.getsize(nombre)
            #print 'size ', size
            cant = float(size / band_width)
            dif = float(cant - int(cant))
            dif = math.ceil(dif*band_width)
            #print 'antes ',cant
            #print cant
            var =0
            while True:
                f = open(nombre, "rb")
                data = f.read(1024)
                var +=1;
                while data:
                    print var
                    # Enviar contenido.
                    s.send(data)
                    #time.sleep(0.5)
                    #print content
                    data = f.read(1024)
                    var +=1               
                f.close()
                print 'salio var ', var
                break
                #print 'contador ', cont
        # Se utiliza el caracter de código 1 para indicar
        # al cliente que ya se ha enviado todo el contenido.
        if(tipo =='archivo'):
            break
        try:
            print ""
            #if(tipo == 'mensaje'):
             #   var = "*"
              #  s.send(var)
                #print var
        except TypeError:
            # Compatibilidad con Python 3.
            s.send(bytes(chr(1), "utf-8"))
        finally:
            break;
    if(tipo == 'mensaje'):
        return message;

    print 'El archivo se ha mandado exitosamente'

def unirName(var):
    var = var.split(' ');
    temp = ''+var[0]+' '
    for i in range(len(var)-1):
        i+=1
        temp+=var[i]
        if(i!=(len(var)-1)):
            temp+='_'
    return temp  

def main():
    s = socket()
    s.connect(("localhost", 6052))
    
    while True:
        recibir('mensaje','',s)
        var = enviar('','mensaje',s)
        #if (var == 'salir'):
         #   continue;

        if('put' in var):
            time.sleep(2)
            var = var.split(' ')
            #print 'entro en put ',var[1]
            if(len(var)>3):
                temp = ''
                for i in range(len(var)-2):
                    i+=1
                    temp+=var[i]
                    if(i!=(len(var)-2)):
                        temp+=' '
                var[1]=temp

            if(len(var)>1):
                enviar(var[1],'archivo',s)
        elif('get' in var):
            var = var.split(' ')
            #print 'entro en get ', var[1]
            size = recibir('mensaje','',s)
            if(size != 'Archivo no existe'):
                if(len(var)>2):
                    recibir3(var[2]+'/'+var[1],size,s)
        elif var == 'salir*':
            s.close()
            return ''
        #recibir('mensaje','',s)

    # Cerrar conexión y archivo.
    #s.close()
    #f.close()
if __name__ == "__main__":
    main()


'''
RECORDATORIO:
    CAMBIO DE ENVIO DE * SUMADO AL Mensaje, CHEQUIAR SERVER PYTHON SI NO AFECTA
    QUITAR PRINTS DE DEBUGER
    
'''