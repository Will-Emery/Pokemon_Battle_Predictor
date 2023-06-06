# Pokemon Battle Predictor

This is a program which will interfact with Pokemon Showdown replays to predict the outcome of a battle. This model was trained on gen9ou battles so it's success with other generations and tiers is not guaranteed. To break down the naming scheme, gen9ou means generation 9 overused. This means that the model was trained on battles from the 9th generation of Pokemon games and the overused tier. The overused tier is the most popular tier in the game and is the one that most people play.

As of right now, the predictor is averaging about 60% accuracy. This is in part due to the complexity of the game and the fact that the model is only trained on 2,061 battles. Future work for this would be to train on some more battles and try to incorperate more into the model than just total type weaknesses and resistances. The ground work for this has already been done.

The model is capable of taking in the base states of each Pokemon and the moves that they have. This is not currently being used because with my limited knowledge of machine learning, I was not able to figure out how to incorperate this into the model. I have left the code capable of doing this that it can be used in the future.

## Getting Started

Clone the repository and run the following command to install the required packages:
`pip install -r requirements.txt`

The actual model is found in the modeling.py file. The model is trained on the data found in the saved_replays_training folder. The model is then tested on the data found in the saved_replays_testing folder.

To run this file and train the model, run the following command:
`python modeling.py`
