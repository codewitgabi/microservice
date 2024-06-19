import express from "express";
import { config } from "dotenv";
import proxy from "express-http-proxy";
import cors from "cors";
import logger from "morgan";
config();

const app = express();
app.set("port", process.env.PORT || 3000);

const auth_service_host = process.env.AUTH_SERVICE_HOST;
const todo_service_host = process.env.TODO_SERVICE_HOST;

// middlewares

app.use(logger("dev"));
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/auth/api", proxy(auth_service_host));
app.use("/todo/api", proxy(todo_service_host));

app.use("*", (req, res) => {
  res.status(404).json({ message: "Not Found" });
});

app.use((err, req, res, next) => {
  res
    .status(500)
    .json({
      message:
        err.message || "Internal server error, please contact administrator",
    });
});

const runserver = () => {
  app.listen(app.get("port"), () => {
    console.log(`Server is running on port ${app.get("port")}`);
  });
};

runserver();
