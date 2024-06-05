var close = document.getElementsByClassName("closeBtnAlert");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

const form_signup = document.getElementById("form_signup");
form_signup.addEventListener("submit", function formSignup(event){
    event.preventDefault();
    var formData = new FormData(form_signup);
    fetch("/signup", {
        method: "POST",
        body: formData
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success == true){
            window.location.assign("http://127.0.0.1:5000/login")
        } else {
            var failAlertDiv = document.getElementById("failAlertMsgSignup");
            failAlertDiv.style.display = "block";
            failAlertDiv.style.opacity = 1;
            var failAlertMsgText = document.querySelector("#failAlertMsgSignup strong");
            failAlertMsgText.textContent = data.msg;
        }
    })
})