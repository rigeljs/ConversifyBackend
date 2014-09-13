var broadcast = new ReconnectingWebSocket("ws://"+ location.host + "/broadcast");
var intimate = new ReconnectingWebSocket("ws://"+ location.host + "/intimate");

$(document).ready(function() {
	console.log("in onload function"); 
	broadcast.send({uid : 1});
	});

broadcast.onclose = function(){
    console.log('outbox closed');
    this.broadcast = new WebSocket(broadcast.url);
};

intimate.onclose = function(){
	console.log('outbox closed');
    this.broadcast = new WebSocket(broadcast.url);
}

$("#input-form-broad").on("submit", function(event) {
  event.preventDefault();
  var handle = $("#input-handle-broad")[0].value;
  var text   = $("#input-text-broad")[0].value;
  broadcast.send(JSON.stringify({ handle: handle, text: text }));
  $("#input-text-broad")[0].value = "";
});

$("#input-form-int").on("submit", function(event) {
  event.preventDefault();
  var handle = $("#input-handle-int")[0].value;
  var text   = $("#input-text-int")[0].value;
  intimate.send(JSON.stringify({ handle: handle, text: text }));
  $("#input-text-int")[0].value = "";
});

intimate.onmessage = function(message) {
  var data = JSON.parse(message.data);
  $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.handle).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.text).html() + "</div></div>");
  $("#chat-text").stop().animate({
    scrollTop: $('#chat-text')[0].scrollHeight
  }, 800);
};

broadcast.onmessage = function(message) {
  var data = JSON.parse(message.data);
  $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.handle).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.text).html() + "</div></div>");
  $("#chat-text").stop().animate({
    scrollTop: $('#chat-text')[0].scrollHeight
  }, 800);
};