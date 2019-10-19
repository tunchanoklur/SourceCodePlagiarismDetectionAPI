from flask import Flask, request #import main Flask class and request object
from functions.compare_function import *
import json

app = Flask(__name__) #create the Flask app

@app.route('/getsimscore', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()
    print(req_data)
    data = req_data['filelist']
    result = {
        'similarity':getsimscore(data).tolist() 
    }
    print("DONE")
    print(result)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000