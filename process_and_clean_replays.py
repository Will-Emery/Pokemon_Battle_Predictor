"""Module: process_clean_replays.py
This file contains functions for processing and cleaning replays. This includes removing the turn number, removing the player names, and removing the pokemon nicknames."""
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

    total_bad_replays = 0
    total_cleaned_replays = 0

    for replay in replays:
        #check to see if the replay is already saved
        if replay in os.listdir(clean_replays_location):
            print("Replay already processed")
            continue
        if get_file_contents(dirty_replays_location + "/" + replay) == "Could not connect":
            print("Replay not scraped")
            print("Skipping replay. Please run scrape_replays.py to scrape the replay")
            total_bad_replays += 1
            continue
        else:
            #get the replay text
            print("Processing replay " + replay)
            replay_text = get_file_contents(dirty_replays_location + "/" + replay)

            processed_replay = clean_replay(replay_text)
            #check to see if the replay is already saved
            write_to_file(processed_replay, clean_replays_location + "/" + replay)
            print("Cleaned replay " + replay)
            total_cleaned_replays += 1
    
    print(f"Total bad replays: {total_bad_replays}")
    print(f"Total cleaned replays: {total_cleaned_replays}")


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
            print(f"Player 1 name: {player1_name}")
        elif line.startswith("|player|p2|"):
            player2_name = line.split("|")[3]
            print(f"Player 2 name: {player2_name}")
        if player1_name != None and player2_name != None:break

    #remove until the line '|clearpoke'
    #any information above this is player names, and rules.
    #since all replays are from the same ruleset, this is not needed
    clear_poke_index = replay_lines.index("|clearpoke")
    replay_lines = replay_lines[clear_poke_index + 1:]

    #remove anly lines that start with '|c|', '|t:|', '|l|', or '|j| '|upkeep', '|inactive', '|raw'
    #'|c' is for chat, '|t' is for time, '|upkeep' is for the upkeep phase, and '|inactive' is for the inactive timer
    #these lines are not needed
    replay_lines = [line for line in replay_lines if not line.startswith("|c|") and not line.startswith("|t:|") and not line.startswith("|upkeep") and not line.startswith("|inactive") and not line.startswith("|raw") and not line.startswith("|l|") and not line.startswith("|j|")]

    clean_player_lines = []
    for line in replay_lines:
        clean_player_lines.append(check_for_playername(line, player1_name, player2_name))

    #create the return string. there should be a line break between each line
    return_string = "\n".join(clean_player_lines)
    return return_string


def check_for_playername(line, player1_name, player2_name):
    """Will remove the playername from the line if it is present
    
    Args:
        line: The line to check
        player1_name: The name of player 1
        player2_name: The name of player 2
    
    Returns:
        The line with the player name removed"""
    if player1_name in line or player2_name in line:
        line = line.replace(player1_name, "p1")
        line = line.replace(player2_name, "p2")
    return line


def clean_win_information(clean_replays_location):
    """Removes the winning information from the replay
    
    Args:
        clean_replays_location: The location of the clean replays
    
    Returns:
        None"""
    replays = [file for file in os.listdir(clean_replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    for replay in replays:
        #get the replay text
        print("Processing replay " + replay)
        replay_text = get_file_contents(clean_replays_location + "/" + replay)

        processed_replay = remove_win_information(replay_text)
        #check to see if the replay is already saved
        write_to_file(processed_replay, clean_replays_location + "/" + replay)
        print("Removed win info from replay " + replay)


def remove_win_information(replay_file_contents):
    """Removes the winning information from the replay
    
    Args:
        replay_file_contents: The contents of the replay file
    Returns:
        The processed replay as a string"""
    
    #split the replay into lines
    replay_lines = replay_file_contents.split("\n")

    #remove the lines that start with '|win|p1' or '|win|p2'
    #these lines are not needed for testing
    replay_lines = [line for line in replay_lines if not line.startswith("|win|p1") and not line.startswith("|win|p2")]
    #remove any lines that have the text 'forfeit' in them
    #these lines are not needed for testing
    replay_lines = [line for line in replay_lines if "forfeit" not in line]
    #create the return string. there should be a line break between each line
    return_string = "\n".join(replay_lines)
    return return_string


if __name__ == "__main__":
    #variables for easy location switching
    # dirty_replays_location = "saved_replays_training/dirty_replays"
    # clean_replays_location = "saved_replays_training/clean_replays"
    dirty_replays_location = "saved_replays_testing/dirty_replays"
    clean_replays_location = "saved_replays_testing/clean_replays"
    process_replays(dirty_replays_location, clean_replays_location)

    # testing = input("Was this for testing? (y/n)")
    # while testing != "y" and testing != "n":
    #     testing = input("Please enter y or n")
    # if testing == "y":
    #     print("cleaning winning information from replays")
    #     clean_win_information(clean_replays_location)

