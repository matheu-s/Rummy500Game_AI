
# Rummy500Game_AI - MCCFR

Using machine learning to create a super AI player for Rummy 500. 
* Algorithm used: Monte Carlo Counterfactual Regret Minimization.  
* GUI for playing the game Rummy 500 against the developed model.
* Only the two zero sum approach is considered. 




## How to play Rummy 500

#### Objective: 
Score points by forming melds (three or fours cards of the same rank) and runs (three or more consecutive cards of the same suit).
#### Gameplay:
Each player receives 13 random cards. One additional card is flipped on the table, forming the beginning of the discard pile. The game starts with the first players choosing to draw from the discard pile or the hidden deck. After this action, it can lay down melds on the table and end his turn by discarding one card from his hand. The game ends when hidden decks or one of the player's hand is empty.
#### Scoring:
* Ace-10. 5 points
* J-Q-K. 10 points.
#### Packages:
* pygame
* labml


## Reference

 - [Monte Carlo Sampling for Regret Minimization in Extensive Games](https://mlanctot.info/files/papers/nips09mccfr.pdf)
 - [CFR in Poker](https://nn.labml.ai/cfr/index.html)


