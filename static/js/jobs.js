import { getData } from "./utils/api.js";
async function getAllDataFetch() {
  const res = await getData();
  console.log(res);
  return res;
}

const emptySpace = document.querySelector(".available-job");
async function addingDataToDOM() {
  let getJobs = await getAllDataFetch();
  if (!getJobs) {
    return console.error("No data found!");
  }
  getJobs.forEach((job) => {
    let childDiv = document.createElement("div");
    childDiv.className = "styleChildDiv";

    let titleData = document.createElement("h3");
    let companyData = document.createElement("p");
    let salaryData = document.createElement("h4");
    let timeData = document.createElement("h5");
    let hr = document.createElement("hr");
    let imgData = document.createElement("img");
    let btnDetails = document.createElement("button");

    let innerDivImgTime = document.createElement("div");
    innerDivImgTime.className = "card-header";
    imgData.src = `${job.company_logo}` || "";
    imgData.className = "company-logo";
    timeData.innerText = `${job.job_type}`;

    innerDivImgTime.appendChild(imgData);
    innerDivImgTime.appendChild(timeData);
    childDiv.appendChild(innerDivImgTime);

    let innerDivTitleCompany = document.createElement("div");
    titleData.innerText = `${job.category}`;
    companyData.innerText = `${job.company_name} - ${
      job.candidate_required_location
    }`;
    timeData.style.color = "gray";
    innerDivTitleCompany.appendChild(titleData);
    innerDivTitleCompany.appendChild(companyData);
    childDiv.appendChild(innerDivTitleCompany);

    childDiv.appendChild(hr);

    let innerDivSalaryBtn = document.createElement("div");
    innerDivSalaryBtn.className = "salary-btn";

    salaryData.innerText = `${job.salary}` || "Not specified";
    salaryData.className = "salary";
    btnDetails.className = "btnDetails";
    btnDetails.innerText = "Show Details";

    innerDivSalaryBtn.append(salaryData);
    innerDivSalaryBtn.append(btnDetails);
    childDiv.appendChild(innerDivSalaryBtn);

    btnDetails.addEventListener("click", () => {
      window.location.href = `/job-details.html?id=${job.id}`; // it's equal to useNavigate and Dynamic Routing( /details/:id)
    });

    emptySpace.appendChild(childDiv);
  });
}
let inputSearch = document.querySelector(".search-input");
let btnSearch = document.querySelector(".btnSearch");

// console.log(inputSearch.value);

// console.log(filterJob);
btnSearch.addEventListener("click", async (e) => {
  let getJobs = await getAllDataFetch();
  if (!getJobs) {
    return console.error("No data found!");
  }
  // console.log(getJobs);
  let filterJob = getJobs.filter((jobs) => {
    return jobs.category === inputSearch.value;
  });
  console.log(filterJob);
  emptySpace.innerHTML = "";
  filterJob.forEach((job) => {
    let childDiv = document.createElement("div");

    childDiv.className = "styleChildDiv";

    let titleData = document.createElement("h3");
    let companyData = document.createElement("p");
    let salaryData = document.createElement("h4");
    let timeData = document.createElement("h5");
    let hr = document.createElement("hr");
    let imgData = document.createElement("img");
    let btnDetails = document.createElement("button");

    let innerDivImgTime = document.createElement("div");
    innerDivImgTime.className = "card-header";
    imgData.src = `${job.company_logo}` || "";
    imgData.className = "company-logo";
    timeData.innerText = `${job.job_type}`;

    innerDivImgTime.appendChild(imgData);
    innerDivImgTime.appendChild(timeData);
    childDiv.appendChild(innerDivImgTime);

    let innerDivTitleCompany = document.createElement("div");
    titleData.innerText = `${job.category}`;
    companyData.innerText = `${job.company_name} - ${
      job.candidate_required_location
    }`;
    timeData.style.color = "gray";
    innerDivTitleCompany.appendChild(titleData);
    innerDivTitleCompany.appendChild(companyData);
    childDiv.appendChild(innerDivTitleCompany);

    childDiv.appendChild(hr);

    let innerDivSalaryBtn = document.createElement("div");
    innerDivSalaryBtn.className = "salary-btn";

    salaryData.innerText = `${job.salary}` || "Not specified";
    salaryData.className = "salary";
    btnDetails.className = "btnDetails";
    btnDetails.innerText = "Show Details";

    innerDivSalaryBtn.append(salaryData);
    innerDivSalaryBtn.append(btnDetails);
    childDiv.appendChild(innerDivSalaryBtn);

    btnDetails.addEventListener("click", () => {
      window.location.href = `/job-details.html?id=${job.id}`; // it's equal to useNavigate and Dynamic Routing( /details/:id)
    });

    emptySpace.appendChild(childDiv);
  });
});

document.addEventListener("DOMContentLoaded", () => {
  addingDataToDOM();
  console.log(`${location.pathname}/1`);
});
