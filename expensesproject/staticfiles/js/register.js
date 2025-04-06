console.log("Register page loaded!");

document.getElementById("togglePassword").addEventListener("click", function () {
  let passwordField = document.getElementById("passwordfield");
  if (passwordField.type === "password") {
    passwordField.type = "text";
    this.innerText = "Hide";
  } else {
    passwordField.type = "password";
    this.innerText = "Show";
  }
});

const usernameField = document.querySelector("#usernamefield");
const feedBackField = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailfield");
const emailFeedbackField = document.querySelector(".email-feedback-field");
const submitBtn = document.querySelector(".submit-btn");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;
  console.log("Email entered:", emailVal);

  emailField.classList.remove("is-invalid");
  emailFeedbackField.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email/", {
      method: "POST",
      body: JSON.stringify({ email: emailVal }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      }
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedbackField.style.display = "block";
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  console.log("Username entered:", usernameVal);

  usernameField.classList.remove("is-invalid");
  feedBackField.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username/", {
      method: "POST",
      body: JSON.stringify({ username: usernameVal }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      }
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          feedBackField.style.display = "block";
          feedBackField.innerHTML = `<p>${data.username_error}</p>`;
          submitBtn.disabled = true;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

// Function to get CSRF token from meta tag
function getCSRFToken() {
  return document.querySelector("meta[name='csrf-token']").getAttribute("content");
}
