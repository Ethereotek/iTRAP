
var httpRequest = new XMLHttpRequest();

function send_iTAT_Request(endpoint, metricType){
	console.log(endpoint)
	httpRequest.abort()
	httpRequest.open('GET', endpoint)

	httpRequest.onload = function(){
		let text = httpRequest.response;
		console.log(text)
		window.app.endpoints[metricType].response = text;
		return;
	}

	httpRequest.send();
	return;
}