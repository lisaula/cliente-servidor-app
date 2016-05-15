from manager import manager
class main:
	m = manager()
	m.imprimir()
	m.registrar('luis', '1234')
	print m.log('luis', '1234')
	m.imprimir()
	m.unlog('luis')
	m.imprimir()
	print ' down'
	m.down()
	print 'p'
	p = manager()
	p.imprimir()