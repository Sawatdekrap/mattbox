import React, { useRef, useEffect } from "react";
import { LayoutItf, ComponentItf } from "./interfaces";

interface UseWebsocketProps {
  gameId: string;
  onComponentUpdate: (data: string) => void;
  onLayoutUpdate: (layout: LayoutItf) => void;
}

const useWebsocket = ({
  gameId,
  onComponentUpdate,
  onLayoutUpdate,
}: UseWebsocketProps) => {
  const ws = useRef<WebSocket>();

  useEffect(() => {
    if (!ws.current) {
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
          const newLayout: LayoutItf = { components: components };
          onLayoutUpdate(newLayout);
        } else {
          onComponentUpdate(dataString);
        }
      });
    }

    return () => {
      ws?.current?.readyState === WebSocket.OPEN && ws.current.close();
    };
  }, [gameId]);

  const sendComponentUpdate = (data: string) => {
    ws.current && ws.current.send(data);
  };

  return { sendComponentUpdate };
};

export default useWebsocket;
