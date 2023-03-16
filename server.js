var express = require('express')
var fs = require('fs')
var cif = require('./cif/cif.js')
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

var rawHistory = JSON.parse(cif.loadFile("data/history.json"));
var history = cif.addHistory(rawHistory);



app.get('/getActions', function (req, res) {
    var storedVolitions = cif.calculateVolition(cast);
    res.end(JSON.stringify(cif.getActions("hero", "hero", storedVolitions, cast, 1, 5, 5)));
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