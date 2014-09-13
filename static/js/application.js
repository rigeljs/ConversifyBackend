var broadcast = new ReconnectingWebSocket("ws://"+ location.host + "/broadcast");
var update = new ReconnectingWebSocket("ws://"+ location.host + "/update");
console.log(location.host);

broadcast.onopen = function() {
	broadcast.send(JSON.stringify({uid : 1}));
};

broadcast.onclose = function(){
    console.log('outbox closed');
    this.broadcast = new WebSocket(broadcast.url);
};

update.onclose = function(){
	console.log('outbox closed');
    this.broadcast = new WebSocket(broadcast.url);
}

$("#input-form-broad").on("submit", function(event) {
  event.preventDefault();
  var handle = $("#input-handle-broad")[0].value;
  var text   = $("#input-text-broad")[0].value;
  broadcast.send(JSON.stringify({ sender_id: 1, conversation_id: 1, content: text }));
  $("#input-text-broad")[0].value = "";
});

$("#input-form-int").on("submit", function(event) {
  event.preventDefault();
  var methodName = $("#input-handle-int")[0].value;
  var arg   = $("#input-text-int")[0].value;
  update.send('{ "method": {0}, "arguments": {1} }'.format(methodName, arg));
  $("#input-text-int")[0].value = "";
});

update.onmessage = function(message) {
  console.log(message);
  var data = JSON.parse(message.data);
  $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text("method results").html() + "</div><div class='panel-body'>" + $('<span/>').text(data.results).html() + "</div></div>");
  $("#chat-text").stop().animate({
    scrollTop: $('#chat-text')[0].scrollHeight
  }, 800);
};

broadcast.onmessage = function(message) {
  console.log("received message");
  var data = JSON.parse(message.data);
  console.log(data);
  $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.sender_id).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.content).html() + "</div></div>");
  $("#chat-text").stop().animate({
    scrollTop: $('#chat-text')[0].scrollHeight
  }, 800);
};