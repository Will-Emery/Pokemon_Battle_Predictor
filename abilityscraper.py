"""Module: abilityscraper.py
This file contains functions for scraping the ability data from the website. This includes scraping the ability name, description, and effect."""

import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

def make_data_frame():
    """Make a dataframe for the abilties"""
    #list of attacks formatted with name, type, damage type, Power, Accuracy, PP
    return pd.DataFrame(columns = ['Name', 'Description', 'Effect'])


def scrape_ability_info():
    """Scrape the ability data from the website"""
    ability_df = make_data_frame()

    link = "https://pokemondb.net/ability"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all table rows (<tr>) within the desired table
    table_rows = soup.find_all("tr")

    # Extract data from each table row
    for row in table_rows:
        # Find the columns within the row (<td>) and extract relevant data
        columns = row.find_all("td")
        if len(columns) >= 3:
            name = str(columns[0].find("a").text.strip())
            description = str(columns[2].text.strip())
            effect = str(add_effect(name))
            
            print("Name: " + name + " Description: " + description + " Effect: " + effect)
            ability_df = ability_df._append({'Name': name, 'Description': description, 'Effect': effect}, ignore_index=True)
    
    return ability_df


def add_effect(ability_name):
    """Add the effect of the ability to the dataframe"""
    #if there is a space in the name, replace it with a dash
    ability_name = ability_name.replace(" ", "-")
    #remove any apostrophes
    ability_name = ability_name.replace("'", "")

    link = "https://pokemondb.net/ability/" + ability_name
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    #should be in the first <p> tag in the first <div> tag
    effect = soup.find("div", class_="grid-row").find("p").text.strip()
    #trim any text after the text "Game descriptions"
    effect = effect.split("Game descriptions")[0]
    return effect


if __name__ == "__main__":
    start_time = time.time()
    ability_df = scrape_ability_info()
    ability_df.to_csv("ability_data.csv", index=False)
    print(ability_df)