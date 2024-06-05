// Referências aos elementos
var openModalBtn = document.getElementById("btnAddTask");
var closeModalBtn = document.getElementById("closeModalBtn");
var modal = document.getElementById("ModalAddTask");

// Abrir o modal quando o botão for clicado
openModalBtn.addEventListener("click", function() {
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
