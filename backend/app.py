from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/generate')
def generate():
    return jsonify(message='ok')

if __name__ == '__main__':
    app.run()
