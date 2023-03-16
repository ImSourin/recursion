define p = Character('Reese', color="#c8ffc8")

#This is the beginning of the game 

label start:

    scene bg damaged_ship
    with dissolve

    p "What happened? Why am I floating in space?"

    "The protagonist looks around and sees that the spaceship has been damaged"
    
    p "I need to save the crew members and find out what happened."

    # 3 questions?
    jump question_bank
    jump question_bank
    jump question_bank

    jump check_and_jump

label repair_oxygen: 

    "The protagonist checks the oxygen levels and sees that they are low"

    p "I need to repair the oxygen supply first. It's a matter of life and death."

    "The protagonist rushes to repair the oxygen supply, but it takes time and his stamina keeps decreasing. Finally, he is successful in repairing the oxygen supply"
    
    p "Phew, I've managed to fix the oxygen supply. I can breathe a sigh of relief for now, but there's still a lot to do. What should I do next?"

    jump question_bank

    jump check_and_jump


label gather_supplies:


    # Display the protagonist's dialogue
    p "I should gather supplies while I have the chance. We need food, water, and other essentials to survive. Who knows how long we'll be stuck out here."

    "I've managed to gather the supplies we need to survive. But there's more to be done. What should I do next?"
    
    jump question_bank

    jump check_and_jump

label analyze_data:

    p "I need to analyze the data logs. Maybe there's something there that can help us figure out what happened."

    "The protagonist heads to the computer room and starts analyzing the data logs. As they sift through the logs, they notice something unusual."

    p "This is strange. There's an encrypted file here that wasn't created by any of our crew members. I should try to decrypt it and see what's inside."

    jump question_bank

    jump check_and_jump

label find_suspect: 

    p "I need to find out who's behind this attack. It's clear that someone on board is responsible."

    "The protagonist starts searching the ship for any clues that might lead them to the suspect. While searching, they come across something suspicious"

    p "This doesn't look right. It's a piece of equipment that was tampered with. This could be a clue to who the traitor is. I should investigate further."

    p "I need to take a break and recover my stamina. If I don't rest, I won't be able to continue. I'll need all my strength to get through this."

    "The protagonist takes a moment to rest and regain their strength. While resting, they notice something strange out of the corner of their eye."

    p "What's that? It looks like a hidden panel. I wonder what's behind it. I should investigate."

    p "I've gathered supplies, analyzed data, and found a suspect. It turns out that one of our crew members was responsible for the attack. We've arrested the traitor and secured the ship. We're safe for now, but who knows what else could happen out here in space. I need to stay vigilant."

    jump question_bank

    jump check_and_jump


label question_bank:
    # Call cif to get the univisited nodes
    # if no nodes left
    jump win
       
    menu:
        # Avoid menu if only 1 menu item or 2 items(analyze_data and find_suspect)
        # If repair_oxygen is univisited
        "Worry about health":
            #Call cif api to increase healthWorry
        
        #If gather_supplies is unvisited
        "Worry about stamina":
            #Call cif api to increase staminaWorry

        #If analyze_data or find_suspect is unvisited
        "Worry about suspicion":
            #Call cif api to increase suspicion
    

label check_and_jump:
    # call cif_api to get transition
    # if transition is between find_suspect and analyze_data
    menu:
        "find suspect":
            # transition = find_suspect
        "analyze_data":
            # transition = analyze_data

    # call transition api
    # call trigger

    # check if dead from cif
    # if dead:
        jump lost

    # jump to transition

label win:
    "WIN"

label lost:
    "LOST"
    
    