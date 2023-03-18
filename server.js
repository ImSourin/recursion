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


var allNodes = new Map()
actions.forEach((obj) => {
    allNodes.set(obj.name, false);
});

var terminalActionMap = {
    "REPAIR_O2": ['INCREASE_HEALTH', 'DECREASE_HEALTH_WORRY'],
    "GATHER_SUPPLIES": ['INCREASE_STAMINA', 'DECREASE_STAMINA_WORRY'],
    "FIND_SUSPECT": ['DECREASE_SUSPICION'],
    "ANALYZE_DATA": ['INCREASE_CONFIDENCE'],
    "DIE_HEALTH": [],
    "DIE_STAMINA": []
}

app.get('/getActions', function (req, res) {
    console.log("getActions");
    var storedVolitions = cif.calculateVolition(cast);
    var actionList = cif.getActions("hero", "hero", storedVolitions, cast, 5, 5, 5);
    for (let i = 0; i < actionList.length; i++) {
        var lin = actionList[i]['lineage'].split("-")[0];
        if (allNodes.get(lin) === false) {
            res.end(lin);
            console.log("action sent" + actionList[i]['lineage']);
            return;
        }
    }
    console.log("action sent" + JSON.stringify(actionList));
    res.end("DIE"); // should never happen
})

app.post('/performAction', bodyParser.json(), function (req, res) {
    console.log("performAction"+req.body['action'])
    if(terminalActionMap.hasOwnProperty(req.body['action'])) {
        allNodes.set(req.body['action'], true);
        for (let i = 0; i < terminalActionMap[req.body['action']].length; i++) {
            cif.doAction(actionMap.get(terminalActionMap[req.body['action']][i]));
            console.log('execute action '+ terminalActionMap[req.body['action']][i]);
        }
    } else {
        cif.doAction(actionMap.get(req.body['action']));
        console.log('execute action '+ req.body['action']);
    }
    allNodes[req.body['action']] = true;
    res.end("OK");
})

app.post('/getAttribute', bodyParser.json(), function (req, res) {
    console.log("getAttribute");
    var attributeQuery = {
        "class": req.body['class'], "type": req.body['type'], "first": "hero"
    };
    res.end(JSON.stringify(cif.get(attributeQuery)));
})

app.get('/runTriggers', function (req, res) {
    console.log("runTriggers");
    res.end(JSON.stringify(cif.runTriggerRules(cast)));
})

app.get('/getUnvisitedNodes', function (req, res) {
    console.log("getUnvisitedNodes");
    var nodeList = []
    if (!allNodes["REPAIR_O2"]) nodeList.push("REPAIR_O2")
    if (!allNodes["GATHER_SUPPLIES"]) nodeList.push("GATHER_SUPPLIES")
    if (!allNodes["FIND_SUSPECT"]) nodeList.push("FIND_SUSPECT")
    if (!allNodes["ANALYZE_DATA"]) nodeList.push("ANALYZE_DATA")
    res.end(JSON.stringify(nodeList));
})

var questionIds = [];

app.get('/getQuestion', function (req, res) {
    console.log("getQuestion");
    var file = fs.readFileSync("data/questions.json", 'utf8');
    var questions = JSON.parse(file)["questions"];

    var nodeList = []
    if (allNodes["REPAIR_O2"]) nodeList.push("REPAIR_O2")
    if (allNodes["GATHER_SUPPLIES"]) nodeList.push("GATHER_SUPPLIES")
    if (allNodes["FIND_SUSPECT"]) nodeList.push("FIND_SUSPECT")
    if (allNodes["ANALYZE_DATA"]) nodeList.push("ANALYZE_DATA")
    nodeList.sort();
    for (let i = 0; i < questions.length; i++) {
        var vis = questions[i]['visited'].sort();
        if (JSON.stringify(nodeList) === JSON.stringify(vis) && !questionIds.includes(questions[i]['id'])) {
            questionIds.push(questions[i]['id']);
            res.end(JSON.stringify(questions[i]));
            return;
        }
    }
})

app.get('/isDead', function (req, res) {
    console.log("isDead");
    var healthQuery = {
        "class": 'attribute', "type": 'health', "first": "hero"
    };
    health = cif.get(healthQuery).value

    var staminaQuery = {
        "class": 'attribute', "type": 'stamina', "first": "hero"
    };

    stamina = cif.get(staminaQuery).value

    if (health < 0 || stamina < 0) {
        res.end("True");
        return;
    }
    res.end("False");
})

var server = app.listen(8081, function () {
    console.log("CiF backend listening")
})