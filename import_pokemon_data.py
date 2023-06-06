"""Module: import_pokemon_data.py
This file contains functions for importing data about Pokemon, attacks, and abilities. This includes importing the Pokemon's stats, moves, and types."""

import pandas as pd

def import_pokemon_data():
    """This function will import the pokemon data from the csv file
    Args:
        None
        
    Returns:
        A dataframe containing the pokemon data"""
    return pd.read_csv("pokemon_data.csv")

def import_attack_data():
    """This function will import the move data from the csv file
    Args:
        None
        
    Returns:
        A dataframe containing the move data"""
    return pd.read_csv("attack_data.csv")

def import_ability_data():
    """This function will import the ability data from the csv file
    Args:
        None
        
    Returns:
        A dataframe containing the ability data"""
    return pd.read_csv("ability_data.csv")

def import_type_matchup_data():
    """This function will import the type matchup data from the csv file
    Args:
        None
        
    Returns:
        A dataframe containing the type matchup data"""
    return pd.read_csv("type_matchups.csv", index_col=0)


def get_pokemon_base_stats(pokemon):
    """This function will return the base stats of a pokemon
    Args:
        pokemon: The name of the pokemon
        
    Returns:
        The base stats of the pokemon"""
    pokemon_data = import_pokemon_data()
    #This will be in the order base_stat_total, attack, defense, special_attack, special_defense, speed
    return pokemon_data[pokemon_data["Name"] == pokemon].iloc[0, 4:10].tolist()

    

if __name__ == "__main__":
    print(import_pokemon_data())
    print(import_attack_data())
    print(import_ability_data())
    print(import_type_matchup_data())
    print(get_pokemon_base_stats("Bulbasaur"))