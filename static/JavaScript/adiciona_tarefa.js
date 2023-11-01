document.getElementById("form_tarefas").addEventListener("submit", function(event){
    event.preventDefault()
    var formData = new FormData(document.getElementById("form_tarefas"));
    // Recebe os dados JSON
    fetch("/adiciona-tarefa", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        funcAdicionaTarefas(dado);
    })
    
})
function funcAdicionaTarefas(dado) {
    var div_pendentes_content = document.getElementById("pendentes-content");
    if ((div_pendentes_content.getElementsByClassName("tarefa-caixa").length)<4){
        tarefasUI(dado.categoria, dado.descricao, dado.data, dado.ID);
    }
}