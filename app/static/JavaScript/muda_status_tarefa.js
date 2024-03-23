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
                method: "PUT",
                body: formData
            })
        }
    }
}

// Função para excluir a tarefa 
function excluirTarefa(tarefa){ 
    alerta_confirmacao = confirm("Deseja mesmo excluir a tarefa?");
    if (alerta_confirmacao) {
        $.ajax({
            method: 'POST',
            url: '/excluir-tarefa',
            data: {"tarefa_excluida": tarefa.getAttribute("id_tarefa")},
            success: function(response){
                tarefa.remove();
            },
            error: function(error) {
                // Verifique se o erro é uma resposta JSON com uma mensagem de erro
                try {
                    const errorMessage = JSON.parse(error.responseText).error;
                    alert('Erro: ' + errorMessage);
                } catch (e) {
                    // Se o erro não for um JSON com uma mensagem de erro, exiba a resposta completa
                    alert('Erro: ' + error.responseText);
                }
            }
        });
    }
}

// Função para editar a tarefa

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
