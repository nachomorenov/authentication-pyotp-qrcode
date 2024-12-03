import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, flash
import io
import base64

app = Flask(__name__)
app.secret_key = "SECRETKEYEXAMPLE"

#Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key)
    
    qr_url = totp.provisioning_uri(name="John Doe", issuer_name="Bank Example")
    img = qrcode.make(qr_url)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    qr_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    if request.method == "POST":
        code = request.form["code"]
        
        if totp.verify(code):
            flash("Código correcto! Acceso concedido. Redirigiendo a la pagina principal...", "success")
        else:
            flash("Código incorrecto. Inténtalo de nuevo.", "failure")
        return redirect("/") 

    return render_template("index.html", qr_base64=qr_base64)


if __name__ == "__main__":
    app.run(debug=True)