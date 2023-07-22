from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
import tensorflow as tf
from ultralytics import YOLO
import requests
import cv2
import urllib
import numpy as np

def mount_model():
    yolo_model = YOLO("models/yolo_leafs_v1.pt")
    return yolo_model

def download_image(img_url):
    print("Downloading image....")
    """response = requests.get(img_url)

    with open("image.jpg", "wb") as f:
        f.write(response.content)
    """
    with urllib.request.urlopen(img_url) as req:
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        print("Download completed!")

    return img

APP = Flask(__name__)
CORS(APP, support_credentials=True)
API = Api(APP)

model = mount_model()

class Predict(Resource):

    @staticmethod
    @cross_origin(supports_credentials=True)
    def post():
        
        print("STARTING....")
        global model
        global download_image

        parser = reqparse.RequestParser()
        parser.add_argument('img_url')
        args = parser.parse_args()  # creates dict


        try:
            img_url = args['img_url'].lower()

            img = download_image(img_url)
            
            print(f"query img_src={img_url}")
            predict = model(img)
            labeled_img = predict[0].plot() # is redenring only one img.
            cv2.imwrite("api/output.jpg", labeled_img)
            print(predict)
            out = {'Prediction': "testando"}
        except Exception as error:
            print(error)
            return {'error': "can't predict."}, 404
        
        print("ENDED....")
        return out, 200
    
API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True, port='3000')
    print("Running...")