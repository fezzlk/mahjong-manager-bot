# class PlotUseCases:

#     def plot(self):
#         group_id = request_info_service.req_line_group_id¥
#         group_id = 'R808c3c802d36f386290630fc6ba10f0c'
#         matches = session\
#         .query(Matches).filter(and_(
#         Matches.status == 2,
#         Matches.line_group_id == group_id,
#         )).order_by(Matches.id.desc())\
#         .all()
#         match = matches[0]
#         print(match)
#         以下ResultServiceに移植
#         results = session\
#         .query(Results).filter(
#         Results.id.in_([int(s) for s in json.loads(match.hanchan_ids)]),
#         )\
#         .order_by(Results.id)\
#         .all()
#         x = []
#         y = pd.DataFrame({})
#         print(results)
#         for result in results:
#         y = y.append(pd.Series(json.loads(result.result), name=result.id))
#         print(y)
#         plt.figure()

#         # Data for plotting
#         t = np.arange(0.0, 2.0, 0.01)
#         s = 1 + np.sin(2 * np.pi * t)

#         fig, ax = plt.subplots()
#         ax.plot(t, s)

#         ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#                title='About as simple as it gets, folks')
#         ax.grid()
#         path = "static/images/graphs/fuga.png"

#         fig.savefig(path)
#         image_url = f'https://f4d896d5edd1.ngrok.io/{path}'
#         image_url = f'https://mahjong-manager.herokuapp.com/{path}'
#         reply_service.add_image(image_url)
