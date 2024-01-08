const form_signup = document.getElementById("form_signup");

form_signup.addEventListener("submit", function(event){
    event.preventDefault();

    formData = new FormData(form_signup);

    fetch("/auth.signup", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json());
});