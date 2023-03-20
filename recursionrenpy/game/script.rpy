init python:
    import requests
    import json
    BASE_URL = 'http://localhost:8081/'
    headers = {
        'Content-Type': 'application/json',
    }


define p = Character('Shaw', color="#c8ffc8")

#This is the beginning of the game 

label start:

    play music "audio/intro.mp3"
    scene bg damaged_ship_1
    with fade

    show shaw scared at left
    with dissolve

    p "What happened? Why am I floating in space?"

    hide shaw scared
    with dissolve

    "Shaw looks around and sees that the spaceship has been damaged"
    
    show shaw neutral at left
    with dissolve

    p "I need to save the crew members and find out what happened."


    show shaw neutral at left
    with dissolve

    "There has been an attack on the spaceship. You need to save the crew members and find out how did it happen. Specifically, you need to Repair Oxygen, Gather supplies, Analyze data and Find a suspect."

    # 3 questions?
    call QUESTION
    call QUESTION
    call QUESTION

    jump TRANSITION


label REPAIR_O2: 
    scene bg oxygen_room
    with fade

    "Shaw checks the oxygen levels and sees that they are low."

    show shaw scared at left 
    with dissolve

    p "I need to repair the oxygen supply first. It's a matter of life and death."

    hide shaw scared
    with dissolve

    "Shaw rushes to repair the oxygen supply, but it takes time and his stamina keeps decreasing. Finally, she is successful in repairing the oxygen supply"
    
    show shaw happy at left 
    with dissolve

    p "Phew, I've managed to fix the oxygen supply. I can breathe a sigh of relief for now, but that's just one piece of the puzzle."

    show shaw neutral at left
    with dissolve

    call QUESTION

    call TRANSITION


label GATHER_SUPPLIES:

    scene bg supply_room
    with fade

    show shaw sad at left
    with dissolve
    # Display the protagonist's dialogue
    p "I should gather supplies while I have the chance. We need food, water, and other essentials to survive. Who knows how long we'll be stuck out here."
    
    show shaw neutral at left 
    with dissolve
    ". . . "

    show shaw happy at left
    with dissolve
    "I've managed to gather the supplies we need to survive. But there's more to be done. What should I do next?"

    show shaw neutral at left
    with dissolve
    
    call QUESTION

    jump TRANSITION


label ANALYZE_DATA:

    scene bg data_log_room 
    with fade

    show shaw neutral at left
    with dissolve
    p "I need to analyze the data logs. Maybe there's something there that can help us figure out what happened."

    hide shaw neutral at left
    with dissolve

    "Shaw heads to the computer room and starts analyzing the data logs. As they sift through the logs, they notice something unusual."

    show shaw surprised at left
    with dissolve
    p "This is strange. There's an encrypted file here that wasn't created by any of our crew members. I should try to decrypt it and see what's inside."

    show shaw neutral at left
    with dissolve

    python:
        unvisited_nodes = json.loads(requests.get(BASE_URL+'getUnvisitedNodes').text)
        if "FIND_SUSPECT" not in unvisited_nodes:
            p("But it's all in vain now. I shouldn't have accused John so early.")
        else:
            p("I think I found who it was!!")

    call QUESTION

    jump TRANSITION


label FIND_SUSPECT: 

    scene bg space_corridor
    with fade

    show shaw angry at left
    with dissolve

    p "I need to find out who's behind this attack. It's clear that someone on board is responsible."

    hide shaw angry
    with dissolve

    "Shaw starts searching the ship for any clues that might lead them to the suspect. While searching, they come across something suspicious"

    show shaw surprised at left 
    with dissolve
    p "This doesn't look right. It's a piece of equipment that was tampered with. This could be a clue to who the traitor is. I should investigate further."

    hide shaw surprised
    with dissolve

    show shaw neutral at left
    with dissolve
    p "I need to take a break and recover my stamina. If I don't rest, I won't be able to continue. I'll need all my strength to get through this."

    hide shaw neutral
    with dissolve

    "Shaw takes a moment to rest and regain their strength. While resting, they notice something strange out of the corner of their eye."

    show shaw surprised at left
    with dissolve

    p "What's that? It looks like a hidden panel. I wonder what's behind it. I should investigate."

    hide shaw surprised
    with dissolve

    $ confidence = json.loads(requests.post(BASE_URL+'getAttribute', headers=headers, json={
            'class': 'feeling',
            'type': 'confidence'
        }).text)[0]['value']

    "Shaw accuses John since he was the last one to log in to the servers."

    if confidence == 100:
        p "It turns out that John was responsible for the attack. We've arrested the traitor and secured the ship. We're safe for now, but who knows what else could happen out here in space. I need to stay vigilant."
    else:

        show shaw sad at left
        with dissolve

        p "Aah, I'm sorry! I shouldn't have accused you before being confident. I should have analyzed the data first."

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
    stop music fadeout 1.0
    show shaw happy at left
    with dissolve
    python:
        renpy.set_return_stack([])
        narrator("Congratulations! You have successfully completed the mission and emerged victorious. Your skills and strategy have paid off. Enjoy your well-earned win!")
    return

label DIE:
    stop music fadeout 1.0
    show shaw sad at left
    with dissolve
    python:
        renpy.set_return_stack([])
        narrator("Aaah!! But your health and stamina is too low now. You should have repaired the Oxygen supply quicker.")
    return
