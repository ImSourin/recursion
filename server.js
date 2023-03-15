var express = require('express')
var fs = require('fs')
var cif = require('./cif.js')
var app = express();
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

cif.init()
var rawSchema = cif.loadFile("data/schema.json");
var schema = cif.loadSocialStructure(rawSchema);

var rawCast = cif.loadFile("data/cast.json");
var cast = cif.addCharacters(rawCast);

var rawTriggerRules = cif.loadFile("data/triggerRules.json");
var triggerRules = cif.addRules(rawTriggerRules);

var rawVolitionRules = cif.loadFile("data/volitionRules.json");
var volitionRules = cif.addRules(rawVolitionRules);

var rawActions = cif.loadFile("data/actions.json");
var actions = cif.addActions(rawActions);

var rawHistory = cif.loadFile("data/history.json");
var history = cif.addHistory(rawHistory);

var storedVolitions = cif.calculateVolition(cast);

console.log(storedVolitions)

app.get('/getActions', function (req, res) {
    res.end(possibleActions)
})

app.post('/performActions', function (req, res) {
    res.end(possibleActions[JSON.parse(req.body.action)])
})

app.get('/getAttributes', function (req, res) {
    var heroIntelligencePred = {
        "class" : "attribute",
        "type" : "intelligence",
        "first" : "hero"
    };
    res.end(cif.get(heroIntelligencePred))
})

app.get('/getFeeling', function (req, res) {
    var heroIntelligencePred = {
        "class" : "attribute",
        "type" : "intelligence",
        "first" : "hero"
    };
    res.end(cif.get(heroIntelligencePred))
})

var server = app.listen(8081, function () {
    console.log("CiF backend listening")
})