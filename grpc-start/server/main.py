from concurrent import futures

import grpc
import users_pb2
import users_pb2_grpc

from pydantic import BaseModel

class GetUserSchema(BaseModel):
    id: int


class UserServiceServer(users_pb2_grpc.UserService):
    def __init__(self):
        self.users = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "hobbies": ["reading", "painting"],
            },
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "age": 28,
                "hobbies": ["cooking", "gardening"],
            },
            {
                "name": "Alice Smith",
                "email": "alice@example.com",
                "age": 25,
                "hobbies": ["running", "swimming"],
            },
            {
                "name": "Bob Johnson",
                "email": "bob@example.com",
                "age": 35,
                "hobbies": ["dancing", "playing guitar"],
            },
        ]

    def CreateUser(self, request, context):
        name = request.name
        email = request.email
        age = request.age
        hobbies = request.hobbies

        return users_pb2.CreateUserResponse(
            data={"name": name, "email": email, "age": age, "hobbies": hobbies}
        )

    def GetUsers(self, request, context):
        return users_pb2.GetUsersResponse(data=self.users)

    def GetUser(self, request: GetUserSchema, context):
        user = self.users[request.id]

        return users_pb2.CreateUserResponse(data=user)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
