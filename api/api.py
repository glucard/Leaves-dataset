from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
import tensorflow as tf
from ultralytics import YOLO
import requests
import cv2
import urllib
import numpy as np
import os
import json

IMG_SIZE = 299,299

def get_disease_cls_map():
    with open('models\\diseases_cls_map.json') as json_file:
        data = json.load(json_file)
    return data


def get_yolo_model():
    yolo_model = YOLO("models/yolo_leafs_v1.pt")
    return yolo_model

def get_disease_models():
    """
    returns a dict that have each disease model.
    """
    disease_models = {}

    plants_name = [d.split(".")[0] for d in os.listdir("models\\disease_models")]
    print(plants_name)

    for pn in plants_name:
        disease_models[pn] = tf.keras.models.load_model(f"models\\disease_models\\{pn}.keras")
    return disease_models

def download_image(img_url):
    print("Downloading image....")
    with urllib.request.urlopen(img_url) as req:
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'Load it as it is'
        print("Download completed!")

    return img

def preprocess_tf(img):
    """
    preprocess a img to use on disease models
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE, interpolation = cv2.INTER_AREA)
    img = np.expand_dims(img, axis=0)

    return img

yolo_model = get_yolo_model()
disease_models = get_disease_models()
disease_cls_map = get_disease_cls_map()

APP = Flask(__name__)
CORS(APP, support_credentials=True)
API = Api(APP)

class Label(Resource):

    @staticmethod
    @cross_origin(supports_credentials=True)
    def post():
        
        print("STARTING....")
        global yolo_model
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
            predict = yolo_model(img)
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
    
    
class Predict(Resource):

    @staticmethod
    @cross_origin(supports_credentials=True)
    def post():
        
        print("STARTING....")
        global yolo_model
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
            result = yolo_model(img)[0]
            cls_names = yolo_model.names
            print(cls_names)
            
            detections = []

            for b in result.boxes:
                """
                a process that will occur for each boxes (detection)
                """
                xyxy = b.xyxy.detach().cpu().numpy().tolist()[0] # detection boundaries
                xyxy = [int(p) for p in xyxy] # parsing to int.
                conf = b.conf.detach().cpu().numpy().tolist()[0] # detection confidence
                cls = cls_names[int(b.cls)] # detection class
                
                detection_img = img[xyxy[1]:xyxy[3]][xyxy[0]:xyxy[2]] # detection image selection
                preprocessed_dimg = preprocess_tf(detection_img)

                y_pred_disease = disease_models[cls].predict(preprocessed_dimg)[0]
                disease_cls = np.argmax(y_pred_disease)
                disease_cls_name = disease_cls_map[cls][disease_cls]

                disease = {
                    "cls": disease_cls_name,
                    "conf": float(y_pred_disease[disease_cls]), # parsing to float, or else flask throws a error: TypeError: Object of type float64 is not JSON serializable,
                }

                detections.append({
                    "xyxy": xyxy,
                    "conf": conf,
                    "cls": cls,
                    "disease": disease,
                })

            out = {
                "detections": detections,
            }

        except urllib.error.HTTPError as error:
            print("Error: ", error)
            return {'error': "can't get image"}, 404
        
        except Exception as error:
            print(error)
            return {'error': "can't label."}, 404
        
        print("ENDED....")
        return out, 200
    
API.add_resource(Label, '/label')
API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(host="0.0.0.0", debug=True, port='3000')
    print("Running...")