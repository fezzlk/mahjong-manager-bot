"""ocr"""

import json
import os


class OcrService:
    """ocr service"""

    def __init__(self, services):
        self.services = services
        self.result = None
        from google.oauth2 import service_account
        # Read env data
        self.credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        print('GOOGLE_APPLICATION_CREDENTIALS: ', self.credentials_raw)
        if self.credentials_raw != None:
            # Generate credentials
            service_account_info = json.loads(
                self.credentials_raw, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info)

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
        if self.credentials_raw == None:
            self.services.app_service.logger.warning(
                'ocr_service is not setup'
            )
            return
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient(credentials=self.credentials)

        image = vision.Image(content=content)

        self.services.app_service.logger.info(
            'ocr: text detection running'
        )
        response = client.text_detection(image=image)
        self.result = response.text_annotations

    def delete_result(self):
        self.result = None

    def get_points(self):
        if self.result is None:
            self.services.app_service.logger.warning(
                'the requested image is not loaded(required execute self.run()'
            )

        pos_PTs = []
        for text in self.result:
            if (text.description.startswith('PT')):
                pos_upper_left = text.bounding_poly.vertices[0]
                print('pos_upper_left', pos_upper_left)
                pos_PTs.append(pos_upper_left)

        if len(pos_PTs) != 4:
            print('cannot find 4 "PT" marks')
            self.services.reply_service.add_text('点数を読み取れませんでした。手入力してください。')
            return

        def sorter(v): return (v.y, v.x)
        pos_PTs = sorted(pos_PTs, key=sorter)

        # distance_between_PTs_y
        distance_between_PTs_y = pos_PTs[3].y - pos_PTs[0].y
        pre_upper_PT_y = 333
        pre_distance_between_PTs_y = 456
        rates_y = [
            [(v - pre_upper_PT_y)/pre_distance_between_PTs_y for v in rete_array]
            for rete_array in [
                [255, 302, 380],
                [435, 473, 533],
                [584, 622, 682],
                [727, 763, 827],
            ]
        ]

        # distance_between_PTs_x
        distance_between_PTs_x = pos_PTs[3].x - pos_PTs[0].x
        pre_upper_PT_x = 1176
        rates_x = [
            [(v - pre_upper_PT_x)/pre_distance_between_PTs_y for v in rete_array]
            for rete_array in [
                [765, 1028],
                [843, 1056],
                [922, 1139],
                [1002, 1211],
            ]
        ]

        # 一番上のPTの左上からの距離
        target_y = [
            [v * distance_between_PTs_y + pos_PTs[0].y for v in rete_array]
            for rete_array in rates_y
        ]
        target_x = [
            [v * distance_between_PTs_y + pos_PTs[0].x for v in rete_array]
            for rete_array in rates_x
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

        print('target_names', target_names)
        print('target_points', target_points)
        results = {}
        for i in range(4):
            results[target_names[i]] = target_points[i]
        return results

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
