document.querySelector("form").onsubmit = function () {
    
    
  let bookID = document.getElementById("num").value.trim();
  let bookName = document.getElementById("name").value.trim();
  let author = document.getElementById("auth").value.trim();
  let category = document.getElementById("cat").value.trim();

 
  if (bookID === "" || bookName === "" || author === "" || category === "") {
    alert("Please fill all required fields before adding the book!");
    return false; 
  }

  alert("Book added successfully!");
};