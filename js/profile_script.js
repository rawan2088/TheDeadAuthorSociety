document.querySelector("form").onsubmit = function () {

  let email = document.getElementById("email").value.trim();
  let currentPass = document.getElementById("Cpass").value.trim();
  let newPass = document.getElementById("pass").value.trim();
  let userName = document.getElementById("user").value.trim();

  if (email === "" && currentPass === "" && newPass === "" && userName === "") {
    alert("Please fill at least one field to make changes!");
    return false;
  }


  if (email !== "" && !email.includes("@")) {
    alert("Invalid email!");
    return false;
  }

  if (currentPass !== "" && newPass === "") {
    alert("You must enter a new password to change it!");
    return false;
  }

  if (newPass !== "" && currentPass === "") {
    alert("You must enter your current password to change it!");
    return false;
  }

  if (newPass.length > 0 && newPass.length < 6) {
    alert("New password must be at least 6 characters");
    return false;
  }


  alert("Changes saved successfully!");
};