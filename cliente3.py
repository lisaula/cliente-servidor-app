#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      cliente3.py

from socket import socket
band_width = 1024
def main():
    s = socket()
    s.connect(("localhost", 6035))
    init =0;
    while True:
        while True:
            while True:
                #f = open("archivo.jpg", "rb")
                message = raw_input('Mensaje a enviar: ')
                if(len(message)>band_width):
                    while True:
                        if(init >= len(message)):
                            break;    
                        if((len(message)-init)>=band_width):
                            content = buffer(message,init,band_width)
                            s.send(content)
                            print content
                            init +=band_width
                        else:
                            content = buffer(message, init,len(message)-init)
                            s.send(content)
                            print content
                            init += len(message)-init
                else:
                    s.send(message)
                    print message
                break
            # Se utiliza el caracter de código 1 para indicar
            # al cliente que ya se ha enviado todo el contenido.
            try:
                var = '*'
                s.send(var)
                print var
            except TypeError:
                # Compatibilidad con Python 3.
                s.send(bytes(chr(1), "utf-8"))
            finally:
                break;
        if message == 'salir':
            break;

        print 'El archivo se ha mandado exitosamente'

        f = open("recibidoclient.txt", "wb")
        comando=''

        while True:
            print 'dentro While'
            try:
                # Recibir datos del cliente.
                input_data = s.recv(band_width)
                print 'input data', input_data
            except error:
                print("Error de lectura.")
                break
            else:

                if input_data:
                    print ' 1 else'
                    if input_data == ' salir':
                        break
                    # Compatibilidad con Python 3.
                    if isinstance(input_data, bytes):
                        fvar = input_data.find('*')
                        if(fvar >0):
                            input_data = buffer(input_data,0,fvar)
                            end = True
                        elif(fvar==0):
                            end = True;
                        else:
                            end = False
                        print ' is isinstance', end
                    else:
                        end = input_data == chr(1)
                        print 'else isinstance', end
                    input_data = str(input_data)
                    if not end:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                            print 'exit de ultimo'
                        elif(var ==0):
                            input_data=''
                            print'exit de primero'
                            break;
                        # Almacenar datos.
                        #f.write(input_data)
                        comando+=input_data
                        print 'if not end'
                    else:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                            salir = True
                            print 'exit de ultimo'
                        elif(var ==0):
                            input_data=''
                            salir=True
                            print'exit de primero'
                            break;
                        #f.write(input_data)
                        comando += str(input_data)
                        print 'end'
                        break;
                else:
                    break
                    #print 'no hay nada'
            finally :
                print 'termino' 
        print 'El archivo se ha recibido exitosamente'
        print comando
        
    # Cerrar conexión y archivo.
    s.close()
    #f.close()
if __name__ == "__main__":
    main()