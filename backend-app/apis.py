from flask import Flask, jsonify, request
from flask_cors import CORS;
from smart import processData, build_model1, build_model2, build_model3, train_model, test_model;
# from smart1 import training_model4, testing_model4, load_model4

app = Flask(__name__)
CORS(app);

@app.route('/train', methods=['GET'])
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


@app.route('/status', methods=['GET'])
def get_status():
    training_status = 1
    response_data = {"status": 1}
    return jsonify(response_data), 200  #  200 OK status code



@app.route('/load-model', methods=['GET'])
def get_model_status():
    model_status = 1  
    response_data = {"status": model_status}
    return jsonify(response_data), 200  # Return 200 OK status code



@app.route('/test', methods=['GET'])
def test_image():
    # req_data = request.json  # need to get the JSON data from the request
    # image_url = req_data.get('url') #
    train_ds, val_ds = processData();
    model1 = build_model1();
    train_model(train_ds, val_ds, model1);
    result_list = test_model(model1);

    # model = training_model4();
    # model = load_model4();
    # result_list=testing_model4(model);
    
    # sign, accuracy, msg, sound = test_image_function(image_url) # need to call the function to test the image and get the results
    
    # # response JSON object
    # response_data = {
    #     "sign": sign,
    #     "accuracy": accuracy,
    #     "msg": msg,
    #     "sound": sound
    # }
    
    response_data = result_list;

    return jsonify(response_data), 200  #201 CREATED status code

if __name__ == '__main__':
    app.run()
