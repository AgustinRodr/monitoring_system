document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/login_page"; // si no hay token, redirige al login
    return;
  }

  // Ejemplo: pedir datos protegidos
  fetch("/api/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({hostname: "miPC"})
  })
  .then(res => res.json())
  .then(data => {
    console.log("Datos recibidos:", data);
  })
  .catch(err => console.error("Error:", err));
});

const ctx = document.getElementById("historialChart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: window.labels,
      datasets: [
        {
          label: "CPU %",
          data: window.cpuData,
          borderColor: "#00bfff",
          backgroundColor: "rgba(0, 191, 255, 0.1)",
          tension: 0.4,
          fill: true
        },
        {
          label: "RAM %",
          data: window.ramData,
          borderColor: "#bf00ff",
          backgroundColor: "rgba(191, 0, 255, 0.1)",
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: "white" } }
      },
      scales: {
        x: { ticks: { color: "white" }, grid: { color: "#333" } },
        y: {
          ticks: { color: "white" },
          grid: { color: "#333" },
          min: 0,
          max: 100
        }
      }
    }
  });