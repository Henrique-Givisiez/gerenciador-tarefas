var close = document.getElementsByClassName("closeBtnAlert");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

function showAlert(success, msg) {
  if (success == true) {
        var successAlertDiv = document.getElementById("successAlertMsgLogin");
        successAlertDiv.style.display = "block";
        successAlertDiv.style.opacity = 1;
        var successAlertText = document.querySelector("#successAlertMsgLogin strong");
        successAlertText = msg;
  } else {      
        var failAlertDiv = document.getElementById("failAlertMsgLogin");
        failAlertDiv.style.display = "block";
        failAlertDiv.style.opacity = 1;
        var failAlertMsgText = document.querySelector("#failAlertMsgLogin strong");
        failAlertMsgText.textContent = msg;
  }
}