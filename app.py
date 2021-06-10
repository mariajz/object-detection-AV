
from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
from keras.models import model_from_json
from flask import send_file
import sys
import urllib.request
  
app = Flask(__name__)

resized_shape = (160, 256)

json_file = open('model/model_car.json', 'r', encoding='utf-8-sig')
loaded_model_json = json_file.read()
json_file.close()
model_car = model_from_json(loaded_model_json)
model_car.load_weights("model/model_car.h5")
print("Loaded model1 from disk")

json_file = open('model/model_pedestrian.json', 'r',encoding='utf-8-sig')
loaded_model_json = json_file.read()
json_file.close()
model_pedestrian = model_from_json(loaded_model_json)
model_pedestrian.load_weights("model/model_pedestrian.h5")
print("Loaded model2 from disk")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/testimage', methods=['POST'])
def upload_file():

    if request.method == "POST":
        uploaded_file = request.files['image']

    npimg = np.fromfile(uploaded_file, np.uint8)
    test_img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    test_img = cv2.resize(test_img, (resized_shape[1], resized_shape[0]))
    img = test_img.copy()
    test_img = np.expand_dims(test_img, axis=0)

    pred_all_car = model_car.predict(test_img)
    pred_all_pedestrian= model_pedestrian.predict(test_img)

    im_pred_car = np.array(255*pred_all_car[0], dtype=np.uint8)
    rgb_mask_box = im_pred_car
    ret, thresh = cv2.threshold(rgb_mask_box, 127, 255, 0)
    img2 = img.copy()
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(rgb_mask_box, contours, -1, (0, 255, 0), 3)
    for c in contours:
      rect = cv2.boundingRect(c)
      x, y, w, h = rect
      cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 3)
      cv2.putText(img2, 'CAR', (x, y-5), 0, 0.3, (0, 255, 0))


    
    im_pred_pedestiran = np.array(255*pred_all_pedestrian[0],dtype=np.uint8)
    rgb_mask_box= im_pred_pedestiran
    ret,thresh = cv2.threshold(rgb_mask_box,127,255,0)
    img3 = img2.copy()
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(rgb_mask_box, contours, -1, (255,0,0), 3)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(img3,(x,y),(x+w,y+h),(255,0,0),3)
        cv2.putText(img3,'PEDESTRIAN',(x,y-5),0,0.3,(255,0,0))


    _, buffer = cv2.imencode('.png', img3)
    encoded_img_data = base64.b64encode(buffer)
    img_data = encoded_img_data.decode('utf-8')
    return jsonify({'status':str(encoded_img_data)})



@app.route('/testurl', methods=['POST'])
def upload_url():
    
    if request.method == "POST":
        image_path = request.get_data()
    image_path = image_path.decode("utf-8") 
    print(image_path)
    #image_path = "https://www.drivespark.com/images/2021-04/jaguar-i-pace-black-edition-2.jpg"

    resp = urllib.request.urlopen(image_path)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    test_img = cv2.resize(image,(resized_shape[1],resized_shape[0]))
    img= test_img.copy()

    test_img = np.expand_dims(test_img, axis=0)

    pred_all_car = model_car.predict(test_img)
    pred_all_pedestrian= model_pedestrian.predict(test_img)

    im_pred_car = np.array(255*pred_all_car[0], dtype=np.uint8)
    rgb_mask_box = im_pred_car
    ret, thresh = cv2.threshold(rgb_mask_box, 127, 255, 0)
    img2 = img.copy()
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(rgb_mask_box, contours, -1, (0, 255, 0), 3)
    for c in contours:
      rect = cv2.boundingRect(c)
      x, y, w, h = rect
      cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 3)
      cv2.putText(img2, 'CAR', (x, y-5), 0, 0.3, (0, 255, 0))


    
    im_pred_pedestiran = np.array(255*pred_all_pedestrian[0],dtype=np.uint8)
    rgb_mask_box= im_pred_pedestiran
    ret,thresh = cv2.threshold(rgb_mask_box,127,255,0)
    img3 = img2.copy()
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(rgb_mask_box, contours, -1, (255,0,0), 3)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(img3,(x,y),(x+w,y+h),(255,0,0),3)
        cv2.putText(img3,'PEDESTRIAN',(x,y-5),0,0.3,(255,0,0))

    
    _, buffer = cv2.imencode('.png', img2)
    encoded_img_data = base64.b64encode(buffer)
    return jsonify({'status':str(encoded_img_data)})

	
@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



if __name__ == "__main__":
    app.run(debug = True) 
    
