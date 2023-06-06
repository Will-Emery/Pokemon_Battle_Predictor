"""Module: modeling.py
This file contains functions for modeling the data. This includes training the model, and testing the model."""

import pandas as pd
import numpy as np
import extract_info_from_replay
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

def get_advantage_from_log(replay_log):
    """Gets the player with the advantage from a given replay.
    
    Args:
        replay_log: The log of the replay
    
    Returns:
        The player with the advantage. Either p1 or p2"""
    
    #will be on the first line of the replay. 
    #formatted as "# advantage = p1" or "# advantage = p2"
    replay_lines = replay_log.split("\n")
    advantage_line = [line for line in replay_lines if line.startswith("# advantage = ")]
    return advantage_line[0].split(" ")[3]


def import_training_data(replays_location):
    """Import the data from the replays
    Args:
        replays_location: The location of the replays
    Returns:
        A dataframe containing the data"""
    replays = [file for file in os.listdir(replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    #create a dataframe to store the data
    data = pd.DataFrame(columns=["replay_name", "replay", "winner"])

    for replay in replays:
        #get the replay text
        replay_text = file_io.get_file_contents(replays_location + "/" + replay)

        #get the winner
        winner = get_winner(replay_text)

        #add the data to the dataframe
        data = data._append({"replay_name": replay, "replay": replay_text, "winner": winner}, ignore_index=True)

    return data


def import_testing_data_random(replays_location):
    """Import the data from a random testing replay
    Args:
        replays_location: The location of the replays
    Returns:
        A dataframe containing the data"""
    
    data = pd.DataFrame(columns=["replay_name", "replay", "winner"])
    
    replays = [file for file in os.listdir(replays_location) if file.endswith(".txt")]
    print(f"Found {len(replays)} replays")

    #pick a random replay to test on
    replay = replays[np.random.randint(0, len(replays))]
    print(f"Testing on replay {replay}")

    #get the replay text
    replay_text = file_io.get_file_contents(replays_location + "/" + replay)
    #remove a line containing the text |win|p1 or |win|p2
    replay_text = re.sub(r"\|win\|p[1-2]", "", replay_text)

    data = data._append({"replay_name": replay, "replay": replay_text, "winner": None}, ignore_index=True)

    return data


def import_testing_data(replays_location):
    """Import the datat from the testing replays
    
    Args:
        replays_location: The location of the replays
    Returns:
        A dataframe containing the data"""
    
    data = pd.DataFrame(columns=["replay_name", "replay", "winner"])
    replays = [file for file in os.listdir(replays_location) if file.endswith(".txt")]

    #loop through the replays
    for replay in replays:
        #check to see if the replay is in the list of training replays
        #get the replay text
        replay_text = file_io.get_file_contents(replays_location + "/" + replay)
        #remove a line containing the text |win|p1 or |win|p2
        replay_text = re.sub(r"\|win\|p[1-2]", "", replay_text)

        data = data._append({"replay_name": replay, "replay": replay_text, "winner": None}, ignore_index=True)
    
    print(f"Found {len(data)} replays for testing")

    return data


def train_model(data):
    """Train the model
    Args:
        data: The data to train the model on
    Returns:
        The trained model and the vectorizer"""
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data["replay"])
    y = data["winner"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))

    return clf, vectorizer


def test_model_single(clf, vectorizer, test_data):
    """Test the model on a single replay
    Args:
        clf: The trained model
        vectorizer: The vectorizer used to vectorize the data
    
    Returns:
        The trained model"""
    
    X = vectorizer.transform(test_data["replay"])
    y_pred = clf.predict(X)
    print(f"Predicted winner: {y_pred[0]}")
    Actual_winner = get_winner(file_io.get_file_contents("saved_replays_testing/clean_replays/" + test_data["replay_name"][0]))
    print(f"Actual winner: {Actual_winner}")

    return clf


def test_model_bulk(clf, vectorizer, test_data):
    """Test the model on a bulk of replays
    Args:
        clf: The trained model
        vectorizer: The vectorizer used to vectorize the data
        test_data: The data to test the model on
    
    Returns:
        The trained model"""
    total = len(test_data)
    num_correct = 0

    for index, row in test_data.iterrows():
        replay_text = row["replay"]
        X = vectorizer.transform([replay_text])  # Pass the replay text as a list
        y_pred = clf.predict(X)
        actual_winner = get_winner(file_io.get_file_contents("saved_replays_testing/clean_replays/" + row["replay_name"]))
        print(f"Replay: {row['replay_name']} \t Predicted winner: {y_pred[0]} \t Actual winner: {actual_winner}")

        if y_pred[0] == actual_winner:
            print("Prediction correct")
            num_correct += 1

    print(f"Percent correct: {num_correct / total}")

    return clf
    

if __name__ == "__main__":
    train_data_df = import_training_data("saved_replays_training/clean_replays")
    # test_data_df = import_testing_data_random("saved_replays_testing/clean_replays")
    test_data_bulk_df = import_testing_data("saved_replays_testing/clean_replays")

    train_result = train_model(train_data_df)
    # clf = test_model_single(train_result[0], train_result[1], test_data_df)
    clf = test_model_bulk(train_result[0], train_result[1], test_data_bulk_df)
