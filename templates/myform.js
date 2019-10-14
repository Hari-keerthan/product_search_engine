
function keydownFunction(event) {
  var x = event.keyCode;
  if (x == 13) {
	location.href = "./"+document.getElementById("sear").value;
    }
};
