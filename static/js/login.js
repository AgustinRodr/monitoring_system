console.log("login.js cargado correctamente");

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  console.log("Respuesta login:", data);

  if (data.access_token) {
    localStorage.setItem("token", data.access_token);
    document.cookie = `access_token=${data.access_token}; path=/`;
    window.location.href = "/dashboard";
  } else {
    alert("Credenciales inválidas");
  }
});
