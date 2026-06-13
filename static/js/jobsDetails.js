import { getData } from "./utils/api.js";
const params = new URLSearchParams(window.location.search); // it's equal to useParam in React js
const jobId = params.get("id"); // equal to const [ id ] = useParam()

async function getAllDataFetch() {
  const res = await getData();
  console.log(res);
  return res;
}

const emptySpace = document.querySelector(".available-job-details");
async function getJobDetails() {
  const allJobs = await getAllDataFetch();

  const job = allJobs.find((j) => j.id == jobId);

  if (!job) {
    return console.error("Job not found!");
  }

  let childDiv = document.createElement("div");
  childDiv.className = "styleChildDiv";

  let titleData = document.createElement("h3");
  let companyData = document.createElement("p");
  let salaryData = document.createElement("h4");
  let timeData = document.createElement("h5");
  let hr = document.createElement("hr");
  let imgData = document.createElement("img");

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

  let descriptionData = document.createElement("div");
  descriptionData.className = "job-description";
  descriptionData.innerHTML = job.description;

  salaryData.innerText = `${job.salary}` || "Not specified";
  salaryData.className = "salary";

  let applyBtn = document.createElement("a");
  applyBtn.href = job.url;
  applyBtn.target = "_blank";
  applyBtn.innerText = "Apply Now";
  applyBtn.className = "apply-btn";

  childDiv.append(salaryData, descriptionData, applyBtn);

  emptySpace.appendChild(childDiv);
}

getJobDetails();
