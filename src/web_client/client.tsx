import React, { useState, ChangeEvent } from 'react';
import ReactDOM from 'react-dom';

interface UserInputProps {
  submitMessage: Function
}

const UserInput = (props: UserInputProps) => {
  const [text, setText] = useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
  }

  const submitMessage = () => {
    props.submitMessage(text);
  }

  return (
    <div style={{width: "100%", backgroundColor: "grey"}}>
      <textarea id="input" value={text} onChange={handleChange}></textarea>
      <button onClick={submitMessage}>Submit</button>
    </div>
  );
}

const App = () => {
  const [messages, setMessages] = useState<string[]>([]);

  const submitMessage = (msg: string) => setMessages(messages.concat(msg));

  return (
    <div>
      <UserInput submitMessage={submitMessage} />
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("app"));
