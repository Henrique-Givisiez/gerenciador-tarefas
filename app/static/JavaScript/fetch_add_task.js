form_add_task = document.getElementById("FormAddTask")

form_add_task.addEventListener("submit", function(event){
    event.preventDefault()
    var formData = new FormData(form_add_task);
    fetch("/create-task", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        form_add_task.reset();
    })
    
})
