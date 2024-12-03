import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, url_for, flash
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "SECRETKEYEXAMPLE"

#Generador TOTP
key = pyotp.random_base32()
totp = pyotp.TOTP(key)

#Ruta principal
@app.route('/')
def index():
    uri = totp.provisioning_uri(name="John Doe", issuer_name="Example Bank")
    qr = qrcode.make(uri)
    qr_io = BytesIO()
    qr.save(qr_io, "PNG")
    qr_io.seek(0)
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode()
    return render_template("index.html", qr_code=qr_base64)

@app.route("/verify", methods=["POST"])
def verify():
    if "cancel" in request.form:
        return redirect(url_for("index"))
    
    code = request.form.get("code")
    if totp.verify(code):
        return "Acceso Concedido"
    else:
        flash("Codigo Incorrecto. Intente nuevamente.")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)