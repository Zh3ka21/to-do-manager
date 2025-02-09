export class ProjectManager {
  constructor() {
    this.initProjectForm();
  }

  initProjectForm() {
    const calendarIcon = document.getElementById("calendar-icon");
    if (calendarIcon) {
      calendarIcon.addEventListener("click", () =>
        main.calendar.openCalendarModal()
      );
    }

    const calendarButton = document.querySelector("[data-calendar-trigger]");
    if (calendarButton) {
      calendarButton.addEventListener("click", () =>
        main.calendar.openCalendarModal()
      );
    }
  }

  enableProjectEdit(projectId) {
    const titleElement = document.getElementById("project-name-placeholder");
    const inputElement = document.getElementById("edit-project-input");

    if (!titleElement || !inputElement) {
      console.error("Elements not found for project");
      return;
    }

    const current_project_id = document.getElementById("projectID").value;
    inputElement.value = titleElement.innerText.trim();
    inputElement.dataset.originalValue = inputElement.value;

    titleElement.style.display = "none";
    inputElement.style.display = "inline";
    inputElement.focus();
    inputElement.select();

    inputElement.addEventListener("keyup", (e) => {
      if (e.key === "Enter") {
        this.submitProjectEdit(current_project_id, inputElement.value);
      } else if (e.key === "Escape") {
        this.cancelProjectEdit();
      }
    });

    inputElement.addEventListener("blur", () => {
      this.submitProjectEdit(current_project_id, inputElement.value);
    });
  }

  submitProjectEdit(projectId, newValue) {
    const csrftoken = main.getCSRFToken();

    fetch(`/update_project_name/${projectId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrftoken,
      },
      body: `name=${encodeURIComponent(newValue)}`,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.text();
      })
      .then(() => {
        const projectElement = document.getElementById(
          "project-name-placeholder"
        );
        const inputElement = document.getElementById("edit-project-input");

        if (!projectElement || !inputElement) {
          console.error("Elements not found for project");
          return;
        }

        projectElement.innerText = newValue;
        projectElement.style.display = "inline";
        inputElement.style.display = "none";

        main.showAlert("Project updated successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
        main.showAlert("Failed to update project!", "error");
        this.cancelProjectEdit();
      });
  }

  cancelProjectEdit() {
    const titleElement = document.getElementById("project-name-placeholder");
    const inputElement = document.getElementById("edit-project-input");

    if (!titleElement || !inputElement) {
      console.error("Elements not found for project");
      return;
    }

    if (inputElement.dataset.originalValue) {
      inputElement.value = inputElement.dataset.originalValue;
    }

    titleElement.style.display = "block";
    inputElement.style.display = "none";
  }

  deleteProject() {
    const projectId = document.getElementById("projectID");

    const csrftoken = main.getCSRFToken();

    fetch(`soft_delete_project/${projectId.value}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete project");
        return response.text();
      })
      .then(() => {
        main.calendar.openCalendarModal();
      })
      .catch((error) => {
        console.error("Error deleting project:", error);
        main.showAlert("Failed to delete project!", "error");
      });
  }
}
