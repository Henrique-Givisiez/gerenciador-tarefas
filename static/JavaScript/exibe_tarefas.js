// Busca variáveis do arquivo HTML
var form_tarefa = document.getElementById("form_tarefas");

// Define a função que irá exibir os dados do formulário na página
form_tarefa.addEventListener("submit", function exibe_tarefa(event) {
    var div_pendentes_content = document.getElementById("pendentes-content");
    event.preventDefault(); //Evita o envio padrão do formulário

    if ((div_pendentes_content.getElementsByClassName("tarefa-caixa").length)<4){

        // Cria os elementos HTML 
        var div_tarefa_caixas = document.createElement("div");
        var div_tarefa_header = document.createElement("div")
        var div_tarefa_content = document.createElement("div");
        var div_tarefa_footer = document.createElement("div");
        var h5_header = document.createElement("h5");
        var p_content = document.createElement("p");
        var span_footer = document.createElement("span");
        
        
        // Cria o menu para alterar a categoria da tarefa (pendentes, em progresso ou concluidas)
        var dropdownDiv = document.createElement('div');
        dropdownDiv.className = 'dropdown';

        var button = document.createElement('button');
        button.className= 'menu';
        const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svgElement.setAttribute("width", "22");
        svgElement.setAttribute("height", "22");
        svgElement.setAttribute("fill", "currentColor");
        svgElement.setAttribute("class", "bi bi-three-dots");
        svgElement.setAttribute("viewBox", "0 0 16 16");
        // Crie o elemento <path>
        const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
        pathElement.setAttribute("d", "M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3");
        
        // Anexe o elemento <path> ao elemento <svg>
        svgElement.appendChild(pathElement);
        button.onclick = function(){
            toggleDropdown(button);
        };
        button.appendChild(svgElement);
        
        var dropdownContentDiv = document.createElement('div');
        dropdownContentDiv.id = 'myDropdown';
        dropdownContentDiv.className = 'dropdown-content';
        
        var muda_para_pendente = document.createElement('button');
        muda_para_pendente.id = 'muda_pendente';
        
        var muda_para_progresso = document.createElement('button');
        muda_para_progresso.id = 'muda_progresso';
        
        var muda_para_concluida = document.createElement('button');
        muda_para_concluida.id = 'muda_concluida';

        var excluir_tarefa = document.createElement("button");
        excluir_tarefa.id = "excluir_tarefa";
        
        muda_para_pendente.className = 'move-tarefa';
        muda_para_progresso.className = 'move-tarefa';
        muda_para_concluida.className = 'move-tarefa';
        excluir_tarefa.className = "excluir-tarefa";
        
        muda_para_pendente.textContent = 'Alterar para pendente';
        muda_para_progresso.textContent = 'Alterar para em progresso';
        muda_para_concluida.textContent = 'Alterar para concluida';
        excluir_tarefa.textContent = "Exclua a tarefa";

        muda_para_pendente.setAttribute("data-destino","pendentes");
        muda_para_progresso.setAttribute("data-destino","progresso");
        muda_para_concluida.setAttribute("data-destino","concluida");
        
        dropdownContentDiv.appendChild(muda_para_pendente);
        dropdownContentDiv.appendChild(muda_para_progresso);
        dropdownContentDiv.appendChild(muda_para_concluida);
        dropdownContentDiv.appendChild(excluir_tarefa);
        
        dropdownDiv.appendChild(button);
        dropdownDiv.appendChild(dropdownContentDiv);
        
        
        // Cria as variáveis para receberem os valores do form
        var input_nome_tarefa = document.getElementById("form_nome_tarefa");
        var input_descricao_tarefa = document.getElementById("form_descricao_tarefa");
        var input_data_tarefa = document.getElementById("form_data_tarefa");
        
        
        // Atribui os valores das variáveis aos elementos HTML 
        h5_header.innerHTML = input_nome_tarefa.value;
        p_content.innerHTML = input_descricao_tarefa.value;
        span_footer.innerHTML = input_data_tarefa.value;
        
        
        // Conecta os filhos aos pais
        div_tarefa_header.appendChild(h5_header);
        div_tarefa_header.appendChild(dropdownDiv);
        div_tarefa_content.appendChild(p_content);
        div_tarefa_footer.appendChild(span_footer);
        div_tarefa_caixas.appendChild(div_tarefa_header);
        div_tarefa_caixas.appendChild(div_tarefa_content);
        div_tarefa_caixas.appendChild(div_tarefa_footer);
        div_pendentes_content.appendChild(div_tarefa_caixas);
        
        
        // Adiciona as classes a cada div
        div_tarefa_caixas.classList.add("tarefa-caixa");
        div_tarefa_header.classList.add("tarefa-header");
        div_tarefa_content.classList.add("tarefa-content");
        div_tarefa_footer.classList.add("tarefa-footer");
        div_tarefa_caixas.style.display="flex";
    }
        
    });
    
    