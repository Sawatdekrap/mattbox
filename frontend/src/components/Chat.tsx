import React, { useState } from "react";

interface ChatProps {
  id: string;
  lines: string[];
  handleSubmission: (value: string) => void;
}

const Chat = ({ id, lines, handleSubmission }: ChatProps) => {
  const [input, setInput] = useState("");

  const onSubmit = () => {
    handleSubmission(input);
    setInput("");
  };

  return (
    <div>
      {lines.map((line, lineIdx) => (
        <p key={lineIdx}>{line}</p>
      ))}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={onSubmit}>Submit</button>
    </div>
  );
};

export default Chat;
