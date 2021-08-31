const addComment = document.querySelector(".add-comment");
const addCommenForm = document.querySelector(".add-comment-form");
addCommenForm .style.display = "none";


$(addComment).click(function(e) {
    e.preventDefault();
    addComment.style.display = "none";
    addCommenForm.style.display = "block";
});