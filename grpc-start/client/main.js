const PROTO_PATH = "../protos/users.proto";

import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const target = "localhost:50051";
const userProto = grpc.loadPackageDefinition(packageDefinition).service.users;
const client = new userProto.UserService(
  target,
  grpc.credentials.createInsecure()
);

class UserServiceConsumer {
  constructor() {
    this.target = "localhost:50051";
    this.userProto =
      grpc.loadPackageDefinition(packageDefinition).service.users;
    this.client = new userProto.UserService(
      this.target,
      grpc.credentials.createInsecure()
    );
  }

  getUsers = () => {
    this.client.GetUsers({}, function (err, response) {
      return response.data;
    });
  };

  getUser = (id) => {
    this.client.GetUser({ id }, function (err, response) {
      return response.data;
    });
  };
}

const consumer = new UserServiceConsumer();

const users = consumer.getUsers();
console.log({ users });

export default consumer;
