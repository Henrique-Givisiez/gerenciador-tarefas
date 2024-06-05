var close = document.getElementsByClassName("closeBtnAlert");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

const form_login = document.getElementById("formLogin");
form_login.addEventListener("submit", function formLogin(event){
    event.preventDefault();
    var formData = new FormData(form_login);
    
    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success == true){
            let welcome_msg = data.msg;
            window.location.assign(`http://127.0.0.1:5000/homepage?welcome_msg=${encodeURIComponent(welcome_msg)}`);
        } else {
            var failAlertDiv = document.getElementById("failAlertMsgLogin");
            failAlertDiv.style.display = "block";
            failAlertDiv.style.opacity = 1;
            var failAlertMsgText = document.querySelector("#failAlertMsgLogin strong");
            failAlertMsgText.textContent = data.msg;
        }
    })
})