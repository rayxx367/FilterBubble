var express = require('express');
var app = express();

app.get('/', function(req, res){
	res.sendFile(__dirname + '/landingpage.html')
})

app.get('/userhome', function(req, res){
	res.sendFile(__dirname + '/userhome.html')
})

app.get('/twitterchart', function(req,res){
	res.sendFile(__dirname + '/twitterchart/Donutchart.html')
})

var portX = process.env.PORT || 8080;
app.listen(portX);