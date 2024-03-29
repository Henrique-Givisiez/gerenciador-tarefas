function tarefasUI (categoria_tarefa, descricao_tarefa, data_tarefa, status_tarefa, id_tarefa) {
            // Cria os elementos HTML 
            var div_pendentes_content = document.getElementById("pendentes-content");
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

            // Cria o botão para exibir o menu dropdown
            var button = document.createElement('button');
            button.className= 'menu';
            
            // Cria o símbolo do menu 
            const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svgElement.setAttribute("width", "16");
            svgElement.setAttribute("height", "15");
            svgElement.setAttribute("fill", "currentColor");
            svgElement.setAttribute("class", "bi bi-list");
            svgElement.setAttribute("viewBox", "0 0 16 16");
            const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
            pathElement.setAttribute("d", "M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5");
            svgElement.appendChild(pathElement);

            
            button.appendChild(svgElement);
            // Função 'toggleDropdown' que exibirá as opções do menu 
            button.onclick = function(){
                toggleDropdown(button);
            };
            
            // Cria a div, inicialmente escondida, irá exibir as opções para alterar o status da tarefa
            var dropdownContentDiv = document.createElement('div');
            dropdownContentDiv.id = 'myDropdown';
            dropdownContentDiv.className = 'dropdown-content';
            
            // Crias os botões para alterar o status da tarefa
            var muda_para_pendente = document.createElement('button');
            muda_para_pendente.id = 'muda_pendente';
            var muda_para_progresso = document.createElement('button');
            muda_para_progresso.id = 'muda_progresso';
            var muda_para_concluida = document.createElement('button');
            muda_para_concluida.id = 'muda_concluida';
            
            // Cria o botão para editar a tarefa
            var editar_tarefa = document.createElement("button");
            editar_tarefa.id = "editar_tarefa";

            // Cria o botão para excluir a tarefa
            var excluir_tarefa = document.createElement("button");
            excluir_tarefa.id = "excluir_tarefa";

            // Atribui as classes para os botões e adiciona conteúdo
            muda_para_pendente.className = 'move-tarefa';
            muda_para_progresso.className = 'move-tarefa';
            muda_para_concluida.className = 'move-tarefa';
            excluir_tarefa.className = "excluir-tarefa";
            editar_tarefa.className = "editar-tarefa";
            muda_para_pendente.textContent = 'Alterar para pendente';
            muda_para_progresso.textContent = 'Alterar para em progresso';
            muda_para_concluida.textContent = 'Alterar para concluida';
            editar_tarefa.textContent = "Editar tarefa";
            excluir_tarefa.textContent = "Exclua a tarefa";
    
            // Criação do atributo do status da tarefa
            div_tarefa_caixas.setAttribute("status", status_tarefa)
            
            // Definição da herança entre os elementos criados do menu
            dropdownContentDiv.appendChild(muda_para_pendente);
            dropdownContentDiv.appendChild(muda_para_progresso);
            dropdownContentDiv.appendChild(muda_para_concluida);
            dropdownContentDiv.appendChild(editar_tarefa);
            dropdownContentDiv.appendChild(excluir_tarefa);
            dropdownDiv.appendChild(button);
            dropdownDiv.appendChild(dropdownContentDiv);
            
            // Atribui os valores submetidos (parâmetros) aos elementos da interface  
            h5_header.innerHTML = categoria_tarefa;
            p_content.innerHTML = descricao_tarefa;
            span_footer.innerHTML = data_tarefa;
            
            // Definição da herança entre os elementos criados da div contendo a tarefa estilizada e visualizada pelo usuário
            div_tarefa_header.appendChild(h5_header);
            div_tarefa_header.appendChild(dropdownDiv);
            div_tarefa_content.appendChild(p_content);
            div_tarefa_footer.appendChild(span_footer);
            div_tarefa_caixas.appendChild(div_tarefa_header);
            div_tarefa_caixas.appendChild(div_tarefa_content);
            div_tarefa_caixas.appendChild(div_tarefa_footer);
            div_tarefa_caixas.setAttribute("id_tarefa", id_tarefa);
            div_pendentes_content.appendChild(div_tarefa_caixas);
            
            
            // Adiciona as classes aos elementos restantes
            div_tarefa_caixas.classList.add("tarefa-caixa");
            div_tarefa_header.classList.add("tarefa-header");
            div_tarefa_content.classList.add("tarefa-content");
            div_tarefa_footer.classList.add("tarefa-footer");
            div_tarefa_caixas.style.display="flex";
}