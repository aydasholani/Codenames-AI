document.addEventListener("DOMContentLoaded", function () {
  const socket = io();

  // Hämtar room_id och username från URL-parametrarna
  const roomId = new URLSearchParams(window.location.search).get("room_id");
  const username = new URLSearchParams(window.location.search).get("username");

  // Emit för att gå med i rummet så fort sidan laddats
  socket.emit("join_room_event", { room_id: roomId, username: username });

  // Uppdaterar användarlistan när en ny användare ansluter
  socket.on("update_user_list", function (data) {
    const userList = document.getElementById("user-list");
    userList.innerHTML = ""; // Rensar listan för att förhindra duplicering

    data.users.forEach((user) => {
      const newUser = document.createElement("li");
      newUser.textContent = `${user} joined the room`;
      userList.appendChild(newUser);
    });
  });

  // Hantera användare som lämnar rummet
  socket.on("user_left", function (data) {
    const userList = document.getElementById("user-list");
    const userItem = Array.from(userList.children).find((li) =>
      li.textContent.includes(data.username)
    );
    if (userItem) {
      userItem.textContent = `${data.username} left the room`;
      userItem.style.color = "red"; // Visar att användaren har lämnat
    }
  });

  // Emit när användaren stänger fliken eller webbläsaren
  window.addEventListener("beforeunload", () => {
    socket.emit("leaving_room", { room_id: roomId, username: username });
  });
});
