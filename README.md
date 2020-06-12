### AZChess

#### Introduction
This repo holds my (in development) implementation of the AlphaZero algorithm 
from [Mastering Chess and Shogi by Self-Play with a General Reinforcement 
Learning Algorithm](https://arxiv.org/pdf/1712.01815.pdf). The goal is to 
train a chess AI purely via self-play and providing only the game state and 
rules. The implementation was also inspired by the fantastic LeelaChessZero 
project.

#### Purpose

The purpose of this project is to develop a Chess AI via Reinforcement Learning 
as a personal exercise in Deep Reinforcement Learning. The intended output from 
this project is the lessons that will be learned in developing the codebase. 
The goal is *not* to develop a strong chess AI. Once the implementation is tried 
and tested, I will attempt to train the network locally and with minimal cloud 
compute, to see how well the AI plays after training for a short time.

For a fantastic project with incredibly strong play, see LeelaChessZero 
which is set apart by its utilisation of distributed training.

#### Complete
* Complete chessboard representation (2020-06-13)

#### To do (*in progress*)

* *Design & Implement MCTS class*
* Build self-play workers
* Design neural network architecture
* Decide pipeline 

#### Ambitious Goals
These goals are for potential improvement after the core functionality is built.
* Rebuild self-play workers and training for multi-threading
* Rebuild self-play codebase in C++ for speed
