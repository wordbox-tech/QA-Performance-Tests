from typing import Final

from authorization_handler import firebase_auth_module
from common_constants import USER_ID_ALIAS
from common_constants import USER_ID_PREFIX
from common_constants import USER_RANK_ALIAS
from common_constants import USERS_COLLECTION
from csv_utils import export_to_csv
from dotenv import load_dotenv
from firestore_utils import get_collection
from google.cloud import firestore_v1
from providers import get_sync_firestore_auth_module


CSV_FILE_NAME: Final[str] = "./artillery/users.csv"
EMPTY_STRING: Final[str] = ""

load_dotenv()
firebase_auth_module()
firestore_client = get_sync_firestore_auth_module()


def get_users_data_and_export_to_csv(
    firestore_client: firestore_v1.Client = firestore_client,
):
    file_name = CSV_FILE_NAME
    field_names = [USER_ID_ALIAS, USER_RANK_ALIAS]
    users_collection = firestore_client.collection(USERS_COLLECTION)
    users_data = get_collection(coll_ref=users_collection, field_names=field_names)
    users_data_filter_by_prefix_in_id = [
        user
        for user in users_data
        if user.get(USER_ID_ALIAS, EMPTY_STRING).startswith(USER_ID_PREFIX)
    ]
    export_to_csv(file_name, field_names, users_data_filter_by_prefix_in_id)


if __name__ == "__main__":
    get_users_data_and_export_to_csv()
