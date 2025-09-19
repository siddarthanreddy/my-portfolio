// menu toggle
document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.getElementById("menuBtn");
  const navLinks = document.getElementById("navLinks");

  if (menuBtn) {
    menuBtn.addEventListener("click", () => {
      const visible = navLinks.style.display === "flex";
      navLinks.style.display = visible ? "none" : "flex";
    });
  }

  // reveal on scroll
  const reveals = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.12 }
  );
  reveals.forEach((el) => io.observe(el));

  // footer year
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // contact form
  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const message = document.getElementById("message").value.trim();
      const status = document.getElementById("formStatus");

      status.textContent = "Sending...";
      try {
        const res = await fetch("/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, message }),
        });
        const data = await res.json();
        if (res.ok) {
          status.textContent = "Message sent — thank you!";
          contactForm.reset();
        } else {
          status.textContent = data.message || "Submission failed.";
        }
      } catch (err) {
        status.textContent = "Network error — try again.";
        console.error(err);
      }
      setTimeout(() => (status.textContent = ""), 5000);
    });
  }
});
