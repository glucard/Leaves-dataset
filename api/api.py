from flask import Flask, send_file
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
    with urllib.request.urlopen(img_url) as req:
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        print("Download completed!")

    return img

model = mount_model()

APP = Flask(__name__)
CORS(APP, support_credentials=True)
API = Api(APP)

class Label(Resource):

    @staticmethod
    @cross_origin(supports_credentials=True)
    def post():
        
        print("STARTING....")
        global model
        global download_image

        parser = reqparse.RequestParser()
        parser.add_argument('img_url')
        args = parser.parse_args() # creates dict

        try:
            
            # Getting img
            img_url = args['img_url'].lower()
            print(f"query img_src={img_url}")
            img = download_image(img_url)

            # predicting results
            predict = model(img)
            labeled_img = predict[0].plot() # is redenring only one img.

            # setting output
            cv2.imwrite("api/output.jpg", labeled_img)
            out = send_file("output.jpg")

        except urllib.error.HTTPError as error:
            print("Error: ", error)
            return {'error': "can't get image"}, 404
        
        except Exception as error:
            print(error)
            return {'error': "can't label."}, 404
        
        print("ENDED....")
        return out, 200
    
API.add_resource(Label, '/label')

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True, port='3000')
    print("Running...")