var express = require('express')
var fs = require('fs')
var cif = require('./cif/cif.js')
var bodyParser = require('body-parser')
var app = express();
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

cif.init()
var rawSchema = JSON.parse(cif.loadFile("data/schema.json"));
var schema = cif.loadSocialStructure(rawSchema);

var rawCast = JSON.parse(cif.loadFile("data/cast.json"));
var cast = cif.addCharacters(rawCast);

var rawTriggerRules = JSON.parse(cif.loadFile("data/triggerRules.json"));
var triggerRules = cif.addRules(rawTriggerRules);

var rawVolitionRules = JSON.parse(cif.loadFile("data/volitionRules.json"));
var volitionRules = cif.addRules(rawVolitionRules);

var rawActions = JSON.parse(cif.loadFile("data/actions.json"));
var actions = cif.addActions(rawActions);
const actionMap = new Map()
actions.forEach((obj) => {
    actionMap.set(obj.name, obj);
});

var rawHistory = JSON.parse(cif.loadFile("data/history.json"));
var history = cif.addHistory(rawHistory);



app.get('/getActions', function (req, res) {
    var storedVolitions = cif.calculateVolition(cast);
    // res.end(JSON.stringify(cif.getActions("hero", "hero", storedVolitions, cast, 1, 5, 5)));
    res.end(JSON.stringify(cif.getAllActions()));
})

app.post('/performAction', bodyParser.json(), function (req, res) {
    console.log('Action found' + actionMap[req.body['action']])
    cif.doAction(actionMap.get(req.body['action']));
    res.end("OK");
})

app.post('/getAttribute', bodyParser.json(), function (req, res) {
    var attributeQuery = {
        "class" : req.body['class'],
        "type" : req.body['type'],
        "first" : "hero"
    };
    res.end(JSON.stringify(cif.get(attributeQuery)))
})

var server = app.listen(8081, function () {
    console.log("CiF backend listening")
})