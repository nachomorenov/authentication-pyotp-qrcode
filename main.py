from flask import Flask, render_template, request, flash, redirect, url_for
import pyotp
import base64
import qrcode
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'SECRETKEYEXAMPLE'


key = pyotp.random_base32()
totp = pyotp.TOTP(key)


def generate_qr_base64():
    uri = totp.provisioning_uri(name="John Doe", issuer_name="Bank Example")
    qr = qrcode.QRCode()
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

qr_base64 = generate_qr_base64()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_code = request.form.get("code")
        if totp.verify(user_code):
            flash("Código verificado con éxito.", "success")
        else:
            flash("Código incorrecto. Intenta nuevamente.", "danger")
        return redirect(url_for("index"))

    return render_template("index.html", qr_base64=qr_base64)

if __name__ == "__main__":
    app.run(debug=True)
