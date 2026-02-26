import string
import secrets
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "super-secret-key-for-session" # Required for session storage

def generate_password(length, mode):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    if mode == "letters_only":
        pool = letters
    elif mode == "numbers_only":
        pool = digits
    elif mode == "letters_symbols":
        pool = letters + symbols
    elif mode == "numbers_symbols":
        pool = digits + symbols
    else:
        pool = letters + digits + symbols

    return ''.join(secrets.choice(pool) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        length = int(request.form.get('length', 16))
        mode = request.form.get('mode', 'all_mixed')
        password = generate_password(length, mode)
        
        # Update History: Keep the last 5 passwords
        history = session['history']
        history.insert(0, password) # Add new one to the top
        session['history'] = history[:5] # Keep only top 5
    
    return render_template('index.html', password=password, history=session['history'])

@app.route('/clear')
def clear_history():
    session['history'] = []
    return render_template('index.html', password="", history=[])

if __name__ == '__main__':
    app.run(debug=True)