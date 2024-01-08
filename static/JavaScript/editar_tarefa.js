// Busca o modal de editar a tarefa e guarda em uma varíavel
var modalEditarTarefa = document.getElementById("modalEditarTarefa");

// Busca o botão de fechar o modal de editar a tarefa e guarda em uma variável
var closeModalEditBtn = document.getElementById("closeModalEditBtn");

// Busca o formulário 'form_editar_tarefas' e guarda em uma varíavel
form_edit_tarefas = document.getElementById("form_editar_tarefas");

// Adiciona um listener para o 'closeModalEditBtn' para fechar o modal de editar tarefa
closeModalEditBtn.addEventListener("click", function(){
    modalEditarTarefa.style.display = "none";
})


// Adiciona um listener para o 'form_edit_tarefas' quando submetido
form_edit_tarefas.addEventListener("submit", function(event){
    // Impede a ação padrão do evento submit
    event.preventDefault()

    // Cria um objeto formData para definir pares chaves/valor com os valores do formulário
    var formData = new FormData(form_edit_tarefas);

    // Adiciona o id da tarefa a ser editada ao objeto 
    formData.append("id_tarefa_editada", id_tarefa_global);

    // Recebe os dados JSON
    fetch("/editar-tarefa", {
        method: "POST", // Define um request method via POST
        body: formData
    })
    .then(response => response.json())
    .then(dado => {
        // Reseta os campos do formulário
        form.reset();

        // Recarrega a página
        location.reload();
    })
    
})


// Adiciona um listener para um clique qualquer
document.addEventListener('click', function (event) {

    // Mapeia o alvo do evento
    const target = event.target;

    // Verifica se o target contém a div para editar a tarefa com classe "editar-tarefa"
    if (target.classList.contains('editar-tarefa')) {
        // Busca a "caixa" da tarefa e guarda o id dela 
        const tarefa = target.closest('.tarefa-caixa');
        var id_tarefa = tarefa.getAttribute("id_tarefa");
        // Torna a variável global
        window.id_tarefa_global = id_tarefa;
        
        // Mostra o form para editar a tarefa
        modalEditarTarefa.style.display = "block";
    }
});

