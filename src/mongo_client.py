from pymongo import MongoClient
import env_var

# Firestore MongoDB compatibility API requires these params in the DATABASE_URL
if "firestore.goog" in env_var.DATABASE_URL:
    required_uri_params = ["loadBalanced=true", "tls=true", "retryWrites=false"]
    missing_params = [p for p in required_uri_params if p not in env_var.DATABASE_URL]
    if missing_params:
        raise RuntimeError(
            "DATABASE_URL is missing required params for Firestore MongoDB compatibility: "
            + ", ".join(missing_params)
        )

mongo_client = MongoClient(env_var.DATABASE_URL)
db_name = env_var.DATABASE_NAME

line_users_collection = mongo_client[db_name].line_users
command_aliases_collection = mongo_client[db_name].command_aliases
user_groups_collection = mongo_client[db_name].user_groups
groups_collection = mongo_client[db_name].groups
group_settings_collection = mongo_client[db_name].group_settings
web_users_collection = mongo_client[db_name].web_users
hanchans_collection = mongo_client[db_name].hanchans
matches_collection = mongo_client[db_name].matches
user_matches_collection = mongo_client[db_name].user_matches
hanchan_matches_collection = mongo_client[db_name].hanchan_matches
user_hanchans_collection = mongo_client[db_name].user_hanchans
yakuman_users_collection = mongo_client[db_name].yakuman_users

print("Connected to DB server.")
