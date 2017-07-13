var os = require('os');



var PythonShell = require('python-shell');
 
PythonShell.run('C:\\Users\\rayxx\\Desktop\\testbubble\\03_test_prediction.py', function (err) {
  if (err) throw err;
  console.log('finished');
});