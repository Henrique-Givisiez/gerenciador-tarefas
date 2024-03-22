function tarefasUI (dado) {
            const div_status_content = document.getElementById(`${dado[5]}Content`);

            var div_task_box = document.createElement("div");
            var div_task_header = document.createElement("div")
            var div_task_content = document.createElement("div");
            var div_task_footer = document.createElement("div");
            var h5_header = document.createElement("h5");
            var p_content = document.createElement("p");
            var span_footer = document.createElement("span");   
            
            
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
        
            
            button.appendChild(svgElement);
            button.onclick = function(){
                toggleDropdown(button);
            };
            
            var dropdownContentDiv = document.createElement('div');
            dropdownContentDiv.id = 'myDropdown';
            dropdownContentDiv.className = 'dropdown-content';
            
            var muda_para_pendente = document.createElement('button');
            muda_para_pendente.id = 'muda_pendente';
            var muda_para_progresso = document.createElement('button');
            muda_para_progresso.id = 'muda_progresso';
            var muda_para_concluida = document.createElement('button');
            muda_para_concluida.id = 'muda_concluida';
            
            var editar_tarefa = document.createElement("button");
            editar_tarefa.id = "editar_tarefa";
        
            var excluir_tarefa = document.createElement("button");
            excluir_tarefa.id = "excluir_tarefa";
        
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
        
            div_task_box.setAttribute("status", dado[5])
            
            dropdownContentDiv.appendChild(muda_para_pendente);
            dropdownContentDiv.appendChild(muda_para_progresso);
            dropdownContentDiv.appendChild(muda_para_concluida);
            dropdownContentDiv.appendChild(editar_tarefa);
            dropdownContentDiv.appendChild(excluir_tarefa);
            dropdownDiv.appendChild(button);
            
            dropdownDiv.appendChild(dropdownContentDiv);
            
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
        
            div_status_content.appendChild(div_task_box);
            
            div_task_box.classList.add("tarefa-caixa");
            div_task_header.classList.add("tarefa-header");
            div_task_content.classList.add("tarefa-content");
            div_task_footer.classList.add("tarefa-footer");
            div_task_box.style.display="flex";
        }