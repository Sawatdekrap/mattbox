function pushMessage(msg) {
    const chat = document.getElementById('chat');
    const line = document.createElement('li');
    line.textContent = msg;
    chat.appendChild(line);
}

// Socket
const socket =  new WebSocket("ws://localhost:8888");
socket.onopen = () => {
    console.log("Connected to server");
    pushMessage("Joined chat");
};
socket.onmessage = (e) => {
    const msg = e.data;
    pushMessage(msg);
};
document.onclose = () => socket.close;
