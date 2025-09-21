// This section handles the form submission on post-job.html
document.addEventListener('DOMContentLoaded', () => {
    const jobForm = document.querySelector('.job-form');
    if (jobForm) {
        jobForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent the default form submission

            const jobData = {
                title: document.getElementById('job-title').value,
                company: document.getElementById('company').value,
                location: document.getElementById('location').value,
                description: document.getElementById('description').value
            };

            const responseMessage = document.getElementById('response-message');

            try {
                const response = await fetch('http://127.0.0.1:4567/api/jobs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(jobData)
                });

                if (response.ok) {
                    responseMessage.textContent = '✅ Job successfully posted!';
                    responseMessage.style.color = 'green';
                    jobForm.reset(); // Clear the form
                } else {
                    const errorText = await response.text();
                    responseMessage.textContent = '❌ Error posting job: ' + errorText;
                    responseMessage.style.color = 'red';
                }
            } catch (error) {
                responseMessage.textContent = '❌ Failed to connect to the server.';
                responseMessage.style.color = 'red';
                console.error('Network or server error:', error);
            }
        });
    }

    // This section is for fetching and displaying jobs on browse-job.html
    const jobList = document.getElementById("job-list");
    if (jobList) {
        fetch("http://127.0.0.1:4567/api/jobs") // Updated API endpoint
            .then(res => res.json())
            .then(data => {
                jobList.innerHTML = "";
                data.forEach(job => {
                    let div = document.createElement("div");
                    div.className = "job-card";
                    div.innerHTML = `
                        <h3>${job.title}</h3>
                        <p><strong>Company:</strong> ${job.company}</p>
                        <p><strong>Location:</strong> ${job.location || "Not specified"}</p>
                    `;
                    jobList.appendChild(div);
                });
            })
            .catch(err => console.error("Error fetching jobs:", err));
    }
});

function searchJobs() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let jobs = document.querySelectorAll(".job-card");
    jobs.forEach(job => {
        let text = job.innerText.toLowerCase();
        if (text.includes(input)) {
            job.style.display = "block";
        } else {
            job.style.display = "none";
        }
    });
}