from concurrent.futures import ThreadPoolExecutor
from math import ceil
from time import sleep
from typing import Dict
from typing import Union

from authorization_handler import firebase_auth_module
from common_constants import NUMBER_OF_RECORDS_PER_BATCH
from common_constants import NUMBER_OF_RECORDS_PER_BATCHES_CYCLE
from common_constants import NUMBER_OF_USERS
from common_constants import USER_ID_ALIAS
from common_constants import USER_ID_PREFIX
from common_constants import USER_RANK_ALIAS
from common_constants import USERS_COLLECTION
from common_constants import WAIT_TIME_BETWEEN_BATCHES
from common_constants import WAIT_TIME_BETWEEN_BATCHES_CYCLES
from decorators import timer
from dotenv import load_dotenv
from google.cloud import firestore_v1
from providers import get_sync_firestore_auth_module


load_dotenv()
firebase_auth_module()
firestore_client = get_sync_firestore_auth_module()


def create_dummy_user_data(index: int) -> Dict[str, Union[str, int]]:
    return {USER_ID_ALIAS: USER_ID_PREFIX + str(index), USER_RANK_ALIAS: index}


@timer
def load_dummy_users_data(number_of_records: int = NUMBER_OF_USERS) -> None:
    print(f"Dummy users docs to load: {number_of_records}")
    batches_cycles = ceil(NUMBER_OF_USERS / NUMBER_OF_RECORDS_PER_BATCHES_CYCLE)
    start_batches_cycle_from = 0
    end_batches_cycle_until = NUMBER_OF_RECORDS_PER_BATCHES_CYCLE
    for _ in range(batches_cycles):
        executor = ThreadPoolExecutor()
        for j in range(
            start_batches_cycle_from,
            end_batches_cycle_until,
            NUMBER_OF_RECORDS_PER_BATCH,
        ):
            start = j + 1
            end = (
                j + NUMBER_OF_RECORDS_PER_BATCH
                if number_of_records > j + NUMBER_OF_RECORDS_PER_BATCH
                else number_of_records
            )
            executor.submit(_load_dummy_users_data, start, end)
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


def _load_dummy_users_data(
    start: int, end: int, firestore_client: firestore_v1.Client = firestore_client
) -> None:
    batch = firestore_client.batch()
    users_collection = firestore_client.collection(USERS_COLLECTION)
    for i in range(start, end + 1):
        user_data = create_dummy_user_data(i)
        user_doc_ref = users_collection.document(user_data.get(USER_ID_ALIAS))
        batch.create(user_doc_ref, user_data)
    batch.commit()


if __name__ == "__main__":
    load_dummy_users_data()
