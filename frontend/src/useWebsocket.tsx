import React, { useState, useRef, useEffect } from "react";

interface UseWebsocketProps {
  url: string;
}

const useWebsocket = ({ url }: UseWebsocketProps) => {
  const [lastMessage, setLastMessage] = useState("");

  const ws = useRef<WebSocket>();

  useEffect(() => {
    if (!ws.current) {
      ws.current = new WebSocket(url);

      ws.current.addEventListener("open", () => {
        console.log("Connection open");
      });
      ws.current.addEventListener("close", () => {
        console.log("Connection closed");
      });
      ws.current.addEventListener("message", (e) => {
        setLastMessage(e.data.toString());
      });
    }

    return () => {
      ws.current &&
        ws.current.readyState === WebSocket.OPEN &&
        ws.current.close();
    };
  }, [url]);

  const sendMessage = (message: string) => {
    ws.current && ws.current.send(message);
  };

  const isConnected = ws.current?.readyState === WebSocket.OPEN;

  return { sendMessage, lastMessage, isConnected };
};

export default useWebsocket;
