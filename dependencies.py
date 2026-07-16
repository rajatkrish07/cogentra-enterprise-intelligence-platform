from fastapi.params import Depends
from schemas import CurrentUser


def get_api_version() -> str:
    return "v1"

def get_curr_user() -> CurrentUser:
    return CurrentUser(
        username="rajatkr_07",
        email="rajatkrishnan2002@gmail.com"
    )

