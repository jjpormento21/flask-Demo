const navLinks = $(".nav-link");
const pageData = $("#page-data").data();

console.log(pageData);
$(navLinks[pageData.pageid]).addClass("active");

let today = new Date();
var element = document.getElementById("dateEdited");
element.value = today.toString();
