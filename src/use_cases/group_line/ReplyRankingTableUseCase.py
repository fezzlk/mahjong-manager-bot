from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    user_service,
    user_hanchan_service,
    user_match_service,
    match_service,
    hanchan_service,
)
import env_var
from ApplicationService import message_service
from messaging_api_setting import line_bot_api
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List
from datetime import datetime


class ReplyRankingTableUseCase:
    def execute(self) -> None:
        req_line_user_id = request_info_service.req_line_user_id
        mention_line_user_ids = request_info_service.mention_line_ids
        messages = []
        target_user_ids: List[int] = []
        active_user_line_ids: List[str] = []
        line_id_name_dict: Dict[str, str] = {}
        contain_not_friend_user = False

        mention_line_user_ids.append(req_line_user_id)

        # 表示対象のユーザ情報の取得
        for mention_line_user_id in set(mention_line_user_ids):
            user = user_service.find_one_by_line_user_id(mention_line_user_id)

            if user is None:
                contain_not_friend_user = True
                continue

            line_id_name_dict[user.line_user_id] = user.line_user_name
            active_user_line_ids.append(user.line_user_id)
            target_user_ids.append(user._id)

        if contain_not_friend_user:
            reply_service.add_message("友達登録されていないユーザは表示されません。")

        if request_info_service.is_mention_all:
            reply_service.add_message("@Allによるメンションでは、このグループでの対戦に参加したことのある全ユーザを対象とします。")

        from_str = request_info_service.params.get('from')
        to_str = request_info_service.params.get('to')
        from_dt, from_is_invalid = message_service.parse_date_from_text(from_str)
        to_dt, to_is_invalid = message_service.parse_date_from_text(to_str)
        if from_is_invalid or to_is_invalid:
            reply_service.add_message('日付は以下のフォーマットで入力してください。')
            reply_service.add_message('[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD')
            return
        umList = user_match_service.find_all_by_user_id_list(
            target_user_ids,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        matches = match_service.find_all_by_ids_and_line_group_ids(
            ids=[um.match_id for um in umList],
            line_group_ids=[request_info_service.req_line_group_id],
        )
        hanchans = hanchan_service.find_all_archived_by_match_ids(
            match_ids=[m._id for m in matches],
        )
        user_hanchans = user_hanchan_service.find_all_with_line_user_ids_and_hanchan_ids(
            line_user_ids=active_user_line_ids,
            hanchan_ids=[h._id for h in hanchans],
            from_dt=from_dt,
            to_dt=to_dt,
        )
            
        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        display_name_dict = {}
        for line_id in active_user_line_ids:
            profile = line_bot_api.get_profile(line_id)
            
            import certifi
            import urllib3
            request_methods = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = request_methods.request('GET', profile.picture_url)
            f = open(f'src/uploads/profile_image/{line_id}.jpeg', 'wb')
            f.write(response.data)
            f.close()

            display_name_dict[line_id] = profile.display_name

        # データ集計
        # 累計スコア
        total_dict = {line_id: 0 for line_id in active_user_line_ids}
        for match in matches:
            for line_id, score in match.sum_scores.items():
                if line_id in active_user_line_ids:
                    total_dict[line_id] += score
        
        point_dict = {line_id: [] for line_id in active_user_line_ids}
        rank_dict = {line_id: {1: 0, 2: 0, 3: 0, 4: 0, 0: 0} for line_id in active_user_line_ids}
        for uh in user_hanchans:
            point_dict[uh.line_user_id].append(uh.point)
            rank_dict[uh.line_user_id][uh.rank] += 1
            if uh.point < 0:
                rank_dict[uh.line_user_id][0] += 1

        dummy_min_score = -10000
        max_score_dict = {line_id: dummy_min_score for line_id in active_user_line_ids}
        for h in hanchans:
            for u, c in h.converted_scores.items():
                if u in max_score_dict:
                    max_score_dict[u] = max(max_score_dict[u], c)

        ave_rank_str_dict = {}
        ave_rank_dict = {}
        for line_id in rank_dict:
            h_count = sum([rank_dict[line_id][i] for i in range(1, 5)])
            if h_count == 0:
                ave_rank_str_dict[line_id] = '-'
                ave_rank_dict[line_id] = 5
            else:
                ave_rank_str_dict[line_id] = '{:.2f}'.format(sum([rank_dict[line_id][i] * i for i in range(1, 5)]) / h_count)
                ave_rank_dict[line_id] = sum([rank_dict[line_id][i] * i for i in range(1, 5)]) / h_count

        # 画像生成
        scale = 1
        width, height = 1024 * scale, (768 + 110 * max(0, len(active_user_line_ids) - 6)) * scale
        bg_color = (33, 33, 33, 255)
        base_image = Image.new("RGBA", (width, height), bg_color)

        # 王冠画像添付
        crowns_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        gold = Image.open('src/static/images/ranking_table/crown_gold.png')
        silver = Image.open('src/static/images/ranking_table/crown_silver.png')
        bronze = Image.open('src/static/images/ranking_table/crown_bronze.png')
        crowns = [(gold, 7, 77), (silver, 13, 190), (bronze, 7, 300)]
        for i in range(min(3, len(active_user_line_ids))):
            crowns_image.paste(crowns[i][0], (crowns[i][1] * scale, crowns[i][2] * scale))
        base_image = Image.alpha_composite(base_image, crowns_image)

        sorted_total_dict = sorted(
            total_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )
        for i, r in enumerate(sorted_total_dict):
            profile_image = Image.open(f'src/uploads/profile_image/{r[0]}.jpeg')
            profile_image = profile_image.resize((50 * scale, 50 * scale))
            mask = Image.new("L", profile_image.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, profile_image.size[0], profile_image.size[1]), fill=255)
            h = (90 + 110 * i) * scale
            base_image.paste(profile_image, (110 * scale, h), mask)

        draw = ImageDraw.Draw(base_image)

        # 文字設定
        font_path = env_var.FONT_FILE_PATH
        font_color = (255, 255, 255)

        col_font_size = 20 * scale
        col_font = ImageFont.truetype(font_path, col_font_size)

        text = '累計得点'
        w = 450 * scale
        h = 50 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '参加半荘数'
        w = 600 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '最高得点'
        w = 775 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '平均得点'
        w = 950 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')
        
        line_h = 65 * scale
        draw.line((0, line_h, width, line_h), fill=(255, 255, 255), width=2)
        
        font_size = 30 * scale
        font = ImageFont.truetype(font_path, font_size)
    
        for i, r in enumerate(sorted_total_dict):
            h = (120 + 110 * i) * scale

            text = str(i + 1)
            w = 50 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, stroke_width=1, align='center')

            text = display_name_dict[r[0]]
            w = 190 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='lm')
            draw.text((x, y), text, font_color, font=font, align='left')

            text = ('+' + str(r[1])) if r[1] > 0 else str(r[1])
            w = 450 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')

            text = str(len(point_dict[r[0]]))
            w = 600 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')

            if max_score_dict[r[0]] == dummy_min_score:
                text = '-'
            else:
                m = max_score_dict[r[0]]
                text = ('+' + str(m)) if m > 0 else str(m)
            w = 775 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
            
            if len(point_dict[r[0]]) == 0:
                text = '-'
            else:
                text = str(int(sum(point_dict[r[0]]) / len(point_dict[r[0]])))
            w = 950 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
            
            line_h = (175 + 110 * i) * scale
            draw.line((0, line_h, width, line_h), fill=(255, 255, 255), width=1)

        path = f'/ranking_table/{req_line_user_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        try:
            base_image.save(f"src/uploads{path}", quality=75)
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                'ランキングの画像アップロードに失敗しました',
                '送信者: ' + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        
        reply_service.add_image(f'{env_var.SERVER_URL}/uploads{path}')

        # 順位表画像生成
        scale = 1
        width, height = 1024 * scale, (768 + 110 * max(0, len(active_user_line_ids) - 6)) * scale
        bg_color = (33, 33, 33, 255)
        base_image = Image.new("RGBA", (width, height), bg_color)

        # 王冠画像添付
        crowns_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        gold = Image.open('src/static/images/ranking_table/crown_gold.png')
        silver = Image.open('src/static/images/ranking_table/crown_silver.png')
        bronze = Image.open('src/static/images/ranking_table/crown_bronze.png')
        crowns = [(gold, 7, 77), (silver, 13, 190), (bronze, 7, 300)]
        for i in range(min(3, len(active_user_line_ids))):
            crowns_image.paste(crowns[i][0], (crowns[i][1] * scale, crowns[i][2] * scale))
        base_image = Image.alpha_composite(base_image, crowns_image)

        sorted_ave_rank_dict = sorted(
            ave_rank_dict.items(),
            key=lambda x: x[1],
            reverse=False
        )
        for i, r in enumerate(sorted_ave_rank_dict):
            profile_image = Image.open(f'src/uploads/profile_image/{r[0]}.jpeg')
            profile_image = profile_image.resize((50 * scale, 50 * scale))
            mask = Image.new("L", profile_image.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, profile_image.size[0], profile_image.size[1]), fill=255)
            h = (90 + 110 * i) * scale
            base_image.paste(profile_image, (110 * scale, h), mask)

        draw = ImageDraw.Draw(base_image)

        # 文字設定
        font_path = env_var.FONT_FILE_PATH
        font_color = (255, 255, 255)

        col_font_size = 20 * scale
        col_font = ImageFont.truetype(font_path, col_font_size)

        text = '平均順位'
        w = 450 * scale
        h = 50 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '1位'
        w = 550 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '2位'
        w = 650 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')

        text = '3位'
        w = 750 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')
                
        text = '4位'
        w = 850 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')
        
        text = '飛び'
        w = 950 * scale
        x, y, x2, y2 = draw.textbbox((w, h), text, font=col_font, anchor='mm')
        draw.text((x, y), text, font_color, font=col_font, align='center')
        
        w1 = 0 * scale
        h1 = 65 * scale
        w2 = 1024 * scale
        h2 = h1
        draw.line((w1, h1, w2, h2), fill=(255, 255, 255), width=2)
        
        font_size = 30 * scale
        font = ImageFont.truetype(font_path, font_size)
    
        for i, r in enumerate(sorted_ave_rank_dict):
            h = (120 + 110 * i) * scale

            text = str(i + 1)
            w = 50 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, stroke_width=1, align='center')

            text = display_name_dict[r[0]]
            w = 190 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='lm')
            draw.text((x, y), text, font_color, font=font, align='left')

            text = ave_rank_str_dict[r[0]]
            w = 450 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')

            text = str(rank_dict[r[0]][1])
            w = 550 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
            
            text = str(rank_dict[r[0]][2])
            w = 650 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
                        
            text = str(rank_dict[r[0]][3])
            w = 750 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
            
            text = str(rank_dict[r[0]][4])
            w = 850 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')
            
            text = str(rank_dict[r[0]][0])
            w = 950 * scale
            x, y, x2, y2 = draw.textbbox((w, h), text, font=font, anchor='mm')
            draw.text((x, y), text, font_color, font=font, align='center')

            line_h = (175 + 110 * i) * scale
            draw.line((0, line_h, width, line_h), fill=(255, 255, 255), width=1)

        path = f'/ranking_table_rank/{req_line_user_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        try:
            base_image.save(f"src/uploads{path}", quality=75)
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                'ランキングの画像アップロードに失敗しました',
                '送信者: ' + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        
        reply_service.add_image(f'{env_var.SERVER_URL}/uploads{path}')
