// Recebe os dados JSON
fetch('/homepage/read-tasks')
.then(response => response.json())
.then(dado => {
    funcInicializaTarefas(dado);
})


/*
Função para tratar os dados JSON e enviar para a função 'tarefasUI'
Observação: a função 'tarefasUI' irá exibir de fato os dados das tarefas na interface do usuário 
*/
function funcInicializaTarefas(dado) {
    // Busca os valores de cada item no objeto 'data'
    
    for (const chave in dado) {
        const tarefa = dado[chave];
        tarefasUI(tarefa.categoria, tarefa.descricao, tarefa.data, tarefa.ID);
    }
}
