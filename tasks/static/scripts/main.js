import { Calendar } from "./Calendar.js";
import { TaskManager } from "./TaskManager.js";
import { ProjectManager } from "./ProjectManager.js";

class Main {
  constructor() {
    this.calendar = new Calendar();
    this.taskManager = new TaskManager();
    this.projectManager = new ProjectManager();

    // Attach the Main instance to the window object
    window.main = this;

    this.init();
  }

  init() {
    document.addEventListener("DOMContentLoaded", () => {
      this.calendar.initCalendar();
      this.taskManager.initTaskForm();
      this.projectManager.initProjectForm();

      // Set CSRF token dynamically for all HTMX requests
      document.addEventListener("htmx:configRequest", (event) => {
        event.detail.headers["X-CSRFToken"] = this.getCSRFToken();
      });
    });
  }

  getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }

  showAlert(message, type = "success") {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type}`;
    alertDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px;
      border-radius: 4px;
      background-color: ${type === "success" ? "#4CAF50" : "#f44336"};
      color: white;
      z-index: 1000;
      transition: opacity 0.5s ease-in-out;
    `;
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);

    // Remove the alert after 3 seconds
    setTimeout(() => {
      alertDiv.style.opacity = "0";
      setTimeout(() => alertDiv.remove(), 500);
    }, 3000);
  }
}

const main = new Main();

if (document.getElementById("task-form")) {
  document
    .getElementById("task-form")
    .addEventListener("htmx:afterRequest", function () {
      console.log("Form submitted, clearing inputs.");
      document.getElementById("new-task").value = "";
      document.getElementById("deadline-time").value = "";
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const taskForm = document.getElementById("task-form");
  if (taskForm) {
    taskForm.addEventListener("htmx:afterRequest", function () {
      console.log("Form submitted, clearing inputs.");
      document.getElementById("new-task").value = "";
      document.getElementById("deadline-time").value = "";
    });
  }
});

// Set CSRF token dynamically for all HTMX requests
document.addEventListener("htmx:configRequest", (event) => {
  event.detail.headers["X-CSRFToken"] = getCSRFToken();
});

document.addEventListener("DOMContentLoaded", function () {
  const calendarIcon = document.getElementById("calendar-icon");
  if (calendarIcon) {
    calendarIcon.addEventListener("click", () =>
      main.calendar.openCalendarModal()
    );
  }
  main.calendar.initCalendar();
});

// document.addEventListener("DOMContentLoaded", function () {
//   const calendarButton = document.querySelector("[data-calendar-trigger]");
//   if (calendarButton) {
//     calendarButton.addEventListener("click", openCalendarModal);
//   }
//   initCalendar();
// });

// import { Calendar } from ".Calendar.js";
