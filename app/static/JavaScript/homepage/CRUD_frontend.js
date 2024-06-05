// Definição das funções que irão criar, ler, atualizar ou deletar as tarefas


// --------------------- CREATE TASKS --------------------- //
// Função que irá criar as tarefas
const form_add_task = document.getElementById("FormAddTask");
form_add_task.addEventListener("submit", function adicionarTarefa(event){
    
    event.preventDefault();

    let formData = new FormData(form_add_task); // Cria um objeto com o construtor FormData pra enviar os dados do formulário

    
    fetch("/create-task", { // Requisição com o endpoint create-task para adicionar a tarefa
        method: "POST",
        body: formData 
    })
    .then(response => {
        return response.json(); // Retorna a promessa para ser tratada no próximo then
    })    
    .then(data => {
        if (data.success != true){
            showAlert(data.success, data.status);
        } else{
            form_add_task.reset(); // Reseta o formulário
            location.reload();            
        }
    })
})

// --------------------- READ TASKS --------------------- //
// Esse trecho de código irá ler as tarefas e exibi-las na homepage
fetch('/homepage/read-tasks') // Faz uma solicitação no endpoint "/homepage/read-tasks" e recebe as tarefas retornadas como dados 
.then(response => response.json())
.then(dado => {
    for (const chave in dado) {
        const tarefa = dado[chave];
        showTasks(tarefa); // Função que irá exibir as tarefas na homepage
    }
});

// Função que exibe as tarefas
function showTasks (dado) {
    const div_status_content = document.getElementById(`${dado[5]}Content`); // Pega o status da tarefa e busca a coluna a qual ela pertence

    // Cria os elementos necessários para a caixa da tarefa
    var div_task_box = document.createElement("div");
    var div_task_header = document.createElement("div")
    var div_task_content = document.createElement("div");
    var div_task_footer = document.createElement("div");
    var h5_header = document.createElement("h5");
    var p_content = document.createElement("p");
    var span_footer = document.createElement("span");   
    
    // Criação dos elementos necessários para o menu dropdown 
    var dropdownDiv = document.createElement('div');
    dropdownDiv.className = 'dropdown';

    var button = document.createElement('button');
    button.className= 'menu';
    
    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.setAttribute("width", "16");
    svgElement.setAttribute("height", "15");
    svgElement.setAttribute("fill", "currentColor");
    svgElement.setAttribute("class", "bi bi-list");
    svgElement.setAttribute("viewBox", "0 0 16 16");
    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d", "M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5");
    svgElement.appendChild(pathElement);

    var dropdownContentDiv = document.createElement('div');
    dropdownContentDiv.id = 'myDropdown';
    dropdownContentDiv.className = 'dropdown-content';
    
    button.appendChild(svgElement);
    button.onclick = function(){
        toggleDropdown(button);
    };
    
    // Botões que irão mudar o status da tarefa  
    var muda_para_pendente = document.createElement('button');
    muda_para_pendente.id = 'muda_pendente';
    muda_para_pendente.className = 'move-tarefa';
    muda_para_pendente.textContent = 'Alterar para pendente';
    muda_para_pendente.setAttribute("data-destino","pending"); // Atributo que irá retornar o destino (pending) da tarefa
    
    var muda_para_progresso = document.createElement('button');
    muda_para_progresso.id = 'muda_progresso';
    muda_para_progresso.className = 'move-tarefa';
    muda_para_progresso.textContent = 'Alterar para em progresso';
    muda_para_progresso.setAttribute("data-destino","InProgress"); // Atributo que irá retornar o destino (InProgress) da tarefa
    
    var muda_para_concluida = document.createElement('button');
    muda_para_concluida.id = 'muda_concluida';
    muda_para_concluida.className = 'move-tarefa';
    muda_para_concluida.textContent = 'Alterar para concluida';
    muda_para_concluida.setAttribute("data-destino","Completed"); // Atributo que irá retornar o destino (Completed) da tarefa
    
    // Criação do botão para atualizar a tarefa com novas informações
    var editar_tarefa = document.createElement("button");
    editar_tarefa.id = "editar_tarefa";
    editar_tarefa.className = "editar-tarefa";
    editar_tarefa.textContent = "Editar tarefa";
    
    // Criação do botão que irá excluir a tarefa
    var excluir_tarefa = document.createElement("button");
    excluir_tarefa.id = "excluir_tarefa";
    excluir_tarefa.className = "excluir-tarefa";
    excluir_tarefa.textContent = "Exclua a tarefa";
    
    div_task_box.setAttribute("status", dado[5]) // Pega o status da tarefa e atribui a task box
    
    dropdownContentDiv.appendChild(muda_para_pendente);
    dropdownContentDiv.appendChild(muda_para_progresso);
    dropdownContentDiv.appendChild(muda_para_concluida);
    dropdownContentDiv.appendChild(editar_tarefa);
    dropdownContentDiv.appendChild(excluir_tarefa);
    dropdownDiv.appendChild(button);
    
    dropdownDiv.appendChild(dropdownContentDiv);
    
    // Adiciona as informações da tarefa aos elementos
    h5_header.innerHTML = dado[2];
    p_content.innerHTML = dado[3];
    span_footer.innerHTML = dado[4];
    
    div_task_header.appendChild(h5_header);
    div_task_header.appendChild(dropdownDiv);

    div_task_content.appendChild(p_content);

    div_task_footer.appendChild(span_footer);


    div_task_box.appendChild(div_task_header);
    div_task_box.appendChild(div_task_content);
    div_task_box.appendChild(div_task_footer);
    div_task_box.setAttribute("id_tarefa", dado[0]);

    div_status_content.appendChild(div_task_box); // Aloca a tarefa na sua respectiva coluna 
    
    div_task_box.classList.add("tarefa-caixa");
    div_task_header.classList.add("tarefa-header");
    div_task_content.classList.add("tarefa-content");
    div_task_footer.classList.add("tarefa-footer");
    div_task_box.style.display="flex";
};


