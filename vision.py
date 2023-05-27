import os 
from dotenv import load_dotenv
import base64
from google.cloud import vision
from googleapiclient import discovery
from googleapiclient.errors import HttpError



# Load the contents of the .env file
load_dotenv()

# set up the authentication for GCP 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ['YOUR_SERVICE']

def recognize_captcha(api_key, image_path):
    try:
        # Create a service object for the Google Vision API
        service = discovery.build('vision', 'v1', developerKey=api_key, static_discovery=False)

        # Load the captcha image
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Encode the image in base64
        image_content = base64.b64encode(content).decode('UTF-8')

        # Create the request payload
        request_body = {
            'requests': [
                {
                    'image': {
                        'content': image_content
                    },
                    'features': [
                        {
                            'type': 'TEXT_DETECTION'
                        }
                    ]
                }
            ]
        }

        # Send the request to the Google Vision API
        response = service.images().annotate(body=request_body).execute()

        # Get the recognized text from the captcha image
        texts = response['responses'][0]['textAnnotations']

        if len(texts) > 0:
            captcha_text = texts[0]['description']
            return captcha_text
        else:
            return "No text found in the captcha image."
        
    except HttpError as error:
        print(f"An error occurred: {error}")

