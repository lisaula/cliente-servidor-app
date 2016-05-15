#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      servidor3.py
#
from __future__ import division
from socket import socket, error
import os
import sys
from manager import manager
import math
import time

band_width = 1024
def unirName(var):
    var = var.split(' ');
    temp = ''+var[0]+' '
    for i in range(len(var)-1):
        i+=1
        temp+=var[i]
        if(i!=(len(var)-1)):
            temp+='_'
    return temp
class cmd:
    path =''
    usuario = ''
    def __init__(self, path=None):
        if self.path is '':
            self.path = 'servidor'
        else:
            self.path = path
        if not (os.path.isdir(self.path)):
            os.mkdir(self.path)

        print self.path
    def __call__(self, path=None):
        if self.path is '':
            self.path = 'servidor'
        else:
            self.path = path
        if not (os.path.isdir(self.path)):
            os.mkdir(self.path)
        print self.path
    def setUsuario(self, u):
        self.usuario = u
    def terminal(self, comando, conn):
        comando = comando.split(' ')
        if(len(comando)>0):
            if(comando[0]=='cd' and len(comando)>1):
                if(os.path.exists(self.path+comando[1])):
                    self.path += comando[1]
                else:
                    if(comando[1]=='..'):
                        parse = self.path.split('/')
                        if(parse[len(parse)-1]!=self.usuario):
                            self.path=''+parse[0]
                            for i in range(len(parse)-2):
                                i +=1
                                if(parse[i]!= ''):
                                    self.path+='/'+parse[i]
                        else:
                            return 'Carpeta raiz, no puedes volver mas atras'
                    else:       
                        return 'Directorio no existe'+ self.path+comando[1]
            elif(comando[0]== 'ls'):
                if(os.path.isdir(self.path)):
                    ficheros = os.listdir(self.path)
                    res = ''
                    if(len (ficheros)==0):
                        res = 'Directorio vacio'
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
                else:
                    return 'Directorio ya creado'
            elif(comando[0]== 'rm' and len(comando)>1):
                if(os.path.isdir(self.path+'/'+comando[1])):
                    return 'Comando Invalido.\nEstas intentando borrar un directorio'
                elif os.path.isfile(self.path+'/'+comando[1]):
                    enviar('Esta seguro que desea borrarlo? Y/N','mensaje', conn)
                    res = recibir('mensaje','',conn)
                    if(res.find('Y')>=0):
                        os.remove(self.path+'/'+comando[1])
                        return 'Archivo borrado exitosamente'
                    return 'Archivo no borrado'
                else:
                    return 'No se encontro el archivo'
            elif(comando[0]== 'put' and len(comando)>2):
                if(len(comando)>3):
                    temp = ''
                    for i in range(len(comando)-2):
                        i+=1
                        temp+=comando[i]
                        if(i!=(len(comando)-2)):
                            temp+='_'
                    comando[1]=temp
                    comando[2]=comando[len(comando)-1]
                return recibir3(self.path+'/'+os.path.basename(comando[1]), comando[2],conn)
                #return recibir('archivo', self.path+'/'+os.path.basename(comando[1]), conn)
            elif(comando[0]== 'get' and len(comando)>1):
                if(os.path.exists(self.path+'/'+comando[1])):
                    size = os.path.getsize(self.path+'/'+comando[1])
                    size = str(size)
                    print 'size ',size
                    enviar(size,'mensaje',conn)
                    time.sleep(2)
                    enviar(self.path+'/'+comando[1],'archivo',conn)
                    return 'Archivo enviado exitosamente'
                else:
                    return 'Archivo no existe'
            elif(comando[0]=='salir'):
                self.path = 'servidor'
                return 'salio'
            else:
                return 'Comando invalido'
        else:
            return 'No ha ingresado nada'
        return self.path
def recibir2(nombre, conn):
    f = open(nombre, "wb")
    while True:
        try:
            # Recibir datos del cliente.
            input_data = conn.recv(band_width)
        except error:
                print("Error de lectura.")
                break
        else:
            if input_data:
                num =input_data.find(' end')
                if(' end' in input_data):
                    input_data = buffer(input_data,0,num)
                    salir = True
                else:
                    if(num>=0):
                        if(len(input_data)==num):
                            input_data = buffer(input_data,0,num)
                            salir = True
                
                if(salir):
                    break;
            f.write(input_data)
        finally:
            print 'Salio'
    f.close()
    return 'Recibido correctamente';
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
    return 'Recibido correctamente'

