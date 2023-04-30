from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/train', methods=['POST'])
def start_training():
    req_data = request.get_json()
    #need to add required data here
    try:
        time.sleep(100)  # Wait 15 minutes
        response_data = {"status": 1}
        return jsonify(response_data), 200 #working so 200 ok status code
    except:
        error_message = "error occurred during training."
        return jsonify({"error": error_message}), 400  #  400 ERROR status code


#training_status = 1

@app.route('/status', methods=['GET'])
def get_status():
    response_data = {"status": training_status}
    return jsonify(response_data), 200  #  200 OK status code


#model_status = 1  

@app.route('/load-model', methods=['GET'])
def get_model_status():
    response_data = {"status": model_status}
    return jsonify(response_data), 200  # Return 200 OK status code



@app.route('/test', methods=['POST'])
def test_image():
    req_data = request.json  # need to get the JSON data from the request
    image_url = req_data.get('url') #
    
    
    sign, accuracy, msg, sound = test_image_function(image_url) # need to call the function to test the image and get the results
    
    # response JSON object
    response_data = {
        "sign": sign,
        "accuracy": accuracy,
        "msg": msg,
        "sound": sound
    }

    return jsonify(response_data), 201  #201 CREATED status code

if __name__ == '__main__':
    app.run()