// --------------------- UPDATE TASKS --------------------- // 
// Função para gerenciar a mudança de status de uma tarefa
function moverTarefa(tarefa, destino) {
    // Verifica se o destino é uma coluna válida (pendente, em progresso, concluída)
    if (['pending', 'InProgress', 'Completed'].includes(destino)) {
        const colunaDestino = document.getElementById(`${destino}Content`);
        
        // Verifica se a coluna de destino existe
        if (colunaDestino) {
            // Remove a tarefa da coluna atual
            const colunaAtual = tarefa.parentElement;
            colunaAtual.removeChild(tarefa);
            
            // Adiciona a tarefa à coluna de destino
            colunaDestino.appendChild(tarefa);
            var formData = new FormData();
            var id_tarefa = tarefa.getAttribute("id_tarefa");
            formData.append("task_id", id_tarefa);
            formData.append("new_task_status",destino);
            
            formData.append("new_task_date", 0);
            formData.append("new_task_type", 0);
            formData.append("new_task_description", 0);
            fetch("/update-task", {
                method: "POST",
                body: formData
            })
        }
    }
}



var modalEditarTarefa = document.getElementById("ModalUpdateTask");
var closeModalEditBtn = document.getElementById("closeModalEditBtn");

closeModalEditBtn.addEventListener("click", function(){
    modalEditarTarefa.style.display = "none";
})

window.addEventListener("click", function(event) {
    if (event.target == modalEditarTarefa) {
        modalEditarTarefa.style.display = "none";
    }
});

const form_edit_tarefas = document.getElementById("formEditTask");

form_edit_tarefas.addEventListener("submit", function(event){
    event.preventDefault()
    var formData = new FormData();
    formData.append("task_id", id_tarefa_global);
    formData.append("new_task_type", form_edit_tarefas.elements[0].value);
    formData.append("new_task_description", form_edit_tarefas.elements[1].value);
    formData.append("new_task_date", form_edit_tarefas.elements[2].value);
    formData.append("new_task_status", 0);
    
    fetch("/update-task", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success != true){
            showAlert(data.success, data.status);
        } else{            
            form_edit_tarefas.reset();
            location.reload();
        }
    })
    
})

// --------------------- DELETE TASKS --------------------- // 
// Função para excluir a tarefa 
function excluirTarefa(tarefa){ 
    var formData = new FormData();
    formData.append("task_id", tarefa.getAttribute("id_tarefa"));
    fetch("/delete-task",{
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success == true){
            tarefa.parentElement.removeChild(tarefa);
            location.reload();
        } else {
            showAlert(data.success, data.status);
        }
    })
}



var modalEditarTarefa = document.getElementById("ModalUpdateTask");
var closeModalEditBtn = document.getElementById("closeModalEditBtn");

// Função responsável por fechar o modal de edital tarefa quando apertado no botão de fechar
closeModalEditBtn.addEventListener("click", function(){
    modalEditarTarefa.style.display = "none";
})

// Função responsável por fechar o modal de edital tarefa quando apertado fora do modal
window.addEventListener("click", function(event) {
    if (event.target == modalEditarTarefa) {
        modalEditarTarefa.style.display = "none";
    }
});


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

// Adiciona ouvintes de evento para os botões que movem ou excluem tarefas
document.addEventListener('click', function (event) {
    const target = event.target;
    
    // Verifica se o usuário apertou o botão para mover uma tarefa
    if (target.classList.contains('move-tarefa')) {
        // Busca o elemento mais próximo com a classe 'move-tarefa' para retornar a div tarefa-caixa que contém a tarefa
        const tarefa = target.closest('.tarefa-caixa');
        const destino = target.dataset.destino;
        if (tarefa && destino) {
            moverTarefa(tarefa, destino);
        }
    }
    
    // Verifica se o usuário apertou o botão para excluir a tarefa
    if (target.classList.contains('excluir-tarefa')){
        const tarefa = target.closest('.tarefa-caixa');
        if (tarefa) {
            excluirTarefa(tarefa);
        }
    }
});


// Função para obter o valor do parâmetro de query
function getQueryParam(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Obter o valor do parâmetro welcome_msg
let welcomeMsg = getQueryParam('welcome_msg');

// Atribuir o valor ao elemento h1
if (welcomeMsg) {
    document.getElementById('welcome-header').textContent = welcomeMsg;
}
