const socket = io();

// Anslut till rummet och meddela att en användare gått med
socket.emit("join_room", {
  room_code: "{{ room_code }}",
  username: "{{ user_name }}",
});

// Lyssna på användarens anslutning
socket.on("user_joined", function (data) {
  alert(data.username + " har gått med i rummet.");
});

// Lyssna när runda startas
socket.on("round_started", function () {
  alert("Ny runda har startat!");
  // Uppdatera sidan om det behövs
});

// Starta runda genom att meddela servern
function startRound() {
  socket.emit("start_round", { room_code: "{{ room_code }}" });
}
