from bs4 import BeautifulSoup
import requests
import os
from file_io import write_to_file, get_file_contents

"""Module for scraping replays from pokemon showdown and saving them as .txt files"""

def process_links(link_file):
    """Process the links in a file
    
    Args:
        link_file: The file containing the links
        
    Returns:
       """
    #open the file
    with open(link_file, "r") as file:
        #read the file
        links = file.readlines()
        #remove the newline characters
        links = [link.strip() for link in links]

    #variables for the location of the files for easy changing
    #location = "saved_replays_training/dirty_replays/"
    location = "saved_replays_testing/dirty_replays/"

    
    #loop through the links
    for link in links:
        if link[link.find("gen9ou"):] in os.listdir(location):
            print("Replay already saved")
            
            if get_file_contents(location + link[link.find("gen9ou")] + ".txt") == "Could not connect":
                #this means the replay was not scraped successfully, try again
                print("Replay not scraped successfully, trying again")
                
                replay = scrape_replay(link)
                
                if replay == None: continue
                
                else:
                    write_to_file(replay, location + link[link.find("gen9ou"):] + ".txt")
                    print("Saved replay " + link[link.find("gen9ou"):] + ".txt")
            
            continue
        else:
            replay = scrape_replay(link)
            
            if replay == None: continue
            
            else:
                write_to_file(replay, location + link[link.find("gen9ou"):] + ".txt")
                print("Saved replay " + link[link.find("gen9ou"):] + ".txt")


def scrape_replay(link):
    """Scrapes a replay from a link and saves it as a .txt file
    
    Args: link: The link to the replay
    
    Returns: The text of the replay"""
    #check to make sure the link is valid
    response = requests.get(link)
    if response.status_code != 200:
        print("Invalid link")
        return None
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        return(soup.text)


if __name__ == '__main__':
    #Replay links file variables for easy changing
    #replay_links_file = "saved_replays_training/replay_links.txt"
    replay_links_file = "saved_replays_testing/replay_links.txt"
    process_links(replay_links_file)