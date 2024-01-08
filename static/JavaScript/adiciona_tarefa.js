// Adiciona um listener pra um submit do form 'form_tarefas'
document.getElementById("form_tarefas").addEventListener("submit", function(event){
    // Impede a ação padrão do evento submit
    event.preventDefault()

    // Busca o form de adicionar a tarefa pelo id
    form_add_tarefas = document.getElementById("form_tarefas");

    // Cria um objeto formData para definir pares chave/valor com os valores do formulário
    var formData = new FormData(form_add_tarefas);

    // Recebe os dados JSON chamando a função no backend pela rota "adiciona-tarefa"
    fetch("/adiciona-tarefa", {
        method: "POST",    // Define um request method via POST
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        // Chama a função "tarefasUI" para tratar os dados e exibi-los na UI
        tarefasUI(dado.categoria, dado.descricao, dado.data, dado.ID);

        // Reseta os campos do formulário 
        form_add_tarefas.reset();

        // Recarrega a página
        location.reload();
    })
})
