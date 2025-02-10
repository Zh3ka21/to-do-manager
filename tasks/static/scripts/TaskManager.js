console.log("Htmx is okay:", typeof htmx !== "undefined");

export class TaskManager {
  constructor() {
    this.initTaskForm();

    document.addEventListener("htmx:beforeRequest", function (evt) {
      console.log("HTMX Request about to be sent:", evt.detail);
    });

    document.addEventListener("htmx:afterRequest", function (evt) {
      console.log("HTMX Request completed:", evt.detail);
    });

    document.addEventListener("htmx:configRequest", function (evt) {
      console.log("HTMX Request configured:", evt.detail);
    });
  }

  getCSRFToken() {
    const csrfCookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="));
    return csrfCookie ? csrfCookie.split("=")[1] : null;
  }

  refreshTaskList() {
    const selectedDate = document.getElementById("selected-date").value;
    this.fetchTasksForDate(selectedDate);
  }

  initTaskForm() {
    const taskForm = document.getElementById("task-form");
    if (taskForm) {
      taskForm.addEventListener("htmx:afterRequest", () => {
        console.log("Form submitted, clearing inputs.");
        document.getElementById("new-task").value = "";
        document.getElementById("deadline-time").value = "";
      });
    }
  }

  enableTaskEdit(taskId) {
    const titleElement = document.getElementById(`task-title-${taskId}`);
    const inputElement = document.getElementById(`edit-task-input-${taskId}`);

    if (!titleElement || !inputElement) {
      console.error("Elements not found for Task ID:", taskId);
      return;
    }

    titleElement.style.display = "none";
    inputElement.style.display = "block";
    inputElement.focus();
    inputElement.select();

    inputElement.dataset.originalValue = inputElement.value;

    inputElement.addEventListener("keyup", (e) => {
      if (e.key === "Enter") {
        this.submitEdit(taskId, inputElement.value);
        console.log("Submitted");
      } else if (e.key === "Escape") {
        this.cancelEdit(taskId);
        console.log("Canceled");
      }
    });

    inputElement.addEventListener("blur", () => {
      this.submitEdit(taskId, inputElement.value);
    });
  }

  submitEdit(taskId, newValue) {
    const titleElement = document.getElementById(`task-title-${taskId}`);
    const inputElement = document.getElementById(`edit-task-input-${taskId}`);

    const csrftoken = main.getCSRFToken();

    console.log(titleElement);
    console.log(inputElement);

    fetch(`/task/edit/${taskId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrftoken,
      },
      body: `title=${encodeURIComponent(newValue)}`,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.text();
      })
      .then(() => {
        titleElement.textContent = newValue; // Update the title text
        titleElement.style.display = "block"; // Show the title
        inputElement.style.display = "none"; // Hide the input
        main.showAlert("Task updated successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
        main.showAlert("Failed to update task!", "error");
        this.cancelEdit(taskId);
      });
  }

  cancelEdit(taskId) {
    const titleElement = document.getElementById(`task-title-${taskId}`);
    const inputElement = document.getElementById(`edit-task-input-${taskId}`);

    if (!titleElement || !inputElement) {
      console.error("Elements not found for Task ID:", taskId);
      return;
    }

    if (inputElement.dataset.originalValue) {
      inputElement.value = inputElement.dataset.originalValue;
    }

    titleElement.style.display = "block";
    inputElement.style.display = "none";
  }

  fetchTasksForDate(dateString) {
    fetch(`/get_tasks_for_date/?date=${dateString}`)
      .then((response) => response.json())
      .then((data) => {
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";

        const projectIdInput = document.getElementById("projectID");
        const projectNamePlaceholder = document.getElementById(
          "project-name-placeholder"
        );

        if (data.context && data.context.project) {
          const project = data.context.project;

          // Update project ID and project name only if they are present
          projectIdInput.value = project.id || ""; // Ensure empty value if project ID is not available
          if (projectNamePlaceholder) {
            projectNamePlaceholder.innerText =
              project.name || "No project selected"; // Fallback to default text
          }
        } else {
          // If no project data, reset values to default
          projectIdInput.value = "";
          if (projectNamePlaceholder) {
            projectNamePlaceholder.innerText = "No project selected";
          }
        }

        // Handle tasks
        if (data.context && data.context.tasks.length > 0) {
          data.context.tasks.sort((a, b) => a.priority - b.priority);
          console.log(data.context.tasks);

          data.context.tasks.forEach((task) => {
            if (!task.id) {
              console.error("Missing task ID:", task);
              return;
            }
            console.log("Current taks id: ", task.id);

            const taskHtml = `
            <div class="task-grid" id="task-${task.id}">
              <div class="task-content">
                <input type="checkbox" 
                  ${task.is_done ? "checked" : ""}
                  class="task-checkbox"
                  hx-post="/task/${task.id}/toggle/"
                  hx-trigger="change"
                  hx-swap="outerHTML"
                  hx-target="#task-${task.id}"
                  hx-headers='{"X-CSRFToken": "${this.getCSRFToken()}"}'
                  onchange="main.taskManager.toggleTaskStyle(${
                    task.id
                  }, this.checked)">
                  
