const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
const navItems = document.querySelectorAll(".nav-links a");
const year = document.querySelector("#year");
const contactForm = document.querySelector("#contactForm");
const formStatus = document.querySelector("#formStatus");

if (year) {
  year.textContent = new Date().getFullYear();
}

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    document.body.classList.toggle("nav-open", isOpen);
  });

  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    });
  });
}

const sections = document.querySelectorAll("main section[id]");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        navItems.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
        });
      });
    },
    { rootMargin: "-45% 0px -45% 0px" }
  );

  sections.forEach((section) => observer.observe(section));
}

if (contactForm && formStatus) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    formStatus.textContent = "Thank you. Your message has been noted for this portfolio demo.";
    contactForm.reset();
  });
}

const heroCanvas = document.querySelector("#heroCanvas");

function drawHeroCanvas() {
  if (!heroCanvas) {
    return;
  }

  const context = heroCanvas.getContext("2d");
  const rect = heroCanvas.getBoundingClientRect();
  const pixelRatio = window.devicePixelRatio || 1;

  heroCanvas.width = rect.width * pixelRatio;
  heroCanvas.height = rect.height * pixelRatio;
  context.scale(pixelRatio, pixelRatio);
  context.clearRect(0, 0, rect.width, rect.height);

  const width = rect.width;
  const height = rect.height;
  const startX = width * 0.58;
  const startY = height * 0.2;
  const nodeWidth = Math.min(210, width * 0.32);
  const nodeHeight = 58;
  const gap = 34;
  const nodes = [
    { label: "Audience Insight", color: "#dbeafe" },
    { label: "Campaign Strategy", color: "#d9f6f2" },
    { label: "Content Workflow", color: "#eaf2ff" },
    { label: "Marketing Analytics", color: "#dbeafe" },
  ];

  context.fillStyle = "#f5f9ff";
  context.fillRect(width * 0.54, 0, width * 0.46, height);

  context.strokeStyle = "#bdd7ff";
  context.lineWidth = 2;
  context.beginPath();
  context.moveTo(startX + nodeWidth * 0.5, startY + nodeHeight);

  nodes.forEach((_, index) => {
    if (index === 0) {
      return;
    }
    const y = startY + index * (nodeHeight + gap);
    context.lineTo(startX + nodeWidth * 0.5, y);
  });
  context.stroke();

  nodes.forEach((node, index) => {
    const y = startY + index * (nodeHeight + gap);

    context.fillStyle = node.color;
    roundRect(context, startX, y, nodeWidth, nodeHeight, 8);
    context.fill();

    context.strokeStyle = "#b7cbe5";
    context.stroke();

    context.fillStyle = "#172033";
    context.font = "700 14px Arial, Helvetica, sans-serif";
    context.fillText(node.label, startX + 18, y + 35);
  });

  context.strokeStyle = "#3b82f6";
  context.lineWidth = 3;
  context.beginPath();
  context.moveTo(width * 0.62, height * 0.76);
  context.lineTo(width * 0.7, height * 0.68);
  context.lineTo(width * 0.78, height * 0.72);
  context.lineTo(width * 0.86, height * 0.57);
  context.lineTo(width * 0.93, height * 0.48);
  context.stroke();
}

function roundRect(context, x, y, width, height, radius) {
  context.beginPath();
  context.moveTo(x + radius, y);
  context.arcTo(x + width, y, x + width, y + height, radius);
  context.arcTo(x + width, y + height, x, y + height, radius);
  context.arcTo(x, y + height, x, y, radius);
  context.arcTo(x, y, x + width, y, radius);
  context.closePath();
}

drawHeroCanvas();
window.addEventListener("resize", drawHeroCanvas);
