var modalEditarTarefa = document.getElementById("ModalUpdateTask");
var closeModalEditBtn = document.getElementById("closeModalBtn");

closeModalEditBtn.addEventListener("click", function(){
    modalEditarTarefa.style.display = "none";
})

form_edit_tarefas = document.getElementById("formEditTask");

form_edit_tarefas.addEventListener("submit", function(event){
    event.preventDefault()
    var formData = new FormData();
    formData.append("task_id", id_tarefa_global);
    formData.append("new_task_type", form_edit_tarefas.elements[0].value);
    formData.append("new_task_description", form_edit_tarefas.elements[1].value);
    formData.append("new_task_date", form_edit_tarefas.elements[2].value);
    formData.append("new_task_status", 0);

    fetch("/update-task", {
        method: "PUT",
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        form.reset();
        location.reload();
    })
    
})

document.addEventListener('click', function (event) {

    const target = event.target;

    if (target.classList.contains('editar-tarefa')) {
        const tarefa = target.closest('.tarefa-caixa');
        var id_tarefa = tarefa.getAttribute("id_tarefa");
        // Torna a variável global
        window.id_tarefa_global = id_tarefa;
        
        // Mostra o form para editar a tarefa
        modalEditarTarefa.style.display = "block";
    }
});
