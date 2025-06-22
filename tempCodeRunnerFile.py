from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib, ssl
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change_this_to_a_secure_key')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill all fields', 'error')
        return redirect(url_for('home'))

    # Email sending setup (use environment variables or config in production)
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get('SENDER_EMAIL')       # Your Gmail address
    password = os.environ.get('EMAIL_PASSWORD')          # Gmail app password

    receiver_email = sender_email
    email_message = f"""\
Subject: Portfolio Contact Form Message

From: {name} <{email}>

{message}
"""

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_message)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        print(f"Email error: {e}")
        flash('Failed to send message. Try again later.', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
