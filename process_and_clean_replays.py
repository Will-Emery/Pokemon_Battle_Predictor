"""Module: process_clean_replays.py
This file contains functions for processing and cleaning replays. This includes removing the turn number, removing the player names, and removing the pokemon names."""
from file_io import write_to_file, get_file_contents
import os
import re


def process_replays(dirty_replays_location, clean_replays_location):
    """Process the replays in the given locations and saves them to a new file
    
    Args:
        replays_locations: The location of the replays to process
    
    Returns:
        None"""
    
    replays = [file for file in os.listdir(dirty_replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    for replay in replays:
        #check to see if the replay is already saved
        if replay in os.listdir(clean_replays_location):
            print("Replay already processed")
            continue
        else:
            #get the replay text
            replay_text = get_file_contents(dirty_replays_location + "/" + replay)

            processed_replay = clean_replay(replay_text)
            #check to see if the replay is already saved
            write_to_file(processed_replay, clean_replays_location + "/" + replay)
            print("Cleaned replay " + replay)


def clean_replay(replay_file_contents):
    """Process a replay
    
    Args:
        replay_file_contents: The contents of the replay file
    
    Returns:
        The processed replay as a string"""
    #split the replay into lines
    replay_lines = replay_file_contents.split("\n")

    #find the name of the players and store them to variables
    #will be formatted as '|player|p1|player1name' or '|player|p2|player2name'
    player1_name = None
    player2_name = None

    for line in replay_lines:
        if line.startswith("|player|p1|"):
            player1_name = line.split("|")[3]
        elif line.startswith("|player|p2|"):
            player2_name = line.split("|")[3]
        if player1_name != None and player2_name != None:break

    #remove until the line '|clearpoke'
    #any information above this is player names, and rules.
    #since all replays are from the same ruleset, this is not needed
    clear_poke_index = replay_lines.index("|clearpoke")
    replay_lines = replay_lines[clear_poke_index + 1:]

    #remove anly lines that start with '|c|', '|t:|', '|upkeep', '|inactive', or '|raw'
    #'|c' is for chat, '|t' is for time, '|upkeep' is for the upkeep phase, and '|inactive' is for the inactive timer
    #these lines are not needed
    replay_lines = [line for line in replay_lines if not line.startswith("|c|") and not line.startswith("|t:|") and not line.startswith("|upkeep") and not line.startswith("|inactive") and not line.startswith("|raw")]

    for line in replay_lines:
        #replace any instances of the player names with 'p1' or 'p2'
        line = line.replace(player1_name, "p1")
        line = line.replace(player2_name, "p2")

    #create the return string. there should be a line break between each line
    return_string = "\n".join(replay_lines)
    return return_string
    

if __name__ == "__main__":
    process_replays("saved_replays_training/dirty_replays", "saved_replays_training/clean_replays")
