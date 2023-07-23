# Loading models

Sequence of steps to use each model.

## Disease_models

- Import tensorflow;
- import the model using `model = keras.models.load_model('path/to/location.keras')`;
- Learn more at Tensorflow website https://www.tensorflow.org/guide/keras/serialization_and_saving

## Yolo_leaf_classifier

```
from ultralytics import YOLO

# Load a model
model = YOLO("path/to/model.pt")  # load a pretrained model (recommended for training)

# Use the model
results = model("path/to/leaf.jpg")  # predict on an image
```
- Learn more at yolov8 ultralytics repository https://github.com/ultralytics/ultralytics#readme
- See more predicting at https://docs.ultralytics.com/modes/predict/#inference-sources