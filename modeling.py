"""Module: modeling.py
This file contains functions for modeling the data. This includes training the model, and testing the model."""

import pandas as pd
import numpy as np
import os
import re
import file_io
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

def get_winner(replay_log):
    """Gets the winner of a given replay
    Args:
        replay_log: The log of the replay
    Returns:
        The winner of the replay. Either p1 or p2"""
    #winner will be found on the line with "|win|p1" or "|win|p2"
    replay_lines = replay_log.split("\n")
    winner_line = [line for line in replay_lines if line.startswith("|win|")]
    return winner_line[0].split("|")[2]        


def import_training_data(replays_location):
    """Import the data from the replays
    Args:
        replays_location: The location of the replays
    Returns:
        A dataframe containing the data"""
    replays = [file for file in os.listdir(replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    #create a dataframe to store the data
    data = pd.DataFrame(columns=["replay", "winner"])

    for replay in replays:
        #get the replay text
        replay_text = file_io.get_file_contents(replays_location + "/" + replay)

        #get the winner
        winner = get_winner(replay_text)

        #add the data to the dataframe
        data = data._append({"replay": replay_text, "winner": winner}, ignore_index=True)

    return data

def import_testing_data(replays_location):
    """Import the data from the testing replays
    Args:
        replays_location: The location of the replays
    Returns:
        A dataframe containing the data"""
    
    data = pd.DataFrame(columns=["replay", "winner"])
    
    replays = [file for file in os.listdir(replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    #pick a random replay to test on
    replay = replays[np.random.randint(0, len(replays))]
    print(f"Testing on replay {replay}")

    #get the replay text
    replay_text = file_io.get_file_contents(replays_location + "/" + replay)
    data  = data._append({"replay": replay_text, "winner": None}, ignore_index=True)

    return data

def train_model(data):

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data["replay"])
    y = data["winner"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))

    return clf, vectorizer


def test_model(clf, vectorizer, test_data):
    X = vectorizer.transform(test_data["replay"])
    y_pred = clf.predict(X)
    print(y_pred)
    
    return clf

if __name__ == "__main__":
    train_data_df = import_training_data("saved_replays_training/clean_replays")
    test_data_df = import_testing_data("saved_replays_testing/clean_replays")

    train_result = train_model(train_data_df)
    clf = test_model(train_result[0], train_result[1], test_data_df)
