var modalEditarTarefa = document.getElementById("modalEditarTarefa");
var closeModalEditBtn = document.getElementById("closeModalEditBtn");

closeModalEditBtn.addEventListener("click", function(){
    modalEditarTarefa.style.display = "none";
})

document.getElementById("form_editar_tarefas").addEventListener("submit", function(event){
    event.preventDefault()
    form_edit_tarefas = document.getElementById("form_editar_tarefas");
    var formData = new FormData(form_edit_tarefas);
    formData.append("id_tarefa_editada", id_tarefa_global);
    // Recebe os dados JSON
    fetch("/editar-tarefa", {
        method: "POST",
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
