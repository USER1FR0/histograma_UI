# ==========================================================
# app.py — solo sirve el index.html estatico
# Vercel requiere una variable "app" exportada
# ==========================================================
from flask import Flask, send_from_directory
import os

app = application = Flask(__name__, static_folder='public')

@app.route("/")
def index():
    return send_from_directory('public', 'index.html')

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('public', filename)

if __name__ == "__main__":
    app.run(debug=True)