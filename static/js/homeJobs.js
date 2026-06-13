import { getData } from "./utils/api.js";

const container = document.querySelector(".latest-jobs");

async function loadHomeJobs() {
    if (!container) return;

    const jobs = await getData();
    if (!jobs) return;

    container.innerHTML = "";

    jobs.slice(0, 9).forEach((job) => {
        const card = document.createElement("div");
        card.className = "latest-job-card";

        card.innerHTML = `
        <div class="company-logo-container">
            ${
            job.company_logo
                ? `<img src="${job.company_logo}" alt="logo">`
                : `<span>Logo</span>`
        }
        </div>

        <div class="job-card-header">
            <a href="/job-details.html?id=${job.id}">
                <h3 class="job-card-title">${job.title}</h3>
            </a>
        </div>

        <div class="latest-job-description">

            <div class="job-company-name">
                <i class="fa-solid fa-building"></i>
                <h5>${job.company_name}</h5>
            </div>

            <div class="job-company-location">
                <i class="fas fa-location-dot"></i>
                <h5>${job.candidate_required_location}</h5>
            </div>

            <div class="latest-job-time">
                <i class="fa-solid fa-clock"></i>
                <h5>${new Date(job.publication_date).toLocaleDateString()}</h5>
            </div>

            <div class="latest-job-sallary">
                <i class="fa-solid fa-dollar-sign"></i>
                <h5>${job.salary || "Not specified"}</h5>
            </div>

        </div>
    `;

        container.appendChild(card);
    });
}

document.addEventListener("DOMContentLoaded", loadHomeJobs);