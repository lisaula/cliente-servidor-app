from user import user
import os
class manager:
	users=[]
	path = None;

	def __init__(self):
		self.path = '/servidor'

		self.users.append(user('admin', '1234'))

	def registrar(self, u, p):
		if(len(u)>20 or len(p)>20):
			return False
		if(len(self.users)==0):
			u = user(u, p)
			self.users.append(u)
		else:
			print self.buscar(u)
			if self.buscar(u) == None :
				self.users.append(user(u,p))	
		return True

	def imprimir(self):
		for i in range(len(self.users)):
			print self.users[i].username
			print self.users[i].password
			print self.users[i].activo
		print 'termino', len(self.users)

	def buscar(self,user):
		for i in range(len(self.users)):
			if self.users[i].username == user:
				return self.users[i]
		return None

	def log(self, user, p):
		var=self.buscar(user) 
		#print 'None en log', var
		if(var!= None):
			#print 'pass no es', p
			if(var.password == p):
				var.activar(True)
				return True
		return False
	def isActive(self, u):
		var = self.buscar(u)
		if( var != None):
			if(var.activo):
				return True
		return False
	def unlog(self, user):
		print 'unlog'
		var=self.buscar(user) 
		var.activar(False)

	def load(self):
		if(os.path.isfile("usuarios")):
			f = open("usuarios","rb")
			self.users=[]
			while(True):
				u = f.read(20)
				p = f.read(20)
				while u:
					u = self.shor(u)
					p = self.shor(p)
					self.users.append(user(u, p))
					u = f.read(20)
					p = f.read(20)	

				break
			f.close()

	def shor(self, var):
		temp = ''
		for i in range(len(var)):
			#print var[i]
			if(var[i] != ' '):
				temp +=var[i]
		#print temp
		return temp
	def down(self):
		f = open("usuarios","wb")
		for i in range(len(self.users)):
			if(len(self.users[i].username)<20):
				for x in range (20 - len(self.users[i].username)):
					self.users[i].username+=' '
			if(len(self.users[i].password)<20):
				for x in range (20 - len(self.users[i].password)):
					self.users[i].password+=' '

			f.write(self.users[i].username)
			f.write(self.users[i].password)
			self.users[i].username = self.shor(self.users[i].username)
			self.users[i].password = self.shor(self.users[i].password)
			print 'guardo ', i
		f.close()




