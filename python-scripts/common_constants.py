from typing import Final


# Constants for loading and deleting users data
NUMBER_OF_RECORDS_PER_BATCH: Final[int] = 100
NUMBER_OF_RECORDS_PER_BATCHES_CYCLE: Final[int] = 10000
NUMBER_OF_USERS: Final[int] = 100000
WAIT_TIME_BETWEEN_BATCHES: Final[float] = 0.2
WAIT_TIME_BETWEEN_BATCHES_CYCLES: Final[float] = 1

# Constants related to user entity
USER_ID_ALIAS: Final[str] = "id"
USER_ID_PREFIX: Final[str] = "performancetestuser"
USER_RANK_ALIAS: Final[str] = "rank"
USERS_COLLECTION: Final[str] = "Users"
