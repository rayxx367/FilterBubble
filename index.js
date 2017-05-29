var express = require('express');
var app = express();

app.get('/', function(req, res){
	res.sendFile(__dirname + '/landingpage.html')
})

var portX = process.env.PORT || 8080;
app.listen(portX);