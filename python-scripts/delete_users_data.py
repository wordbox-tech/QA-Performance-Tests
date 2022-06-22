from concurrent.futures import ThreadPoolExecutor
from math import ceil
from time import sleep
from typing import Final
from typing import List

from authorization_handler import firebase_auth_module
from common_constants import NUMBER_OF_RECORDS_PER_BATCH
from common_constants import NUMBER_OF_RECORDS_PER_BATCHES_CYCLE
from common_constants import USER_ID_ALIAS
from common_constants import USER_ID_PREFIX
from common_constants import USERS_COLLECTION
from common_constants import WAIT_TIME_BETWEEN_BATCHES
from common_constants import WAIT_TIME_BETWEEN_BATCHES_CYCLES
from decorators import timer
from dotenv import load_dotenv
from google.cloud import firestore_v1
from providers import get_sync_firestore_auth_module


GREATER_THAN_OR_EQUAL_TO_SIGN: Final[str] = ">="
LESS_THAN_OR_EQUAL_TO_SIGN: Final[str] = "<="
HIGH_CODE_POINT_IN_UNICODE_RANGE: Final[str] = "\uf8ff"


load_dotenv()
firebase_auth_module()
firestore_client = get_sync_firestore_auth_module()
print("Getting users docs to delete...")
users_collection = firestore_client.collection(USERS_COLLECTION)
users_docs_ref = users_collection.where(
    USER_ID_ALIAS, GREATER_THAN_OR_EQUAL_TO_SIGN, USER_ID_PREFIX
).where(
    USER_ID_ALIAS,
    LESS_THAN_OR_EQUAL_TO_SIGN,
    USER_ID_PREFIX + HIGH_CODE_POINT_IN_UNICODE_RANGE,
)
users_docs_to_delete: List[firestore_v1.DocumentSnapshot] = list(users_docs_ref.get())


@timer
def delete_users_data() -> None:
    number_of_records = len(users_docs_to_delete)
    print(f"Users docs to delete: {number_of_records}")
    batches_cycles = ceil(number_of_records / NUMBER_OF_RECORDS_PER_BATCHES_CYCLE)
    start_batches_cycle_from = 0
    end_batches_cycle_until = NUMBER_OF_RECORDS_PER_BATCHES_CYCLE
    for _ in range(batches_cycles):
        executor = ThreadPoolExecutor()
        for j in range(
            start_batches_cycle_from,
            end_batches_cycle_until,
            NUMBER_OF_RECORDS_PER_BATCH,
        ):
            start = j
            end = (
                j + NUMBER_OF_RECORDS_PER_BATCH
                if number_of_records > j + NUMBER_OF_RECORDS_PER_BATCH
                else number_of_records
            )
            executor.submit(_delete_users_data, start, end)
            print(start, end)
            sleep(WAIT_TIME_BETWEEN_BATCHES)
            if end in [end_batches_cycle_until, number_of_records]:
                start_batches_cycle_from = end_batches_cycle_until
                end_batches_cycle_until = (
                    end_batches_cycle_until + NUMBER_OF_RECORDS_PER_BATCHES_CYCLE
                )
                break
        executor.shutdown()
        sleep(WAIT_TIME_BETWEEN_BATCHES_CYCLES)


def _delete_users_data(
    start: int, end: int, firestore_client: firestore_v1.Client = firestore_client
) -> None:
    batch = firestore_client.batch()
    for user_doc in users_docs_to_delete[start:end]:
        batch.delete(user_doc.reference)
    batch.commit()


if __name__ == "__main__":
    delete_users_data()
