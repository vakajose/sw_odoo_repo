#from odoo import http 
#from odoo.http import request
import xmlrpc.client

#Datos de conexion
url ='http://localhost:8085'
db = 'odoodb'
username = 'usuario_api'
#password = 'usuario_api'
password = 'b9512b38458fb94db8104d1c1d63fe2728c8b62b'
#class ColegioAPI(http.Controller):
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})
print(uid)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

result = models.execute_kw(db, uid, password, 'colegio.unidad.educativa', 'get_unidades_educativas', [[136]])
result2 = models.execute_kw(db, uid, password, 'colegio.unidad.educativa', 'read', [[3]], {'fields': ['nombre', 'tipo']})
print(result)
print(result2)