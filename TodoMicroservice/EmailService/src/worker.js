import amqp from "amqplib/callback_api.js";
import { config } from "dotenv";
config();
import sendMail from "./send_mail.js";

amqp.connect(process.env.AMQP_HOST, function (error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function (error1, channel) {
    if (error1) {
      throw error1;
    }

    const queue = process.env.QUEUE;

    channel.assertQueue(queue, {
      durable: true,
    });

    channel.prefetch(1);
    console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

    channel.consume(
      queue,
      function (msg) {
        const { action, payload } = JSON.parse(msg.content.toString());

        // send mail here

        switch (action) {
          case "send_account_verification_email":
            console.log(" [*] Processing...");

            sendMail(
              payload?.email,
              "Verify your account",
              `Your otp is ${payload?.otp}`
            );

            console.log(" [*] Done");
            break;

          case "send_task_creation_email":
            console.log(" [*] Processing...");

            sendMail(
              payload?.email,
              "Task created successfully",
              `A new task "${payload?.task_title}" has been created with your account`
            );

            console.log(" [*] Done");
            break;

          default:
            break;
        }

        channel.ack(msg);
      },
      {
        noAck: false,
      }
    );
  });
});
