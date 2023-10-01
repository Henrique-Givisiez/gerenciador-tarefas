const adicionaTarefa = document.getElementById("task-form");
    const taskInput = document.getElementById("task-input");
    const responseDiv = document.getElementById("response");
    adicionaTarefa.addEventListener("submit", function (event) {
      event.preventDefault(); // Impede o envio do formulário padrão
      const task = taskInput.value;
      if (task) {
        const tarefas = document.createElement("div");
        const botaoRemover = document.createElement("button");
        botaoRemover.textContent = "Remover"; 
        botaoRemover.addEventListener("click", function() {
          tarefas.remove();
          if (responseDiv.children.length == 0){
            responseDiv.classList.remove("form-resposta");
          }
        });
        const responseText = document.createElement("p");
        responseText.textContent = "Tarefa adicionada: " + task;
        tarefas.appendChild(responseText);
        tarefas.appendChild(botaoRemover);
        tarefas.classList.add("tarefa");
        responseDiv.appendChild(tarefas);
        responseDiv.classList.add("form-resposta");
       
    // Adiciona a classe form-container à div response
        taskInput.value = ""; // Limpa o campo após a submissão
      }
    });