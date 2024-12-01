import pyotp
import qrcode
from flask import Flask, request, render_template_string


key = pyotp.random_base32()
print("Clave generada:", key)


#Generador de qr
uri = pyotp.totp.TOTP(key).provisioning_uri(name="John Doe", issuer_name= "Bank")
print(uri)
img= qrcode.make(uri)
img.save("totp.png")

print("Codigo QR generado y guardado como 'totp.png'. Escanea el qr con la aplicacion de autenticacion. ")

#Validacion de datos
totp = pyotp.TOTP(key)

while True:
    code = input("Ingrese el codigo (o 'x' para salir): ")
    if code.lower() == 'x':
        print("Cancelando...")
        break
    
    if totp.verify(code):
        print("Acceso Concedido.")
        break
    else:
        print("Codigo incorrecto. Intente de nuevo.")