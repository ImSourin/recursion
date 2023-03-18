init python:
    import requests
    import json
    BASE_URL = 'http://localhost:8081/'
    headers = {
        'Content-Type': 'application/json',
    }


define p = Character('Reese', color="#c8ffc8")

#This is the beginning of the game 

label start:

    scene bg damaged_ship
    with dissolve

    p "What happened? Why am I floating in space?"

    "The protagonist looks around and sees that the spaceship has been damaged"
    
    p "I need to save the crew members and find out what happened."

    # 3 questions?
    call QUESTION
    call QUESTION
    call QUESTION

    jump TRANSITION


label REPAIR_O2: 

    "The protagonist checks the oxygen levels and sees that they are low"

    p "I need to repair the oxygen supply first. It's a matter of life and death."

    "The protagonist rushes to repair the oxygen supply, but it takes time and his stamina keeps decreasing. Finally, he is successful in repairing the oxygen supply"
    
    p "Phew, I've managed to fix the oxygen supply. I can breathe a sigh of relief for now, but there's still a lot to do. What should I do next?"
    
    call QUESTION

    call TRANSITION


label GATHER_SUPPLIES:


    # Display the protagonist's dialogue
    p "I should gather supplies while I have the chance. We need food, water, and other essentials to survive. Who knows how long we'll be stuck out here."

    "I've managed to gather the supplies we need to survive. But there's more to be done. What should I do next?"
    
    call QUESTION

    jump TRANSITION


label ANALYZE_DATA:

    p "I need to analyze the data logs. Maybe there's something there that can help us figure out what happened."

    "The protagonist heads to the computer room and starts analyzing the data logs. As they sift through the logs, they notice something unusual."

    p "This is strange. There's an encrypted file here that wasn't created by any of our crew members. I should try to decrypt it and see what's inside."

    call QUESTION

    jump TRANSITION


label FIND_SUSPECT: 

    p "I need to find out who's behind this attack. It's clear that someone on board is responsible."

    "The protagonist starts searching the ship for any clues that might lead them to the suspect. While searching, they come across something suspicious"

    p "This doesn't look right. It's a piece of equipment that was tampered with. This could be a clue to who the traitor is. I should investigate further."

    p "I need to take a break and recover my stamina. If I don't rest, I won't be able to continue. I'll need all my strength to get through this."

    "The protagonist takes a moment to rest and regain their strength. While resting, they notice something strange out of the corner of their eye."

    p "What's that? It looks like a hidden panel. I wonder what's behind it. I should investigate."

    $ confidence = json.loads(requests.post(BASE_URL+'getAttribute', headers=headers, json={
            'class': 'feeling',
            'type': 'confidence'
        }).text)[0]['value']

    if confidence == 100:
        p "I've gathered supplies, analyzed data, and found a suspect. It turns out that one of our crew members was responsible for the attack. We've arrested the traitor and secured the ship. We're safe for now, but who knows what else could happen out here in space. I need to stay vigilant."
    else:
        p "Oops wrong suspect. no evidence"

    call QUESTION

    jump TRANSITION


label QUESTION:
    python:
        unvisited_nodes = json.loads(requests.get(BASE_URL+'getUnvisitedNodes').text)
        if len(unvisited_nodes) == 0:
            renpy.jump("WIN")
        elif len(unvisited_nodes) == 1:
            requests.post(BASE_URL+'performAction', headers=headers, json={
                'action': unvisited_nodes[0]
            })
            requests.get(BASE_URL+'runTriggers')
            renpy.jump(unvisited_nodes[0])
        elif len(unvisited_nodes) == 2:
            if "ANALYZE_DATA" in unvisited_nodes and "FIND_SUSPECT" in unvisited_nodes:
                renpy.jump("TRANSITION")
        else:
            question = json.loads(requests.get(BASE_URL+'getQuestion').text)
            narrator(question['text'])
            options = list(zip(question['optionLabels'], question['optionActions']))
            action = renpy.display_menu(options)
            requests.post(BASE_URL+'performAction', headers=headers, json={
                'action': action
            })
    return

label TRANSITION:
    python:
        unvisited_nodes = json.loads(requests.get(BASE_URL+'getUnvisitedNodes').text)
        transition = requests.get(BASE_URL+'getActions').text
        if len(unvisited_nodes) == 2 and transition != "DIE_HEALTH" and transition != "DIE_STAMINA":
            if "ANALYZE_DATA" in unvisited_nodes and "FIND_SUSPECT" in unvisited_nodes:
                question = json.loads(requests.get(BASE_URL+'getQuestion').text)
                narrator(question['text'])
                options = list(zip(question['optionLabels'], question['optionActions']))
                transition = renpy.display_menu(options)

        requests.post(BASE_URL+'performAction', headers=headers, json={
            'action': transition
        })
        requests.get(BASE_URL+'runTriggers')
        renpy.jump(str(transition))

label LOST:
    python:
        dead = requests.get(BASE_URL+'isDead').text
        if dead == "True":
            renpy.jump("DIE")


label DIE_HEALTH:
    jump DIE

label DIE_STAMINA:
    jump DIE

label WIN:
    python:
        renpy.set_return_stack([])
        narrator("WIN")
    return

label DIE:
    python:
        renpy.set_return_stack([])
        narrator("DIE")
    return
