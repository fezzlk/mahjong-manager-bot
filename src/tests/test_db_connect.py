from db_setting import Session
session = Session()


def test_db_health_check():
    is_database_working = True

    try:
        # to check database we will execute raw query
        session.execute('SELECT 1')
    except Exception as e:
        print(str(e))
        is_database_working = False

    assert is_database_working


# def test_recieve_message():
#     from models import Users
#     # router.root(Event('hoge'))
#     new_user = Users(
#         name='name',
#         user_id='user_id',
#         mode=services.user_service.modes.wait.value,
#     )
#     services.request_info_service.db.session.add(new_user)
#     services.request_info_service.db.session.commit()
#     services.request_info_service.logger.info(f'create: {new_user.user_id} {new_user.name}')
#     print('hogehoge', new_user.name)

#     users = services.user_service.get()
#     for user in users:
#         print('fugafuga', user.user_id)
#     return new_user


# # def test_input():
# #     errors = []
# #     router.root(Event(req_user='a', event_type='follow'))
# #     router.root(Event(req_user='b', event_type='follow'))
# #     router.root(Event(req_user='c', event_type='follow'))
# #     router.root(Event(req_user='d', event_type='follow'))
# #     router.root(Event(req_user='e', event_type='follow'))

# #     router.root(Event('_input'))
# #     router.root(Event('10000', 'a'))
# #     result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
# #     if not result.points == '{"a": 10000}':
# #         errors.append("failed to input point")
# #     router.root(Event('@b 20000', 'a'))
# #     router.root(Event('60000', 'c'))
# #     router.root(Event('@e 60000', 'c'))
# #     router.root(Event('@e', 'c'))
# #     router.root(Event('@c 30000', 'e'))
# #     router.root(Event('@d 40000', 'd'))

# #     # assert no error message has been registered, else print messages
# #     assert not errors, "errors occured:\n{}".format("\n".join(errors))


# # def test_input_with_tobi():
# #     errors = []

# #     router.root(Event('_input'))
# #     router.root(Event('@a -10000'))
# #     result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
# #     if not result.points == '{"a": -10000}':
# #         errors.append("failed to input point")
# #     router.root(Event('@b 20000'))
# #     router.root(Event('@c 30000'))
# #     router.root(Event('@d 60000'))

#     # router.root(Event(='_tobi a', event_type='postback))

#     # router.root(Event('_input'))
#     # router.root(Event('@a -1000'))
#     # result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
#     # if not result.points == '{"a": 10000}':
#     #     errors.append("failed to input point")
#     # router.root(Event('@b -200'))
#     # router.root(Event('@c 51200'))
#     # router.root(Event('@d 50000'))

#     # router.root(Event(='_tobi', event_type='postback))

#     # # assert no error message has been registered, else print messages
#     # assert not errors, "errors occured:\n{}".format("\n".join(errors))
