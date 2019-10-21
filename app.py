from flask import Flask, request, jsonify #import main Flask class and request object
from functions.compare_function import getsimscore
from flask_cors import CORS

app = Flask(__name__) #create the Flask app
CORS(app)

@app.route('/getsimscore', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()
    print(req_data)
    data = req_data['filelist']
    result = getsimscore(data)
    print("DONE")
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000