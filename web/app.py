from flask import Flask, jsonify ,render_template
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
  return render_template("index.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
