import json
import os
from typing import Final

from google.cloud import firestore_v1
from google.oauth2 import service_account


FIRESTORE_CREDENTIALS_KEY: Final[str] = "FIREBASE_CREDENTIALS_PATH"


def get_sync_firestore_auth_module() -> firestore_v1.Client:
    credentials_json = json.loads(str(os.environ.get(FIRESTORE_CREDENTIALS_KEY)))
    return firestore_v1.Client(
        credentials=service_account.Credentials.from_service_account_info(
            credentials_json
        )
    )
