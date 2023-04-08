
var coll = document.getElementsByClassName("collapsible");
console.log("hello world")
// for( let i = 0; i < coll.length; i++){
// 	coll[i].addEventListener("click", function(){
// 		console.log("collapse")
// 		this.classList.toggle("active");
// 		var content = this.nextElementSibling;

// 		if(content.style.display === "block"){
// 			content.style.display = "none"
// 		}else{
// 			content.style.display = "block"
// 		}
// 	})
// }

function collapse(element){


	console.log("collapse")
	// this.classList.toggle("active");
	var content = element.nextElementSibling;

	if(content.style.display === "block"){
		content.style.display = "none"
	}else{
		content.style.display = "block"
	}
	

}
