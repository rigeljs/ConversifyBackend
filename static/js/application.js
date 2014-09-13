var broadcast = new ReconnectingWebSocket("ws://"+ location.host + "/broadcast");

broadcast.onclose = function(){
    console.log('outbox closed');
    this.broadcast = new WebSocket(broadcast.url);
};

$("#input-form").on("submit", function(event) {
  event.preventDefault();
  var handle = $("#input-handle")[0].value;
  var text   = $("#input-text")[0].value;
  broadcast.send(JSON.stringify({ handle: handle, text: text }));
  $("#input-text")[0].value = "";
});

broadcast.onmessage = function(message) {
  var data = JSON.parse(message.data);
  $("#chat-text").append("<div class='panel panel-default'><div class='panel-heading'>" + $('<span/>').text(data.handle).html() + "</div><div class='panel-body'>" + $('<span/>').text(data.text).html() + "</div></div>");
  $("#chat-text").stop().animate({
    scrollTop: $('#chat-text')[0].scrollHeight
  }, 800);
};