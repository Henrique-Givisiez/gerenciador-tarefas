// Função para mostrar/ocultar o dropdown
function toggleDropdown(btn) {
    var parent_div = btn.parentElement;
    var dropdown = parent_div.querySelector("#myDropdown");
    dropdown.classList.toggle("show");
  }
  
  window.onclick = function(event) {
    var buttons = document.querySelectorAll('button.menu');

    // Verifica se o alvo do clique não é nenhum dos botões e não é um elemento SVG dentro desses botões
    if (!isButtonOrChild(event.target, buttons)) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Função auxiliar para verificar se o elemento clicado é um botão ou está dentro de um botão
function isButtonOrChild(element, buttons) {
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        if (element === button || button.contains(element)) {
            return true;
        }
    }
    return false;
}