def recibir(tipo, nombre, conn):
    
    salir = False
    comando =''
    f = None
    if tipo != 'mensaje':
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
        while True:
            #print 'dentro While'
            try:
                # Recibir datos del cliente.
                input_data = conn.recv(band_width)
                #print 'input data', input_data
            except error:
                print("Error de lectura.")
                break
            else:
                if input_data:
                    #print ' 1 else'
                    # Compatibilidad con Python 3.
                    if isinstance(input_data, bytes):
                        fvar = input_data.find(chr(1))
                        if(fvar >0):
                            input_data = buffer(input_data,0,fvar)
                            end = True
                        elif(fvar==0):
                            input_data=''
                            end = True;
                        else:
                            end = False
                        #end = input_data.find('final')
                        #print ' is isinstance', end
                    else:
                        end = input_data == chr(1)
                        #print 'else isinstance', end

                    input_data = str(input_data)
                    if not end:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                            salir = True
                        elif(var ==0):
                            end=True
                            salir = True
                            continue
                        # Almacenar datos.
                        if tipo != 'mensaje':
                            f.write(input_data)
                        else:
                            comando+=input_data
                        #print 'if not end',input_data
                    else:
                        var = input_data.find('salir')
                        if(var >0):
                            input_data = buffer(input_data,0,var)
                            end = True
                            salir = True
                        elif(var ==0):
                            end=True
                            salir =True
                        #f.write(input_data)
                        if tipo != 'mensaje':
                            f.write(input_data)
                        else:
                            comando += str(input_data)
                            if(salir):
                                comando+='salir'
                        #print 'end', comando
                        break;
                else:
                    #print 'comandoooo ',comando 
                    break
                    #print 'no hay nada'
            finally :
                print ''
    #if tipo != 'mensaje':
    #    f.close()
    print("El archivo se ha recibido correctamente.")

    #print 'comando ',comando
    if tipo != 'mensaje':
        return 'El archivo se ha recibido correctamente.'
    else:
        return comando

def enviar(respuesta, tipo, conn):
    init =0;
    while True:
        if(tipo =='mensaje'):
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
        else:
            while True:
                f = open(respuesta, "rb")
                content = f.read(1024)
                
                while content:
                    # Enviar contenido.
                    conn.send(content)
                    content = f.read(1024)
                f.close()
                break
        # Se utiliza el caracter de código 1 para indicar
        # al cliente que ya se ha enviado todo el contenido.
        try:
            if(tipo == 'mensaje'):
                var = chr(1)
                conn.send(var)
                #print var
        except TypeError:
            # Compatibilidad con Python 3.
            conn.send(bytes(chr(1), "utf-8"))
        finally:
            break;
    print 'El archivo se ha enviado exitosamente' 

def main():
    m = manager()
    m.load()
    s=socket()
    s.bind(("localhost", 6052))
    s.listen(5)
    conn, addr = s.accept() 
    print >>sys.stderr, 'concexion desde', addr
    mycmd = cmd()
    log = False;
    usuario= ''
    while True:
        if not log:
            enviar('Envia tu \'username\'<espacio>\'password\' para logearte, o envia \'registrar\'','mensaje',conn)
        while(log ==False):
            recibido= recibir('mensaje','',conn)
            #print 'al entrar log ',recibido
            if(recibido.find('registrar')>=0):
                enviar('Envia tu username<espacio>contrasenia para registrarte','mensaje',conn)
                while(True):
                    res = recibir('mensaje','',conn)
                    res = res.split(' ')
                    #print 'res ', res
                    if(len(res)>1):
                        if(m.registrar(res[0], res[1])):
                            enviar('Registrado correctamente','mensaje',conn)
                            usuario = res[0]
                            #print 'usuario ', usuario
                            #m.imprimir()
                            mycmd.terminal('mkdir '+usuario, conn)
                            mycmd.terminal('cd /'+usuario, conn)
                            mycmd.setUsuario(usuario)
                            log = True
                            break
                        else:
                            enviar('Error al registar usuario','mensaje',conn)
                    else:
                        enviar('Formato invalido','mensaje',conn)
            else:
                recibido = recibido.split(' ')
                #print 'recibio ',recibido
                if(len(recibido)>1):
                    #m.imprimir()
                    if(m.log(recibido[0],recibido[1])):
                        log = True
                        usuario = recibido[0]
                        mycmd.terminal('mkdir '+usuario, conn)
                        mycmd.terminal('cd /'+usuario, conn)
                        mycmd.setUsuario(usuario)
                        enviar('Estas logeado','mensaje',conn)
                        break
                    else:
                        enviar('Contrasenia o Username invalido\nEnvia tu \'username\'<espacio>\'password\' para logearte, o envia \'registrar\'','mensaje',conn)

                else:
                    enviar('Contrasenia o Username invalido\nEnvia tu \'username\'<espacio>\'password\' para logearte, o envia \'registrar\'','mensaje',conn)
        recibido = recibir('mensaje','',conn)
        #print 'rec',recibido;
        respuesta = mycmd.terminal(recibido, conn)

        if(recibido=='salir'):
            m.unlog(usuario)
            #m.imprimir()
            usuario =''
            log = False
            m.down()
            #print respuesta
            #print recibido
            continue
            #break
        enviar(respuesta,'mensaje',conn)
        
    conn.close()
    m.down()

if __name__ == "__main__":
    main()