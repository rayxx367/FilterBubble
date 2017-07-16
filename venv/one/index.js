var PythonShell = require('python-shell');
var express = require('express');
var app = express();
var bodyparser = require('body-parser');
app.use(bodyparser());
var json2csv = require('json2csv');
var fs = require('fs');

app.use(express.static(__dirname));

var mongojs = require("mongojs");
var db = mongojs('mongodb://rai:rai@ds139242.mlab.com:39242/filterbubble', ['likesInfo']);

app.get('/', function(req, res){
	res.sendFile(__dirname + '/landingpage.html')
})

app.get('/userhome', function(req, res){
	res.sendFile(__dirname + '/userhome.html')
})

app.get('/twitterchart', function(req,res){
	res.sendFile(__dirname + '/twitterchart/Donutchart.html')
})

app.get('/displayChart', function(req,res){
	res.sendFile(__dirname + '/displayChart.html')
})

app.post('/userLikes', function(req, res){
    console.log(req.body.id);
    var fields = ['id', 'name', 'about'];
    var csv = json2csv({ data: req.body.likesArray, fields: fields });
	    fs.writeFile(__dirname+'/likesInfo/'+req.body.id+'_likes.csv', csv, function(err) {
	  		if (err) throw err;
		  	console.log('file saved');
		  	PythonShell.run('03_test_prediction.py', {args: [req.body.id+'_likes.csv']} ,function (err) {
			  if (err) throw err;
			  //window.location("http://www.google.com")
			  console.log("Finished")
			  return res.json ({'hello': 'hello'});
			});
		});
		db.likesInfo.insert(req.body, function(err, noOfDocs){
			console.log("Something done")
		})
    //return res.json(1);
});

var portX = process.env.PORT || 8080;
app.listen(portX);



