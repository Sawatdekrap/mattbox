import React from "react";
import { ComponentItf } from "./interfaces";

interface UseWebsocketProps {
  gameId: string;
  onComponentUpdate: (data: string) => void;
  onLayoutUpdate: (components: ComponentItf[]) => void;
}

const useWebsocket = ({
  gameId,
  onComponentUpdate,
  onLayoutUpdate,
}: UseWebsocketProps) => {
  const url = `ws://localhost:8000/games/${gameId}`;

  const ws = new WebSocket(url);

  ws.addEventListener("open", () => {
    console.log("Connection open");
  });
  ws.addEventListener("close", () => {
    console.log("Connection closed");
  });
  ws.addEventListener("message", (e) => {
    // TODO properly serialize/deserialize
    const dataString: string = e.data.toString();
    console.log(`Recieved: ${dataString}`);

    if (dataString.startsWith("[")) {
      const components = JSON.parse(dataString) as ComponentItf[];
      onLayoutUpdate(components);
    } else {
      onComponentUpdate(dataString);
    }
  });

  const sendComponentUpdate = (data: string) => {
    ws.send(data);
  };

  return { sendComponentUpdate };
};

export default useWebsocket;
