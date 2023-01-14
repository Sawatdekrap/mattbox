import React, { useState } from "react";
import { ChatUpdateTypes } from "../constants";
import { ChatSubmitLineItf, ComponentUpdateItf } from "../interfaces";

interface ChatProps {
  id: string;
  lines: string[];
  sendComponentUpdate: (details: ComponentUpdateItf) => void;
}

const Chat = ({ id, lines, sendComponentUpdate }: ChatProps) => {
  const [input, setInput] = useState("");

  const onSubmit = () => {
    const updateDetails: ChatSubmitLineItf = {
      type: ChatUpdateTypes.SUBMIT,
      line: input,
    };
    sendComponentUpdate(updateDetails);
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
