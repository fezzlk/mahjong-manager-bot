"""ocr"""

import json
import os
import io
from google.cloud import vision
from google.oauth2 import service_account


class OcrService:
    """ocr service"""

    def __init__(self, services):
        self.services = services
        self.result = None
        self.client = None
        credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_raw != None:
            service_account_info = json.loads(
                credentials_raw, strict=False
            )
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def isResultImage(self):
        if self.result is None:
            self.services.app_service.logger.warning(
                'the requested image is not loaded(required execute self.run()'
            )
            return
        for text in self.result:
            print(text.description)
            if ('終局' in text.description):
                return True
        return False

    def run(self, content=None):
        if self.client == None:
            self.services.app_service.logger.warning(
                'ocr_service is not setup'
            )
            return
        """Detects text in the file."""

        image = vision.Image(content=content)

        self.services.app_service.logger.info(
            'ocr: text detection running'
        )
        response = self.client.text_detection(image=image)
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        self.result = response.text_annotations

    def delete_result(self):
        self.result = None

    def get_points(self):
        if self.result is None:
            self.services.app_service.logger.warning(
                'the requested image is not loaded(required execute self.run()'
            )

        # 00を含むテキストを抽出
        pos_points = []
        for text in self.result:
            if (text.description.endswith('00')):
                pos_upper_left_point = text.bounding_poly.vertices[1]
                pos_points.append(pos_upper_left_point)

        def sorter(v): return (v.y, v.x)
        pos_points = sorted(pos_points, key=sorter)

        # 1位と2位の点数の距離
        distance_x = pos_points[1].x - pos_points[0].x
        pre_distance_x = 34
        distance_y = pos_points[1].y - pos_points[0].y
        pre_distance_y = 168
        # 1位の点数の右上
        upper_x = pos_points[0].x
        pre_upper_x = 979
        upper_y = pos_points[0].y
        pre_upper_y = 313
        rates_x = [
            [(v - pre_upper_x)/pre_distance_x for v in rete_array]
            for rete_array in [
                [765, 1028],
                [843, 1056],
                [922, 1139],
                [1002, 1211],
            ]
        ]
        rates_y = [
            [(v - pre_upper_y)/pre_distance_y for v in rete_array]
            for rete_array in [
                [255, 302, 380],
                [435, 473, 533],
                [584, 622, 682],
                [727, 763, 827],
            ]
        ]

        # 各ボーダーの１位の点数の左上からの距離
        target_x = [
            [v * distance_x + upper_x for v in rete_array]
            for rete_array in rates_x
        ]
        target_y = [
            [v * distance_y + upper_y for v in rete_array]
            for rete_array in rates_y
        ]

        target_name_parts = [[], [], [], []]
        target_points = []

        for text in self.result:
            x = text.bounding_poly.vertices[0].x
            y = text.bounding_poly.vertices[0].y
            for i in range(4):
                range_x = target_x[i]
                range_y = target_y[i]
                if (x >= range_x[0]) & (x <= range_x[1]) & (y >= range_y[0]) & (y <= range_y[1]):
                    target_name_parts[i].append(text.description)
                if (x >= range_x[0]) & (x <= range_x[1])\
                        & (y >= range_y[1]) & (y <= range_y[2])\
                        & ((text.description.endswith('00')) | (text.description == '0')):
                    target_points.append(int(text.description))

        target_names = [''.join(parts) for parts in target_name_parts]

        results = {}
        for i in range(4):
            results[target_names[i]] = target_points[i]
        return results