                <div class="task-title" id="task-title-${task.id}" 
                    style="${
                      task.is_done ? "text-decoration: line-through;" : ""
                    }">
                  ${task.title}
                </div>


                <input type="text" 
                    class="edit-task-title" 
                    id="edit-task-input-${task.id}" 
                    name="title" 
                    value="${task.title}"
                    style="display: none;" 
                    hx-post="/task/edit/${task.id}/"
                    hx-trigger="change, blur, keyup[key=='Enter']"
                    hx-target="#task-${task.id}"
                    hx-swap="outerHTML"
                    hx-headers='{"X-CSRFToken": main.getCSRFToken()}'>
              </div>
              <div></div>
              <div class="icons-right">
                <div class="priority-controls">
                  <div class="icon"
                   onclick="main.taskManager.changePriority(${
                     task.id
                   }, 'up')"> 🔼
                  </div>
                  <div class="icon" 
                  onclick="main.taskManager.changePriority(${task.id}, 'down')">
                  🔽
                  </div>
                </div>
                <div class="icon">
                  <img src="${pencilIconPath}" alt="Edit Icon" height="20" 
                      onclick="main.taskManager.enableTaskEdit('${task.id}')">
                </div>
                <div class="icon">
                  <img src="${deleteIconPath}" alt="Delete Icon" height="20"
                      hx-trigger="click"
                      hx-target="#task-${task.id}"
                      hx-swap="delete"
                      hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
                      onclick="main.taskManager.deleteTask('${task.id}')">
                </div>
              </div>
            </div>
          `;
            taskList.innerHTML += taskHtml;
            htmx.process(taskList); // Add this line to process new content
          });
        }
      })
      .catch((error) => console.error("Error fetching tasks:", error));
  }

  toggleTaskStyle(taskId, isChecked) {
    console.log("Toggle called:", taskId, isChecked);
    const taskTitle = document.getElementById(`task-title-${taskId}`);
    if (taskTitle) {
      taskTitle.style.textDecoration = isChecked ? "line-through" : "none";
    }
  }

  deleteTask(taskId) {
    const csrftoken = main.getCSRFToken();

    fetch(`delete_task/${taskId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete task");
        return response.text();
      })
      .then(() => {
        document.getElementById(`task-${taskId}`).remove();
      })
      .catch((error) => {
        console.error("Error deleting task:", error);
        main.showAlert("Failed to delete task!", "error");
      });
  }

  changePriority(taskId, direction) {
    fetch(`/move_task/${taskId}/${direction}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": main.getCSRFToken(),
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.refreshTaskList(); // Reloads tasks after moving
        } else {
          console.error("Error moving task:", data.error);
        }
      })
      .catch((error) => console.error("Request failed:", error));
  }
}
