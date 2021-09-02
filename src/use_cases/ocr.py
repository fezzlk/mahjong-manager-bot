"""ocr"""

from server import logger
from services import (
    ocr_service,
    reply_service,
)


class OcrUseCases:
    """ocr UseCases"""

    def input_result_from_image(self, image_content):
        ocr_service.run(image_content)
        if ocr_service.isResultImage():
            results = ocr_service.get_points()
            if results is None:
                return

            res_message = "\n".join([
                f'{user}: {(point//100)*100}' for user, point in results.items()
            ])
            reply_service.add_message(res_message)
            reply_service.add_submit_results_by_ocr_menu(results)

        else:
            logger.warning(
                'this image is not result of jantama'
            )
        ocr_service.delete_result()
