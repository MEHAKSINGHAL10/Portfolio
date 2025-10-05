from flask import Flask, request, redirect, url_for, flash, render_template
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv  # <-- NEW

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Secret key from .env
app.secret_key = os.environ.get("SECRET_KEY", "fallback_dev_key")

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")


@app.route("/")
def index():
    return render_template("index.html")  # your portfolio file (put it in templates/)

@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    subject = f"New message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_USER, f"Subject: {subject}\n\n{body}")

        flash("Message sent successfully!", "success")
    except Exception as e:
        print(e)
        flash("Failed to send message. Try again later.", "error")

    return redirect("/")  # reload homepage

if __name__ == "__main__":
    app.run(debug=True)
