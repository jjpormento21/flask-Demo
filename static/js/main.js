const navLinks = $(".nav-link");
const pageData = $("#page-data").data();

console.log(pageData);
$(navLinks[pageData.pageid]).addClass("active");

let today = new Date();
let element = document.getElementById("dateEdited");
element.value = today.toString();

function setPostToDelete(postId) {
    document.querySelector(".delete-post-btn").setAttribute("href", '/blog_post_delete/' + postId);
    console.log(postId);
}
