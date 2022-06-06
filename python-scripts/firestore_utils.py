from typing import Dict
from typing import List

from google.cloud import firestore_v1


def get_collection(
    coll_ref: firestore_v1.CollectionReference, field_names: List[str]
) -> List[Dict]:
    collection: List[Dict] = []
    docs = coll_ref.stream()
    for doc in docs:
        doc_dict_filtered = filter_dictionary(
            dictionary=doc.to_dict(), keys_to_filter=field_names
        )
        collection.append(doc_dict_filtered)
    return collection


def filter_dictionary(dictionary: Dict, keys_to_filter: List[str]) -> Dict:
    if not keys_to_filter:
        return dictionary
    dictionary_filtered = {k: v for k, v in dictionary.items() if k in keys_to_filter}
    return dictionary_filtered
