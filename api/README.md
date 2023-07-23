# Leaf Detection and Labeling API

The Leaf Detection and Labeling API is a RESTful service that allows users to predict and label leaves in an image. It provides two main methods, `/label` and `/predict`, which take a JSON input containing an `img_url` and return the respective results.

## Endpoints

### `POST /predict`

Predicts and labels leaves in the input image and returns the results as a JSON response.

#### Request

```json
POST /predict

{
  "img_url": "https://example.com/path/to/image.jpg"
}
```

#### Response

```
{
	"detections": [
		{
			"cls": "Corn",
			"conf": 0.7053574919700623,
			"disease": {
				"cls": "Cercospora_leaf_spot Gray_leaf_spot",
				"conf": 0.4618198275566101
			},
			"xyxy": [
				36,
				0,
				1257,
				835
			]
		}
	]
}
```

### `POST /label`
Labels leaves in the input image and returns the rendered image with bounding boxes.

#### Request

```json
POST /label

{
  "img_url": "https://example.com/path/to/image.jpg"
}
```

#### Response

![rendered image with bounding boxes](https://raw.githubusercontent.com/glucard/Leaves-dataset/dev/api/output.jpg)

## Usage
To use the API, make a POST request to the desired endpoint with a JSON payload containing the img_url. The API will process the image and return the predictions or a labeled image accordingly.

Make sure to handle the API response correctly in your application code.