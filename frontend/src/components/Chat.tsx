import React from "react";

interface ChatProps {
  id: string;
  lines: string[];
}

const Chat = ({ id, lines }: ChatProps) => {
  return (
    <div>
      {lines.map((line, lineIdx) => (
        <p key={lineIdx}>{line}</p>
      ))}
    </div>
  );
};

export default Chat;
