document.addEventListener("DOMContentLoaded", function () {
  const socket = io();

  // Gå med i rummet direkt efter omdirigeringen
  const roomId = "{{ room_id }}";
  const username = "{{ username }}";

  socket.emit("join_room_event", { room_id: roomId, username: username });

  // Hantera lyckad anslutning till rummet
  socket.on("join_success", (data) => {
    console.log(`${data.username} has joined room ${data.room_id}`);
  });

  // Hantera andra användare som går med i rummet
  // socket.on("user_joined", (data) => {
  //   const userList = document.getElementById("user-list");
  //   const newUser = document.createElement("li");
  //   newUser.textContent = `${data.username} joined the room`;
  //   userList.appendChild(newUser);
  // });

  socket.on("user_joined", function (data) {
    const userList = document.getElementById("user-list");
    const existingUser = Array.from(userList.children).find(
      (li) => li.textContent === `${data.username} joined the room`
    );

    if (!existingUser) {
      const newUser = document.createElement("li");
      newUser.textContent = `${data.username} joined the room`;
      userList.appendChild(newUser);
    }
  });
    socket.on("user_joined", function (data) {
      const userList = document.getElementById("user-list");
      const newUser = document.createElement("li");
      newUser.textContent = `${data.username} joined the room`;
      userList.appendChild(newUser);
    });

});
