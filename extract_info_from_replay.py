""""Module: extract_info_from_replay.py
This file contains functions for extracting information from replays. This includes extracting the pokemon, their moves and player ratings."""
import file_io
import re
import os
from type_matchup_tester import get_resistances, get_weaknesses


def extract_pokemon(player, replay_log_contents):
    """Gets the pokemon of a given player
    
    Args:
        player: The player to get the pokemon of
        replay_log_contents: The log of the replay
    
    Returns:
        A list of the pokemon of the player"""

    #get the pokemon of the player
    #lines that define this will look like "|poke|player|pokemon_name"
    #get all the lines that define the pokemon
    pokemon_lines = [line for line in replay_log_contents.split("\n") if line.startswith("|poke|" + player + "|")]

    #now get the pokemon names
    player_teams = [line.split("|")[3] for line in pokemon_lines]

    #remove any gender information. Will be after a comma in the pokemon name
    player_teams = [re.sub(",.*", "", pokemon) for pokemon in player_teams]

    return player_teams


def extract_player_pokemon_moves(player, player_team, replay_log_contents):
    """Gets the moves of a given player's pokemon
    
    Args:
        player: The player to get the pokemon of
        player_team: The team of the player
        replay_log_contents: The log of the replay
        
    Returns:
        A dictionary of a player's pokemon and their moves"""
    
    player_team_dict = {}
    for pokemon in player_team:
        #get the moves of the pokemon
        #lines that define this will look like "|move|playera: pokemon_name|move_name|playera: target_pokemon_name"
        #get all the lines that define the moves
        move_lines = [line for line in replay_log_contents.split("\n") if line.startswith("|move|" + player + "a: " + pokemon + "|")]
        #now get the moves
        pokemon_moves = [line.split("|")[3] for line in move_lines]

        #be sure to clear out any duplicates
        pokemon_moves = list(set(pokemon_moves))
        if len(pokemon_moves) < 4:
            #fill the rest of the moves with empty strings
            for i in range(4 - len(pokemon_moves)):
                pokemon_moves.append("")

        #add the pokemon and their moves to the dictionary
        player_team_dict[pokemon] = pokemon_moves
    
    return player_team_dict


def give_advantage_content_only(replay_log_contents):
    """Gets the advantage of one player over the other
    This function only needs the replay log contents
    
    Args:
        replay_log_contents: The log of the replay

    Returns:
        The player with the advantage. p1 or p2"""
    
    player1_team = extract_pokemon("p1", replay_log_contents)
    player2_team = extract_pokemon("p2", replay_log_contents)

    return give_advantage(player1_team, player2_team)


def give_advantage(player1_team, player2_team):
    """Gets the advantage of one player over the other
    
    Args:
        player1_team: The team of player 1
        player2_team: The team of player 2
        
    Returns:
        The player with the advantage. p1 or p2"""

    for pokemon in player1_team:
        total_resistances_player1 = len(get_resistances(pokemon))
        total_weaknesses_player1 = len(get_weaknesses(pokemon))
    
    for pokemon in player2_team:
        total_resistances_player2 = len(get_resistances(pokemon))
        total_weaknesses_player2 = len(get_weaknesses(pokemon))
    
    if total_weaknesses_player1 > total_weaknesses_player2:
        return "p2"
    elif total_weaknesses_player1 < total_weaknesses_player2:
        return "p1"
    elif total_resistances_player1 > total_resistances_player2:
        return "p1"
    else:
        return "p2"



if __name__ == "__main__":
    #look through all files in the saved_replays_training/clean_replays folder
    for replay in os.listdir("saved_replays_training/clean_replays"):
        print("Processing " + replay)
        if replay != ".DS_Store":   
            #get the replay text
            replay_text = file_io.get_file_contents("saved_replays_training/clean_replays/" + replay)
            #if the first line in replay_text is a comment, skip this file
            if replay_text.startswith("#"):
                print("Advantage already found for " + replay)
                continue
            else:
                #add the advantage to the top of the file as a comment
                print("Adding advantage to " + replay)
                file_io.write_to_file("# advantage = " + give_advantage_content_only(replay_text) + "\n" + replay_text, "saved_replays_training/clean_replays/" + replay)        
    print("Done with training replays")


    #look through all files in the saved_replays_testing/clean_replays folder
    for replay in os.listdir("saved_replays_testing/clean_replays"):
        print("Processing " + replay)
        if replay != ".DS_Store":
            #get the replay text
            replay_text = file_io.get_file_contents("saved_replays_testing/clean_replays/" + replay)
            #if the first line in replay_text is a comment, skip this file
            if replay_text.startswith("#"):
                print("Advantage already found for " + replay)
                continue
            else:
                #add the advantage to the top of the file as a comment
                file_io.write_to_file("# advantage = " + give_advantage_content_only(replay_text) + "\n" + replay_text, "saved_replays_testing/clean_replays/" + replay)
                print("Added advantage to " + replay)
    print("Done with testing replays")