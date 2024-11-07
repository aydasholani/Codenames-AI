const socket = io("http://localhost:5000");

socket.on("connect", () => {
  console.log("Connected to server");
  console.log(roomCode)
  socket.emit("join", { room: roomCode});
  console.log(`Användare anslöt till rum: ${room_code}`)
});

// Lyssna på `update_user_list`
socket.on("update_user_list", (data) => {
  console.log("Uppdaterad användarlista från servern:", data.users);
  

  // Om data.users är null eller undefined, logga ett fel
  if (!data.users) {
    console.error("Användarlistan är tom eller undefined:", data);
    return;
  }

  // Uppdatera användarlistan i HTML
  const userList = document.getElementById("userList");
  userList.innerHTML = ""; // Rensa den befintliga listan

  // Lägg till varje användare från listan
  data.users.forEach((user) => {
    const newUserItem = document.createElement("li");
    newUserItem.textContent = user.username; // Visa användarnamnet
    userList.appendChild(newUserItem);
  });
});

// $(document).ready(function () {
//   var socket = io();
//   socket.on("my response", function (msg) {
//     $("#log").append("<p>Received: " + msg.data + "</p>");
//   });
//   $("form#emit").submit(function (event) {
//     socket.emit("my event", { data: $("#emit_data").val() });
//     return false;
//   });
//   $("form#broadcast").submit(function (event) {
//     socket.emit("my broadcast event", { data: $("#broadcast_data").val() });
//     return false;
//   });
// });