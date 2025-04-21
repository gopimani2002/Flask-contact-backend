from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
CORS(app)

# === Mail Config (for Gmail) ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gopimani0904@gmail.com'           # 🔁 Change this if needed
app.config['MAIL_PASSWORD'] = 'aapjqqlrbywzqpjw'                 # 🔁 Change this if needed
app.config['MAIL_DEFAULT_SENDER'] = 'gopimani0904@gmail.com'     # 🔁 Change this if needed

mail = Mail(app)

# === Test Route ===
@app.route('/', methods=['GET'])
def home():
    return "Flask backend is running!"

# === Contact API ===
@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Save to file
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Message: {message}\n")
        f.write("-" * 40 + "\n")

    # Send Email
    msg = Message(subject=f"New Contact Message from {name}",
                  recipients=['gopimani0904@gmail.com'])  # 🔁 Change this if needed
    msg.body = f"""
You received a new message:

Name: {name}
Email: {email}

Message:
{message}
"""
    try:
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'Message sent and emailed successfully!'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Failed to send email.'}), 500

if __name__ == '_main_':
    app.run(debug=True)