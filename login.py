import urllib 

import urllib2
import json

conditionsSetURL = "https://exp.botonmedico.com/accessDatabase/wp_DB/service/recibirDatos.php"
newConditions = {"username":"anto@gmail.com", "password":"sss"} 
params = json.dumps(newConditions).encode('utf8')
req = urllib2.Request(conditionsSetURL, data=params,headers={'content-type': 'application/json'})
response = urllib2.urlopen(req)
print (response.read())