import * as WebSocket from "ws";
import { createInterface } from "readline";

const readline = createInterface({
  input: process.stdin,
  output: process.stdout,
});
readline.setPrompt("> ");

const ws = new WebSocket("ws://localhost:8888");
ws.on("message", (message: string) => {
  console.log(message);
  readline.prompt();
});

readline.prompt();
readline.on("line", message => {
  ws.send(message);
});
