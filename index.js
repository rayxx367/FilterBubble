var express = require('express');
var app = express();
var serv = require('http').Server(app);

app.get('/', function(req, res){
	res.sendFile(__dirname + '/landingpage.html')
})

var portX = process.env.PORT || 2000;
serv.listen(portX);