"""ocr"""

import json
import os


class OcrService:
    """ocr service"""

    def __init__(self, services):
        self.services = services

        from google.oauth2 import service_account
        # Read env data
        self.credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if self.credentials_raw != None:
            # Generate credentials
            service_account_info = json.loads(
                self.credentials_raw, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info)

    def run(self):
        self.detect_text('ex.JPG')

    def detect_text(self, path):
        if self.credentials_raw == None:
            self.services.reply_service.add_text('ocr_service is not setup')
            return
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient(credentials=self.credentials)
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')
        self.services.reply_service.add_text(texts[0].description)

        for text in texts:
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
