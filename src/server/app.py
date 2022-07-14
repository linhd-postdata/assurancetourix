from flask import Flask
import rantanplan 

app = Flask(__name__)

@app.route('/')
def hello_rantanplan():
    return f"Rantanplan version {rantanplan.__version__}" 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')