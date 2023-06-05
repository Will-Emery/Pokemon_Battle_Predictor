import requests
from bs4 import BeautifulSoup
import time
from file_io import append_to_file

"""Module for scraping replay links from pokemon showdown and saving them as .txt files"""

def get_children_links(parent_link):
    """Gets the children links of a parent link
    
    Args:
        parent_link: The link to the parent page
        
    Returns:
        A list of links to the children pages
    """ 
    #get the html of the parent page
    response = requests.get(parent_link)
    soup = BeautifulSoup(response.content, "html.parser")

    #find all the links to children matches on the page
    #these will be <a href="link">text</a> tags inside of a <li> tag
    children_links = []
    for link in soup.find_all("li"):
        #check if the link is a child link
        if link.find("a") != None:
            #get the link
            link = link.find("a")["href"]
            #add the link to the list of children links
            children_links.append(link)

    #remove the first 8, these are not children links and are just links at the top of the parent page
    children_links = children_links[8:]

    #remove any duplicated links
    children_links = list(dict.fromkeys(children_links))

    #add the base url to the links
    return_links = []
    for link in children_links:
        updated_link = str('https://replay.pokemonshowdown.com/'+ link + ".log")
        return_links.append(updated_link)
    
    return return_links


if __name__ == '__main__':
    #get the links to the children pages
    children_links = get_children_links("https://replay.pokemonshowdown.com/search/?format=gen9ou&rating")
    
    #variables for the location of the file for easy changing
    #location = "saved_replays_training/replay_links.txt"
    location = "saved_replays_testing/replay_links.txt"

    #loop through the children links
    for link in children_links:
        if link not in open(location).read():
            print(link)
            append_to_file(link + '\n', location)
        else:
            print("Link already in file")
            print(link)

    while True:
        children_links = get_children_links("https://replay.pokemonshowdown.com/search/?format=gen9ou")
        for link in children_links:
            if link not in open(location).read():
                print(link)
                append_to_file(link + '\n', location)
            else:
                print("Link already in file")
                print(link)
            
        #sleep for 5 minutes
        print("Sleeping for 10 minutes")
        time.sleep(600)