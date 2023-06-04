import time
from bs4 import BeautifulSoup
import requests
import pandas as pd


def make_data_frame():
    """Make a dataframe for the scraped attacks"""
    #list of attacks formatted with name, type, damage type, Power, Accuracy, PP
    return pd.DataFrame(columns = ['Name', 'Type', 'Damage Type', 'Power', 'Accuracy', 'PP', 
                                   'Description', 'TM', 'Notes'])


def scrape_attack_data():
    """Scrape the attack data from the website"""
    attack_df = make_data_frame()

    link = "https://pokemondb.net/move/all"  # note, only for gen 1. can be changed
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all table rows (<tr>) within the desired table
    table_rows = soup.find_all("tr")

    # Extract data from each table row
    for row in table_rows:
        # Find the columns within the row (<td>) and extract relevant data
        columns = row.find_all("td")
        if len(columns) >= 8:
            notes = ""
            name = columns[0].find("a").text.strip()
            type = columns[1].find("a").text.strip()
           
            #case for none type for move_type
            if columns[2].find("img") == None:
                move_type = None
            else:
                move_type = columns[2].find("img")["alt"]

            #case for none type for power
            if columns[3].text.strip() == "—":
                power = None
            else:
                power = columns[3].text.strip()

            #case for none type for accuracy
            if columns[4].text.strip() == "∞":
                accuracy = "Not Checked"
            else:
                accuracy = columns[4].text.strip()
            
            pp = columns[5].text.strip()
            
            #case to aadd notes if pp is 1
            if pp == "1":
                notes = "Z-Move or Max Move"

            tm = columns[6].text.strip()

            description = columns[7].text.strip()

            # Print or store the extracted data as needed
            print("Name:", name)
            print("Type:", type)
            print("Move Type:", move_type)
            print("Power:", power)
            print("Accuracy:", accuracy)
            print("PP:", pp)
            print("TM:", tm)
            print("Description:", description)
            print("------------------")

            #now add the scraped data to the dataframe
            attack_df = attack_df._append({'Name': str(name), 'Type': str(type), 'Damage Type': str(move_type), 
                                           'Power': float(power), 'Accuracy': float(accuracy), 'PP': float(pp), 
                                           'Description': str(description), 'TM': tm, 'Notes': notes}, 
                                           ignore_index=True)
    return attack_df


if __name__ == "__main__":
    df = scrape_attack_data()
    df.to_csv('attack_data.csv', index=False)