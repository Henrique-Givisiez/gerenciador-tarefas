// Função para gerenciar a mudança de status de uma tarefa
function moverTarefa(tarefa, destino) {
    // Verifique se o destino é uma coluna válida (pendente, em progresso, concluída)
    if (['pendentes', 'progresso', 'concluida'].includes(destino)) {
        const colunaDestino = document.getElementById(`${destino}-content`);
        
        // Verifique se a coluna de destino existe
        if (colunaDestino && ((colunaDestino.getElementsByClassName("tarefa-caixa").length)<4)) {
            // Remova a tarefa da coluna atual
            const colunaAtual = tarefa.parentElement;
            colunaAtual.removeChild(tarefa);
            
            // Adicione a tarefa à coluna de destino
            colunaDestino.appendChild(tarefa);
        }
    }
}

function excluirTarefa(tarefa){ 
    alerta_confirmacao = confirm("Deseja mesmo excluir a tarefa?");
    if (alerta_confirmacao) {
        tarefa.remove();
    }
}

// Adicione ouvintes de evento para os botões que movem tarefas
document.addEventListener('click', function (event) {
    const target = event.target;
    
    if (target.classList.contains('move-tarefa')) {
        const tarefa = target.closest('.tarefa-caixa');
        const destino = target.dataset.destino;
        
        if (tarefa && destino) {
            moverTarefa(tarefa, destino);
        }
    }
    
    if (target.classList.contains('excluir-tarefa')){
        const tarefa = target.closest('.tarefa-caixa');
        if (tarefa) {
            excluirTarefa(tarefa);
        }
    }
});
