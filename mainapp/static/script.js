document.getElementById('butt').onclick = () => {
  const WebSocket = require('ws');
  const socket = new WebSocket('ws://127.0.0.1:8000/ws');
  socket.onopen = function(e) {
    socket.send(JSON.stringify({
      message: 'GGUYLVBYIHGYh'
    }));
  };

  socket.onmessage = function(event) {
    try {
      alert(event);
      console.log("AAA");
      console.log(event);
    } catch (e) {
      console.log('Error:', e.message);
    };
  };
}