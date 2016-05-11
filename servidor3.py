#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      servidor3.py
#
from socket import socket, error
import os
band_width = 1024
class cmd:
    path =''
    def __init__(self, path=None):
        if self.path is '':
            self.path = '/home/luis/Documentos/Python/cliente-servidor'
        else:
            self.path = path
        print self.path
    def __call__(self, path=None):
        if self.path is '':
            self.path = '/home/luis/Documentos/Python/cliente-servidor'
        else:
            self.path = path
        print self.path
        
    def terminal(self, comando):
        comando = comando.split(' ')
        if(len(comando)>=0):
            if(comando[0]=='cd' and len(comando)>=1):
                if(os.path.exists(self.path+comando[1])):
                    self.path += comando[1]
                else:
                    if(comando[1]=='..'):
                        parse = self.path.split('/')
                        self.path=''
                        for i in range(len(parse)-1):
                            if(parse[i]!= ''):
                                self.path+='/'+parse[i]
                    else:       
                        return 'Directorio no existe'+ self.path+comando[1]
            elif(comando[0]== 'ls'):
                if(os.path.isdir(self.path)):
                    ficheros = os.listdir(self.path)
                    res = ''
                    for i in range(len (ficheros)):
                        if(os.path.isdir(self.path+'/'+ficheros[i])):
                            res+='->'+ficheros[i]+'\n';
                        else:
                            res +='-'+ficheros[i]+'\n'
                    return res
                else:
                    return 'Estas tratando de listar un archivo'
            elif(comando[0]=='pwd'):
                return self.path
            elif (comando[0] == 'mkdir' and len(comando) >1):
                if not os.path.isdir(self.path+'/'+comando[1]):
                    os.mkdir(self.path+'/'+comando[1])
                    return 'Directorio '+comando[1]+' creado exitosamente'
            elif(comando[0]== 'rm' and len(comando)>1):
                if(os.path.isdir(self.path+'/'+comando[1])):
                    return 'Comando Invalido.\nEstas intentando borrar un directorio'
                elif os.path.isfile(self.path+'/'+comando[1]):
                    os.remove(self.path+'/'+comando[1])
                    return 'Archivo borrado exitosamente'
                else:
                    return 'No se encontro el archivo'
            elif(comando[0]== 'put' and len(comando)>1):
                return 'put'
            elif(comando[0]=='exit'):
                return 'salio'
            else:
                return 'Comando invalido'
        else:
            return 'No ha ingresado nada'
        return self.path

def main():
    s = socket()
    
    # Escuchar peticiones en el puerto 6030.
    s.bind(("localhost", 6035))
    s.listen(5)
    
    conn, addr = s.accept()
    f = open("recibidoserver.txt", "wb")
    mycmd = cmd()
    while True:
        salir = False
        comando =''
        while True:
            print 'dentro While'
            try:
                # Recibir datos del cliente.
                input_data = conn.recv(band_width)
                print 'input data', input_data
            except error:
                print("Error de lectura.")
                break
            else:
                if input_data:
                    print ' 1 else'
                    # Compatibilidad con Python 3.
                    if isinstance(input_data, bytes):
                        fvar = input_data.find('*')
                        if(fvar >0):
                            input_data = buffer(input_data,0,fvar)
                            end = True
                        elif(fvar==0):
                            input_data=''
                            end = True;
                        else:
                            end = False
                        #end = input_data.find('final')
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
                            salir=True
                        elif(var ==0):
                            salir =True
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
                        elif(var ==0):
                            break;
                        #f.write(input_data)
                        comando += str(input_data)
                        print 'end', comando
                        break;
                else:
                    
                    break
                    #print 'no hay nada'
            finally :
                print 'termino'

        f.close()
        print("El archivo se ha recibido correctamente.")

        print 'comando ',comando

        respuesta = mycmd.terminal(comando)
        if(salir):
            break
        init =0;
        while True:
            while True:
                #f = open("archivo.jpg", "rb")
                #message = raw_input('Mensaje a enviar: ')
                message = respuesta
                if(len(message)>band_width):
                    while True:
                        if(init >= len(message)):
                            break;    
                        if((len(message)-init)>=band_width):
                            content = buffer(message,init,band_width)
                            conn.send(content)
                            print content
                            init +=band_width
                        else:
                            content = buffer(message, init,len(message)-init)
                            conn.send(content)
                            print content
                            init += len(message)-init
                else:
                    conn.send(message)
                    print message
                break
            # Se utiliza el caracter de código 1 para indicar
            # al cliente que ya se ha enviado todo el contenido.
            try:
                var = '*'
                conn.send(var)
                print var
            except TypeError:
                # Compatibilidad con Python 3.
                conn.send(bytes(chr(1), "utf-8"))
            finally:
                break;
        if message == 'salir':
            break;
        print 'El archivo se ha enviado exitosamente' 
    #try:
     #   var = ' final'
      #  s.send(var)
       # print var
    #except TypeError:
     #   # Compatibilidad con Python 3.
      #  s.send(bytes(chr(1), "utf-8"))

    
    
    
    #if(comando == 'exit'):
    conn.close()
    

if __name__ == "__main__":
    main()