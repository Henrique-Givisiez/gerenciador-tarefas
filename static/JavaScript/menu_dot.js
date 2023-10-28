// Função para mostrar/ocultar o dropdown
function toggleDropdown(btn) {
    var parent_div = btn.parentElement; 
    var dropdown = parent_div.querySelector("#myDropdown");
    dropdown.classList.toggle("show");
  }
  
  // Fechar o dropdown se o usuário clicar fora dele
  window.onclick = function(event) {
    if (!event.target.matches('button')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
  