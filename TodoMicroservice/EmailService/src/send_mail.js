import transporter from "./config/transporter.config.js";
import { config } from "dotenv";
config();

async function sendMail(to, subject, message) {
  const info = await transporter.sendMail({
    from: `"Todo Microservice" <${process.env.EMAIL_USER}>`,
    to: [to],
    subject: subject,
    text: message,
    html: `<p>${message}</p>`,
  });

  console.log("Message sent: %s", info.messageId);
}

export default sendMail;
