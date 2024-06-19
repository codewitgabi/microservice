from typing import Literal
import os
import requests


class HttpProducer:
    def __init__(self, service: Literal["auth"]):
        self.service = service  # can only be set to auth since our email service consumes with a message broker
        self.__api_root = (
            os.environ.get("AUTH_SERVICE_HOST")
            if self.service == "auth"
            else os.environ.get("AUTH_SERVICE_HOST")
        )

    def publish(self, action: Literal["get_user_data"], payload: dict | None = None):
        res = None

        match action:
            case "get_user_data":
                res = requests.get(f"{self.__api_root}/account/user/{payload.get("id")}")

                res = res.json()

            case _:
                raise Exception("Invalid action")
            
        return res.get("data")


class AuthServiceProducer(HttpProducer):
    def __init__(self, service = "auth"):
        super().__init__(service)


auth_producer = AuthServiceProducer()
