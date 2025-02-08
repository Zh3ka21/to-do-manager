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

function enableTaskEdit(taskId) {
  console.log("Editing Task ID:", taskId); // Debugging line
  let titleElement = document.getElementById(`task-title-${taskId}`);
  let inputElement = document.getElementById(`edit-task-input-${taskId}`);

  if (!titleElement || !inputElement) {
    console.error("Elements not found for Task ID:", taskId);
    return;
  }

  titleElement.style.display = "none";
  inputElement.style.display = "block";
  inputElement.focus();
}

function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// Set CSRF token dynamically for all HTMX requests
document.addEventListener("htmx:configRequest", (event) => {
  event.detail.headers["X-CSRFToken"] = getCSRFToken();
});

document.addEventListener("DOMContentLoaded", function () {
  const calendarIcon = document.getElementById("calendar-icon");
  if (calendarIcon) {
    calendarIcon.addEventListener("click", openCalendarModal); // Open the modal on icon click
  }
  initCalendar();
});

const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
let currentDate = new Date();
let projects = [];

document.addEventListener("DOMContentLoaded", function () {
  const calendarButton = document.querySelector("[data-calendar-trigger]");
  if (calendarButton) {
    calendarButton.addEventListener("click", openCalendarModal);
  }
  initCalendar();
});

function initCalendar() {
  document.getElementById("weekdays").innerHTML = DAYS.map(
    (day) => `<div class="weekday">${day}</div>`
  ).join("");
  updateCalendar();
  fetchProjects();
}

function updateCalendar() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  document.getElementById(
    "current-month"
  ).textContent = `${MONTH_NAMES[month]} ${year}`;

  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  let daysHtml = "";

  for (let i = 0; i < firstDayOfMonth; i++) {
    daysHtml += `<div class="calendar-day blank"></div>`;
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(Date.UTC(year, month, day));
    const formattedDate = formatDate(date);
    const hasProject = projects.includes(formattedDate);

    daysHtml += `
            <div class="calendar-day ${hasProject ? "has-project" : ""}"
                 data-date="${formattedDate}"
                 onclick="selectDate('${formattedDate}')">
                ${day}
            </div>`;
  }

  document.getElementById("calendar-days").innerHTML = daysHtml;
}

function fetchProjects() {
  const month = currentDate.getMonth() + 1;
  const year = currentDate.getFullYear();

  fetch(`/project_dates/?month=${month}&year=${year}`)
    .then((response) => {
      console.log("Response:", response); // Log the raw response
      return response.json(); // Try to parse as JSON
    })
    .then((data) => {
      projects = data;
      updateCalendar();
    })
    .catch((error) => console.error("Error fetching projects:", error));
}

function selectDate(dateString) {
  console.log("Selected date string:", dateString);

  document
    .querySelectorAll(".calendar-day.selected")
    .forEach((el) => el.classList.remove("selected"));

  const selectedDay = document.querySelector(`[data-date='${dateString}']`);
  if (selectedDay) {
    selectedDay.classList.add("selected");
  }

  document.getElementById("project-form").style.display = "block";
  document.getElementById("selected-date").value = dateString;
}

function formatDate(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
    2,
    "0"
  )}-${String(date.getDate()).padStart(2, "0")}`;
}

function previousMonth() {
  currentDate.setMonth(currentDate.getMonth() - 1);
  updateCalendar();
  fetchProjects();
}

function nextMonth() {
  currentDate.setMonth(currentDate.getMonth() + 1);
  updateCalendar();
  fetchProjects();
}

function openCalendarModal() {
  document.getElementById("calendar-modal").style.display = "flex";
  initCalendar();
}

function closeCalendarModal() {
  document.getElementById("calendar-modal").style.display = "none";
  document.getElementById("project-form").style.display = "none";
  document.getElementById("project-title").value = "";
}

function handleProjectCreated() {
  fetchProjects();
  closeCalendarModal();
}
