// Socket
const socket =  new WebSocket("ws://localhost:8888");
socket.onopen = () => {
    console.log("Connected to server");
};
socket.onmessage = (e) => {
    console.log(`Message from server: ${e.data}`);
};
document.onclose = () => {socket.close();}

function sendMessage(){
    const input = document.getElementById('input');
    const message = input.value;
    socket.send(message);
    input.value = '';
    console.log(`Sent message: ${message}`);
}
