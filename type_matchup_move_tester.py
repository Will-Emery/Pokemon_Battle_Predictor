import pandas as pd
import numpy as np

def type_matchup(move_type, pokemon_type, pokemon_type2):
    """
    Returns the effectiveness of a move of type `move_type` against a Pokemon of type `pokemon_type`.

    Args:
        move_type: The type of the move.
        pokemon_type: The primary type of the Pokemon.
        pokemon_type2: The secondary type of the Pokemon.


    Returns:
        A float representing the effectiveness of the move.
    """

    type_matchup_df = pd.read_csv("type_matchups.csv", index_col=0)

    # Check if the move type is valid
    if move_type not in type_matchup_df.columns:
        raise ValueError("Invalid move type: " + move_type)

    # Check if the Pokemon type is valid
    if pokemon_type not in type_matchup_df.index:
        raise ValueError("Invalid Pokemon type: " + str(pokemon_type))
    
    if not pd.isna(pokemon_type2) and pokemon_type2 not in type_matchup_df.index:
        raise ValueError("Invalid Pokemon type: " + str(pokemon_type2))

    # Get the effectiveness of the move
    move_type_matchup = type_matchup_df.loc[move_type, pokemon_type]

    classify_effectiveness(move_type, pokemon_type, move_type_matchup)

    if not pd.isna(pokemon_type2):
        move_type_matchup *= type_matchup_df.loc[move_type, pokemon_type2]
        classify_effectiveness(move_type, pokemon_type2, move_type_matchup)

    return move_type_matchup


def classify_effectiveness(move_type, pokemon_type, effectiveness):
    """
    Returns an effectiveness classification for a single type of a pokemon
    
    Args:
        move_type: The type of the move.
        pokemon_type: The type of the Pokemon.
        effectiveness: The effectiveness of the move against the Pokemon.
        
    Returns:
        None
    """

    if effectiveness == 0:
       print(str(move_type) + " does not effect " + str(pokemon_type) + ".")
    elif effectiveness == 0.5:
        print(str(move_type) + " is not very effective against " + str(pokemon_type) + ".")
    elif effectiveness == 1:
        print(str(move_type) + " is normally effective against " + str(pokemon_type) + ".")
    elif effectiveness == 2:
        print(str(move_type) + " is super effective against " + str(pokemon_type) + ".")
    else:
        raise ValueError("Invalid effectiveness: " + str(effectiveness))

def main():
    move_df = pd.read_csv("attack_data.csv")
    pokemon_df = pd.read_csv("pokemon_data.csv")

    # Pick a random move
    move = pd.DataFrame(move_df).sample(n=1)
    move_name = move["Name"].values[0]
    move_type = move["Type"].values[0]

    # Pick a random Pokemon
    pokemon = pd.DataFrame(pokemon_df).sample(n=1)
    pokemon_name = pokemon["Name"].values[0]
    pokemon_type = pokemon["Type1"].values[0]
    pokemon_type2 = pokemon["Type2"].values[0] if pokemon["Type2"].values[0] != None else None

    print("Move: " + move_name + " Type: " + str(move_type))
    print("Pokemon: " + pokemon_name + " Type: " + str(pokemon_type) + " Type2: " + str(pokemon_type2))

    # Get the type matchup
    type_matchup_result = type_matchup(move_type, pokemon_type, pokemon_type2)
    print("Type Matchup: " + str(type_matchup_result))

if __name__ == "__main__":
    main()