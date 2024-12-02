import pyotp
import qrcode
from flask import Flask, render_template, request
import io
import base64

app = Flask(__name__)

#Generador TOTP y QR
key = pyotp.random_base32()
totp = pyotp.TOTP(key)
uri = totp.provisioning_uri(name="John Doe", issuer_name="Example Bank")

#Ruta principal
@app.route('/', methods=["GET", "POST"])
def index():
    message = None

    #Generador de QR y convertidor a base64
    qr_image = qrcode.make(uri)
    img_io = io.BytesIO()
    qr_image.save(img_io, "PNG")
    img_io.seek(0)
    qr_code_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")

    if request.method == "POST":
        #Maneja el envio del formulario
        if "cancel" in request.form:
            return redirect(url_for("cancel"))
    
        user_code = request.form.get("codigo")
        if totp.verify(user_code):
            return redirect(url_for("success"))
        else:
            message = "Codigo incorrecto. Intentelo de nuevo."
    
    return render_template("index.html", qr_code_base64=qr_code_base64, message=message)

@app.route("/success")
def success():
    return "<h1>Acceso Concedido.</h1>"

@app.route("/cancel")
def cancel():
    return "<h1>Operacion Cancelada.</h1>"

if __name__ == "__main__":
    app.run(debug=True)