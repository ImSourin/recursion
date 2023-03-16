define p = Character('Reese', color="#c8ffc8")

#This is the beginning of the game 

label start:

    scene bg damaged_ship
    with dissolve

    p "What happened? Why am I floating in space?"

    "The protagonist looks around and sees that the spaceship has been damaged"
    
    p "I need to save the crew members and find out what happened."



    #Display the first choice 

    menu:
        "Repair the oxygen supply first":
            jump repair_oxygen
        "Gather supplies first":
            jump gather_supplies
        "Analyze the data logs first":
            jump analyze_data
        "Find the suspect first":
            jump find_suspect

label repair_oxygen: 

    "The protagonist checks the oxygen levels and sees that they are low"

    p "I need to repair the oxygen supply first. It's a matter of life and death."

    "The protagonist rushes to repair the oxygen supply, but it takes time and his stamina keeps decreasing. Finally, he is successful in repairing the oxygen supply"
    
    p "Phew, I've managed to fix the oxygen supply. I can breathe a sigh of relief for now, but there's still a lot to do. What should I do next?"

    menu:
        "Gather supplies":
            jump gather_supplies
        "Analyze the data logs":
            jump analyze_data
        "Find the suspect":
            jump find_suspect

label gather_supplies:


    # Display the protagonist's dialogue
    p "I should gather supplies while I have the chance. We need food, water, and other essentials to survive. Who knows how long we'll be stuck out here."

    "I've managed to gather the supplies we need to survive. But there's more to be done. What should I do next?"
    
    menu:
        "Analyze the data logs":
            jump analyze_data
        "Find the suspect":
            jump find_suspect

label analyze_data:

    p "I need to analyze the data logs. Maybe there's something there that can help us figure out what happened."

    "The protagonist heads to the computer room and starts analyzing the data logs. As they sift through the logs, they notice something unusual."

    p "This is strange. There's an encrypted file here that wasn't created by any of our crew members. I should try to decrypt it and see what's inside."

    menu: 
        "Find the suspect":
            jump find_suspect

label find_suspect: 

    p "I need to find out who's behind this attack. It's clear that someone on board is responsible."

    "The protagonist starts searching the ship for any clues that might lead them to the suspect. While searching, they come across something suspicious"

    p "This doesn't look right. It's a piece of equipment that was tampered with. This could be a clue to who the traitor is. I should investigate further."

    p "I need to take a break and recover my stamina. If I don't rest, I won't be able to continue. I'll need all my strength to get through this."

    "The protagonist takes a moment to rest and regain their strength. While resting, they notice something strange out of the corner of their eye."

    p "What's that? It looks like a hidden panel. I wonder what's behind it. I should investigate."

    p "I've gathered supplies, analyzed data, and found a suspect. It turns out that one of our crew members was responsible for the attack. We've arrested the traitor and secured the ship. We're safe for now, but who knows what else could happen out here in space. I need to stay vigilant."