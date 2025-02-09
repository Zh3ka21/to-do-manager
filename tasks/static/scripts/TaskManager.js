export class TaskManager {
  constructor() {
    this.initTaskForm();
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

        const projectId = document.getElementById("projectID");
        const projectNamePlaceholder = document.getElementById(
          "project-name-placeholder"
        );

        if (projectNamePlaceholder && data.context && data.context.project) {
          projectNamePlaceholder.innerText = data.context.project.name;
          projectId.value = data.context.project.id;
        }

        if (data.context.tasks.length === 0) {
          taskList.innerHTML = "<p>No tasks for this day.</p>";
          return;
        }

        data.context.tasks.sort((a, b) => a.priority - b.priority);
        data.context.tasks.forEach((task) => {
          const taskHtml = `
            <div class="task-grid" id="task-${task.id}">
              <div class="task-content">
                <input type="checkbox" 
                    ${task.is_done ? "checked" : ""}
                    class="task-checkbox"
                    hx-post="/task/${task.id}/toggle"
                    hx-trigger="change"
                    hx-swap="none"
                    hx-headers='{"X-CSRFToken": main.getCSRFToken()}'
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
                    hx-post="/task/edit/${task.id}"
                    hx-trigger="change, blur, keyup[key=='Enter']"
                    hx-target="#task-${task.id}"
                    hx-swap="outerHTML"
                    hx-headers='{"X-CSRFToken": main.getCSRFToken()}'>
              </div>
              <div></div>
              <div class="icons-right">
                <div class="priority-controls">
                  <div class="icon" onclick="main.taskManager.changePriority(${
                    task.id
                  }, 1)">
                  🔼
                  </div>
                  <div class="icon" onclick="main.taskManager.changePriority(${
                    task.id
                  }, -1)">
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
                      hx-headers='{"X-CSRFToken": main.getCSRFToken()}'
                      onclick="main.taskManager.deleteTask('${task.id}')">
                </div>
              </div>
            </div>
          `;
          taskList.innerHTML += taskHtml;
        });
      })
      .catch((error) => console.error("Error fetching tasks:", error));
  }

  toggleTaskStyle(taskId, isChecked) {
    const taskTitle = document.getElementById(`task-title-${taskId}`);
    if (taskTitle) {
      taskTitle.style.textDecoration = isChecked ? "line-through" : "none";
    }
  }

  deleteTask(taskId) {
    const csrftoken = main.getCSRFToken();

    fetch(`delete-task/${taskId}/`, {
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

  changePriority(taskId, delta) {
    fetch(`/move_task_${delta > 0 ? "up" : "down"}/${taskId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": main.getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const dateString = document.getElementById("date-picker").value;
          this.fetchTasksForDate(dateString);
        }
      })
      .catch((error) => console.error("Error changing task priority:", error));
  }
}
