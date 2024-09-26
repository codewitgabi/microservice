from __future__ import print_function
from typing import List

import grpc
import users_pb2
import users_pb2_grpc


class UserConsumer:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = users_pb2_grpc.UserServiceStub(self.channel)

    def create_user(
        self,
        username: str,
        email: str,
        age: int,
        hobbies: List[str],
    ):
        request = users_pb2.CreateUserRequest(
            name=username, email=email, age=age, hobbies=hobbies
        )

        response = self.stub.CreateUser(request)
        return response.data

    def get_users(self):
        request = users_pb2.GetUsersRequest()
        response = self.stub.GetUsers(request)

        return response.data

    def get_user(self, id: int):
        request = users_pb2.GetUserRequest(id=id)
        response = self.stub.GetUser(request)

        return response.data

    def close(self):
        self.channel.close()


user_consumer = UserConsumer()

# create a user

response = user_consumer.create_user(
    "Codewitgabi",
    "codewitgabi222@gmail.com",
    15,
    ["coding", "flirting", "cooking - no fear, na lie 😂😂"],
)

print(response)

# get all users

users = user_consumer.get_users()

print("All users:")

for user in users:
    print(
        f"Name: {user.name}, Email: {user.email}, Age: {user.age}, Hobbies: {user.hobbies}"
    )

user = user_consumer.get_user(0)

print("Get first user => username", user.name)
print("Get first user => email", user.email)

user_consumer.close()
