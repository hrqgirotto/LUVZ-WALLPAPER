function updateDateTime() {
    const dateElement = document.getElementById('currentDate');
    const timeElement = document.getElementById('clock');
    
    const now = new Date();
    const options = { weekday: 'long', day: 'numeric', month: 'long' };
    const formattedDate = now.toLocaleDateString('pt-BR', options);
    
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    
    dateElement.textContent = formattedDate;
    timeElement.textContent = `${hours}:${minutes}`;
}

// Atualiza a data e hora a cada segundo
setInterval(updateDateTime, 1000);
updateDateTime();
