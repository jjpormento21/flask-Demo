const navLinks = $(".nav-link");
const pageData = $("#page-data").data();

console.log(pageData);
$(navLinks[pageData.pageid]).addClass("active");
