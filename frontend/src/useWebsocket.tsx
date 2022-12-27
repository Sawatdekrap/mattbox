import React, { useRef, useEffect } from "react";
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
  const ws = useRef<WebSocket>();

  useEffect(() => {
    if (ws.current) return;

    const url = `ws://localhost:8000/games/${gameId}`;
    ws.current = new WebSocket(url);

    ws.current.addEventListener("open", () => {
      console.log("Connection open");
    });
    ws.current.addEventListener("close", () => {
      console.log("Connection closed");
    });
    ws.current.addEventListener("message", (e) => {
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

    return () => {
      console.log("Exiting useWebsocket render");
      ws.current && ws.current.close();
    };
  }, [gameId]);

  const sendComponentUpdate = (data: string) => {
    ws.current && ws.current.send(data);
  };

  return { sendComponentUpdate };
};

export default useWebsocket;
