export class Calendar {
  constructor() {
    this.DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    this.MONTH_NAMES = [
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
    this.currentDate = new Date();
    this.projects = [];
  }

  initCalendar() {
    document.getElementById("weekdays").innerHTML = this.DAYS.map(
      (day) => `<div class="weekday">${day}</div>`
    ).join("");
    this.updateCalendar();
    this.fetchProjects();
  }

  updateCalendar() {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();

    document.getElementById(
      "current-month"
    ).textContent = `${this.MONTH_NAMES[month]} ${year}`;

    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let daysHtml = "";

    for (let i = 0; i < firstDayOfMonth; i++) {
      daysHtml += `<div class="calendar-day blank"></div>`;
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(Date.UTC(year, month, day));
      const formattedDate = this.formatDate(date);
      const hasProject = this.projects.includes(formattedDate);

      daysHtml += `
        <div class="calendar-day ${hasProject ? "has-project" : ""}"
             data-date="${formattedDate}"
             onclick="main.calendar.selectDate('${formattedDate}')">
            ${day}
        </div>`;
    }

    document.getElementById("calendar-days").innerHTML = daysHtml;
  }

  fetchProjects() {
    const month = this.currentDate.getMonth() + 1;
    const year = this.currentDate.getFullYear();

    fetch(`/project_dates/?month=${month}&year=${year}`)
      .then((response) => response.json())
      .then((data) => {
        this.projects = data;
        this.updateCalendar();
      })
      .catch((error) => console.error("Error fetching projects:", error));
  }

  selectDate(dateString) {
    document
      .querySelectorAll(".calendar-day.selected")
      .forEach((el) => el.classList.remove("selected"));

    const selectedDay = document.querySelector(`[data-date='${dateString}']`);
    if (selectedDay) {
      selectedDay.classList.add("selected");
    }

    document.getElementById("project-form").style.display = "block";
    document.getElementById("selected-date").value = dateString;

    main.taskManager.fetchTasksForDate(dateString);
  }

  formatDate(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
      2,
      "0"
    )}-${String(date.getDate()).padStart(2, "0")}`;
  }

  previousMonth() {
    this.currentDate.setMonth(this.currentDate.getMonth() - 1);
    this.updateCalendar();
    this.fetchProjects();
  }

  nextMonth() {
    this.currentDate.setMonth(this.currentDate.getMonth() + 1);
    this.updateCalendar();
    this.fetchProjects();
  }

  openCalendarModal() {
    document.getElementById("calendar-modal").style.display = "flex";
    this.initCalendar();
  }

  closeCalendarModal() {
    document.getElementById("calendar-modal").style.display = "none";
    document.getElementById("project-form").style.display = "none";
    document.getElementById("project-title").value = "";
  }
}
