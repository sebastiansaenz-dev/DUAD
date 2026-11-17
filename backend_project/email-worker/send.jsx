import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createElement } from "react";
import { config } from "dotenv";
import { render } from "react-email";
import { Resend } from "resend";
import OrderConfirmedEmail from "./emails/OrderConfirmedEmail.jsx";

const workerDir = dirname(fileURLToPath(import.meta.url));
config({ path: resolve(workerDir, "../.env") });

if (!process.env.RESEND_API_KEY) {
  throw new Error("RESEND_API_KEY is missing");
}

const payload = JSON.parse(readFileSync(0, "utf8"));

if (!payload.to) {
  throw new Error("Missing recipient email");
}

const html = await render(createElement(OrderConfirmedEmail, payload));

const { data, error } = await new Resend(process.env.RESEND_API_KEY).emails.send({
  from: "PawStore <onboarding@resend.dev>",
  to: payload.to,
  subject: `PawStore — Pedido ${payload.orderNumber} confirmado`,
  html,
});

if (error) {
  throw new Error(error.message);
}

console.log(`Sent ${payload.orderNumber} to ${payload.to} (${data?.id ?? "ok"})`);
