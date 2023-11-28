document.getElementById("form_tarefas").addEventListener("submit", function(event){
    event.preventDefault()
    form_add_tarefas = document.getElementById("form_tarefas");
    var formData = new FormData(form_add_tarefas);
    // Recebe os dados JSON
    fetch("/adiciona-tarefa", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        funcAdicionaTarefas(dado);
        form_add_tarefas.reset();
        location.reload();
    })
    
})
function funcAdicionaTarefas(dado) {
    var div_pendentes_content = document.getElementById("pendentes-content");
    if (div_pendentes_content){
        tarefasUI(dado.categoria, dado.descricao, dado.data, dado.ID);
    }
}