// Função para exibir mensagem de sucesso/erro na homepage
function msgBox(sucesso, mensagem){
    if (sucesso = true){
        let successDiv = document.getElementById("successDiv");
        successDiv.innerText = mensagem;
        successDiv.style.display = "flex";

    } else{
        let errorDiv = document.getElementById("errorDiv");
        errorDiv.textContent = mensagem;
        errorDiv.style.display = "flex";
    }
}


var closeMsgSuccessBtn = document.getElementById("closeSuccessBtn");
var closeMsgErrorBtn = document.getElementById("closeErrorBtn");

closeMsgSuccessBtn.addEventListener("click", function(event){
    event.preventDefault();
    console.log("entrou");
    
    let successMsgDiv = document.getElementById("successDiv");
    successMsgDiv.parentNode.removeChild(successMsgDiv);
})

closeMsgErrorBtn.addEventListener("click", function(event){
    
    let errorMsgDiv = document.getElementById("errorDiv");
    errorMsgDiv.parentNode.removeChild(errorMsgDiv);
})
