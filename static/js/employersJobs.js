let currentStep = 1;

const jobForm = document.getElementById("jobForm");
const serverSubmit = jobForm && jobForm.dataset.serverSubmit === "true";

document.querySelectorAll(".nav-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const sectionId = this.getAttribute("data-section");
    if (sectionId === "jobs-list" && document.getElementById("jobs-list")) {
      showSection(sectionId);
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      const url = new URL(window.location.href);
      url.searchParams.delete("create");
      window.history.replaceState({}, "", url);
      return;
    }
    showSection(sectionId);
    document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
    this.classList.add("active");
    updateProgressFromSection(sectionId);
  });
});

function showSection(sectionId) {
  document.querySelectorAll(".content-section").forEach((section) => {
    section.classList.remove("active");
  });
  const section = document.getElementById(sectionId);
  if (section) {
    section.classList.add("active");
  }
  if (sectionId === "preview" || sectionId === "publish") {
    updatePreview();
  }
}

function updateProgressFromSection(sectionId) {
  if (sectionId === "details") {
    setCurrentStep(1);
  } else if (sectionId === "requirements") {
    setCurrentStep(2);
  } else if (sectionId === "preview" || sectionId === "publish") {
    setCurrentStep(3);
  }
}

function setCurrentStep(step) {
  currentStep = step;
  updateProgressUI();
}

function updateProgressUI() {
  document.querySelectorAll(".progress-step").forEach((stepEl) => {
    const stepNum = parseInt(stepEl.getAttribute("data-step"), 10);
    stepEl.classList.remove("active-step", "inactive-step");
    if (stepNum === currentStep) {
      stepEl.classList.add("active-step");
    } else {
      stepEl.classList.add("inactive-step");
    }
  });
}

function updatePreview() {
  const titleEl = document.getElementById("previewTitle");
  const companyEl = document.getElementById("previewCompany");
  const locationEl = document.getElementById("previewLocation");
  const typeEl = document.getElementById("previewType");
  const titleInput = document.getElementById("jobTitle");
  const companyInput = document.getElementById("companyName");
  const locationInput = document.getElementById("location");
  const typeInput = document.getElementById("jobType");

  if (titleEl && titleInput) {
    titleEl.textContent = titleInput.value.trim() || "Job Title";
  }
  if (companyEl && companyInput) {
    companyEl.textContent = companyInput.value.trim() || "Company Name";
  }
  if (locationEl && locationInput) {
    locationEl.textContent = locationInput.value.trim() || "Location";
  }
  if (typeEl && typeInput) {
    const label = typeInput.options[typeInput.selectedIndex];
    typeEl.textContent = label && label.value ? label.text : "Job Type";
  }
}

function validateJobForm() {
  const title = document.getElementById("jobTitle")?.value?.trim();
  const location = document.getElementById("location")?.value?.trim();
  const description = document.getElementById("description")?.value?.trim();
  const jobType = document.getElementById("jobType")?.value;

  if (!title || !location || !description || !jobType) {
    alert("Please fill in job title, location, job type, and description.");
    if (!title || !location || !jobType) {
      showSection("details");
      document.querySelector('[data-section="details"]')?.classList.add("active");
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      document.querySelector('[data-section="details"]')?.classList.add("active");
    } else {
      showSection("requirements");
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      document.querySelector('[data-section="requirements"]')?.classList.add("active");
    }
    return false;
  }
  return true;
}

if (jobForm) {
  if (serverSubmit) {
    jobForm.addEventListener("submit", function (e) {
      if (!validateJobForm()) {
        e.preventDefault();
      }
    });

    ["jobTitle", "location", "jobType", "description", "skills"].forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("input", updatePreview);
        el.addEventListener("change", updatePreview);
      }
    });

    const params = new URLSearchParams(window.location.search);
    if (params.get("create") === "1") {
      showSection("details");
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      document.querySelector('[data-section="details"]')?.classList.add("active");
      setCurrentStep(1);
    }
  } else {
    jobForm.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("Job saved locally (demo mode).");
    });
  }
}

const nextStepBtn = document.getElementById("nextStepBtn");
if (nextStepBtn) {
  nextStepBtn.addEventListener("click", function () {
    const sections = ["details", "requirements", "publish"];
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
      const targetSection = sections[currentStep - 1];
      showSection(targetSection);
      document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
      document.querySelector(`[data-section="${targetSection}"]`)?.classList.add("active");
    }
  });
}

const nextStepBtn2 = document.getElementById("nextStepBtn2");
if (nextStepBtn2) {
  nextStepBtn2.addEventListener("click", function () {
    if (currentStep < 3) {
      setCurrentStep(3);
    }
    showSection("publish");
    document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
    document.querySelector('[data-section="publish"]')?.classList.add("active");
  });
}

updatePreview();
