# from ApplicationService import (
#     # ocr_service,
#     reply_service,
# )
# from linebot.models.events import Event
# from messaging_api_setting import line_bot_api


# class InputResultFromImageUseCase:

#     def execute(self, event: Event) -> None:
#         message_content = line_bot_api.get_message_content(
#             event.message._id
#         )

#         ocr_service.run(message_content.content)
#         if ocr_service.is_result_image():
#             results = ocr_service.get_points()
#             if results is None:
#                 return

#             res_message = "\n".join([
#                 f'{user}: {(point//100)*100}' for user, point in results.items()
#             ])
#             reply_service.add_message(res_message)
#             reply_service.add_submit_results_by_ocr_menu(results)

#         else:
#             print(
#                 'this image is not result of jantama'
#             )
#         ocr_service.delete_result()
