const loginForm = document.getElementById("loginForm");
const navbar = document.getElementById("navbar");
const loginSection = document.getElementById("login");

// Fake login (for now)
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  // After login success
  alert("Login successful!");

  // Change navbar
  navbar.innerHTML = `
    <li><a href="#home">Home</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#sizeinfo">Size Info</a></li>
    <li><a href="#status">Status</a></li>
    <li><a href="#logout" id="logoutBtn">Logout</a></li>
  `;

  // Hide login section
  loginSection.classList.add("hidden");

  // Logout handler
  document.getElementById("logoutBtn").addEventListener("click", () => {
    location.reload(); // refresh to reset navbar
  });
});
