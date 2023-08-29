from pymongo import MongoClient
import env_var
import os

mongo_client = MongoClient(env_var.DATABASE_URL)
db_name = env_var.DATABASE_NAME
# ローカルから MongoDB Atlas に接続する場合は以下を使用
# import certifi
# mongo_client = MongoClient(env_var.DATABASE_URL, tlsCAFile=certifi.where())

line_users_collection = mongo_client[db_name].line_users
user_groups_collection = mongo_client[db_name].user_groups
groups_collection = mongo_client[db_name].groups
group_settings_collection = mongo_client[db_name].group_settings
web_users_collection = mongo_client[db_name].web_users
hanchans_collection = mongo_client[db_name].hanchans
matches_collection = mongo_client[db_name].matches
user_matches_collection = mongo_client[db_name].user_matches
hanchan_matches_collection = mongo_client[db_name].hanchan_matches

print(f'Connected DB server:{env_var.DATABASE_URL}')
