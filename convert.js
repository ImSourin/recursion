var fs = require('fs');
var umdify = require('umdify');

var contents = fs.readFileSync('./test.js', 'utf8');
contents = umdify(contents);
fs.writeFileSync('./actionLibrary.js', contents);