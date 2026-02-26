import string
import secrets
from flask import Flask, render_template, request

app = Flask(__name__)

def generate_password(length, mode):
    # Character pool definitions
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Map the dropdown selection to the character pool
    if mode == "letters_only":
        pool = letters
    elif mode == "numbers_only":
        pool = digits
    elif mode == "letters_symbols":
        pool = letters + symbols
    elif mode == "numbers_symbols":
        pool = digits + symbols
    else:  # "all_mixed"
        pool = letters + digits + symbols

    # Generate the password
    return ''.join(secrets.choice(pool) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        mode = request.form.get('mode', 'all_mixed')
        password = generate_password(length, mode)
    
    return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)