function addPlayerInput() {
    const playerInputs = document.getElementById('player-inputs');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'player_names';
    input.placeholder = 'Spelare ' + (playerInputs.children.length + 1);
    playerInputs.appendChild(input);
}
