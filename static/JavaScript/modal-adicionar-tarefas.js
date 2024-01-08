// Seleção dos elementos necessários para adicionar a tarefa
var btnAdicionarTarefa = document.getElementById("btnAdicionarTarefa");
var closeModalBtn = document.getElementById("closeModalBtn");
var modal = document.getElementById("myModal");

// Abrir o modal quando o botão for clicado
btnAdicionarTarefa.addEventListener("click", function() {
    modal.style.display = "block";
});

// Fechar o modal quando o botão de fechar for clicado
closeModalBtn.addEventListener("click", function() {
    modal.style.display = "none";
});

// Fechar o modal quando o usuário clicar fora dele
window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});
