const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
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
let currentDate = new Date();
let projects = [];

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

function showAlert(message, type = "success") {
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

function enableTaskEdit(taskId) {
  console.log("Editing Task ID:", taskId);

  const titleElement = document.getElementById(`task-title-${taskId}`);
  const inputElement = document.getElementById(`edit-task-input-${taskId}`);

  if (!titleElement || !inputElement) {
    console.error("Elements not found for Task ID:", taskId);
    return;
  }

  // Show input and hide title
  titleElement.style.display = "none";
  inputElement.style.display = "block";
  inputElement.focus();
  inputElement.select();

  // Store original value in case we need to revert
  inputElement.dataset.originalValue = inputElement.value;

  // Handle Enter key submission
  inputElement.addEventListener("keyup", function handleKeyup(e) {
    console.log("Key pressed:", e.key);

    if (e.key === "Enter") {
      console.log("Enter pressed - submitting edit");
      submitEdit(taskId, inputElement.value);
      inputElement.removeEventListener("keyup", handleKeyup);
    } else if (e.key === "Escape") {
      console.log("Escape pressed - canceling edit");
      cancelEdit(taskId);
      inputElement.removeEventListener("keyup", handleKeyup);
    }
  });

  // Handle blur (clicking outside)
  inputElement.addEventListener("blur", function handleBlur() {
    console.log("Input blurred - submitting edit");
    submitEdit(taskId, inputElement.value);
    inputElement.removeEventListener("blur", handleBlur);
  });
}

function submitEdit(taskId, newValue) {
  const titleElement = document.getElementById(`task-title-${taskId}`);
  const inputElement = document.getElementById(`edit-task-input-${taskId}`);

  // Get CSRF token from cookie
  const csrftoken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  console.log("CSRF Token:", csrftoken);
  // Make the fetch request
  fetch(`/task/edit/${taskId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrftoken,
    },
    body: `title=${encodeURIComponent(newValue)}`,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      console.log("New task title:", newValue);
      return response.text();
    })
    .then((html) => {
      // Update the UI
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = html;
      const taskElement = document.getElementById(`task-${taskId}`);
      taskElement.replaceWith(tempDiv.firstElementChild);

      // Show success message
      showAlert("Task updated successfully!");
    })
    .catch((error) => {
      console.error("Error:", error);

      console.log("New task title:", newValue);
      showAlert("Failed to update task!", "error");
      cancelEdit(taskId);
    });
}

function cancelEdit(taskId) {
  console.log("Canceling edit for Task ID:", taskId);

  const titleElement = document.getElementById(`task-title-${taskId}`);
  const inputElement = document.getElementById(`edit-task-input-${taskId}`);

  if (!titleElement || !inputElement) {
    console.error("Elements not found for Task ID:", taskId);
    return;
  }

  // Reset to original value if available
  if (inputElement.dataset.originalValue) {
    inputElement.value = inputElement.dataset.originalValue;
  }

  titleElement.style.display = "block";
  inputElement.style.display = "none";
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

  fetchTasksForDate(dateString); // Fetch tasks when selecting a date
}

function fetchTasksForDate(dateString) {
  fetch(`/get_tasks_for_date/?date=${dateString}`)
    .then((response) => response.json())
    .then((data) => {
      const taskList = document.getElementById("task-list");
      taskList.innerHTML = ""; // Clear existing tasks

      console.log(data);

      // Update the project name
      const projectNamePlaceholder = document.getElementById(
        "project-name-placeholder"
      );
      if (projectNamePlaceholder && data.context && data.context.project) {
        projectNamePlaceholder.innerText = data.context.project.name;
      }

      // Check if there are no tasks
      if (data.context.tasks.length === 0) {
        taskList.innerHTML = "<p>No tasks for this day.</p>";
        return;
      }

      // Sort tasks by priority (higher priority first)
      data.context.tasks.sort((a, b) => b.priority - a.priority);

      // Loop through each task and build the HTML dynamically
      data.context.tasks.forEach((task) => {
        const taskHtml = `
        <div class="task-grid" id="task-${task.id}">
            <div class="task-content">
            <!-- Checkbox for marking task as done -->
            <input type="checkbox" 
                ${task.is_done ? "checked" : ""}
                class="task-checkbox"
                hx-post="/task/${task.id}/toggle"
                hx-trigger="change"
                hx-swap="none"
                hx-headers='{"X-CSRFToken": getCSRFToken()}'
                onchange="toggleTaskStyle(${task.id}, this.checked)">
            
            <!-- Task Title -->
            <div class="task-title" id="task-title-${task.id}" 
                 style="${
                   task.is_done ? "text-decoration: line-through;" : ""
                 }">
                ${task.title}
            </div>

            <!-- Hidden input for editing task title -->
            <input type="text" 
                class="edit-task-title" 
                id="edit-task-input-${task.id}" 
                name="title" 
                value="${task.title}"
                style="display: none;" 
                hx-post="/task/edit/${task.id}"
                hx-trigger="change, blur, keyup[key=='Enter']"
                hx-target="#task-${task.id}"
                hx-swap="outerHTML"
                hx-headers='{"X-CSRFToken": getCSRFToken()}'>
            </div>

            <div></div>

            <div class="icons-right">
                <div class="priority-controls">
                    <div class="icon" onclick="changePriority(${
                      task.id
                    }, 1)">🔼</div>
                    <div class="icon" onclick="changePriority(${
                      task.id
                    }, -1)">🔽</div>
                </div>

                <div class="icon">
                    <img src="${pencilIconPath}" 
                         alt="Edit Icon" 
                         height="20" 
                         onclick="enableTaskEdit('${task.id}')">
                </div>

                <div class="icon">
                    <img src="${deleteIconPath}" 
                         alt="Delete Icon" 
                         height="20"
                         hx-trigger="click"
                         hx-target="#task-${task.id}"
                         hx-swap="delete"
                         hx-headers='{"X-CSRFToken": getCSRFToken()}'
                         onclick="deleteTask('${task.id}')">
                </div>
            </div>
        </div>`;

        taskList.innerHTML += taskHtml;
      });
    })
    .catch((error) => console.error("Error fetching tasks:", error));
}

// Add this new function to handle the checkbox toggle styling
function toggleTaskStyle(taskId, isChecked) {
  const taskTitle = document.getElementById(`task-title-${taskId}`);
  if (taskTitle) {
    taskTitle.style.textDecoration = isChecked ? "line-through" : "none";
  }
}

function deleteTask(taskId) {
  console.log("Deleting Task ID:", taskId);

  const csrftoken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];

  fetch(`delete-task/${taskId}/`, {
    method: "POST", // Ensure this is POST
    headers: {
      "X-CSRFToken": csrftoken, // CSRF token required
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to delete task");
      }
      return response.text();
    })
    .then(() => {
      console.log("Task deleted successfully");
      document.getElementById(`task-${taskId}`).remove(); // Remove from UI
    })
    .catch((error) => {
      console.error("Error deleting task:", error);
      showAlert("Failed to delete task!", "error");
    });
}

// Function to move a task up in priority
function moveTaskUp(taskId) {
  fetch(`/move_task_up/${taskId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Refresh the task list after moving the task
        const dateString = document.getElementById("date-picker").value;
        fetchTasksForDate(dateString);
      }
    })
    .catch((error) => console.error("Error moving task up:", error));
}

// Function to move a task down in priority
function moveTaskDown(taskId) {
  fetch(`/move_task_down/${taskId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Refresh the task list after moving the task
        const dateString = document.getElementById("date-picker").value;
        fetchTasksForDate(dateString);
      }
    })
    .catch((error) => console.error("Error moving task down:", error));
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

function handleProjectCreated(response) {
  if (response.error) {
    alert(response.error);
    return;
  }
  fetchProjects();
  closeCalendarModal();
}
