# Creating a Minesweeper Artificial Intelligence using Constraint Satisfaction Problem Solving Techniques and Probabilistic Inference.

## Introduction 
The goal of this project was to create an Artificial Intelligence (AI) capable of solving Minesweeper in every difficulty, those being Beginner (8x8 with 10 mines), Intermediate (16x16 with 40 mines), and Expert (30x16 with 99 mines). Minesweeper is a game where the player is given a completely hidden board and must flag all bombs in the game by using the numbers on the tiles that display the count of all bombs in the tiles around itself. If the player is successful, then they win the game. If the player uncovers a bomb, they lose.

As the AI must play the game like a regular player would, it must be able to observe the board in its current state, uncover tiles that it deems safe, and flag tiles that it believes to be bombs, all in an attempt to solve the game and win. This AI must be able to win on all three difficulties outlined above.

## Background 
This experiment has been completed multiple times in the past. Becerra [1], in their Algorithm Approaches to Playing Minesweeper thesis, outlined and created an AI using Connected Components Constraint Satisfaction Problem (CSP) and coupled subsets CSP, both of which had a high Beginner and Intermediate win rate, that being 90.85% and 74.18% for the Connected Components CSP, and 91.25% and 75.94% on their coupled subsets CSP. However, they found that the AI would perform worse in Expert mode, with their win rate being 25.96% and 32.90% respectively. From looking at this, it can be inferred that using solely CSP can solve Minesweeper with a high win rate, except for Expert difficulty, which would struggle.

Therefore, CSP should be used in conjunction with another technique. A CSP Minesweeper solver was also written to implement CSP solving with heuristics to find the best possible solution when the CSP solver could not [2], instead of relying on probabilistic inference. This solver reported a 76.4% win rate on Expert difficulty using this Heuristic CSP (HCSP), compared to the CSP-PGMS implementation [3], which resulted in a 45% win rate on Expert.

Another AI was written using rule-based symbolic AI and CSP [4] instead, which, while using different difficulties and board sizes, reported a 70% win rate on Advanced (24x24 with 99 mines), where it would average around 90% uncovered tiles, which meant that a vast majority of their losses were from the AI failing to find a safe tile based off of luck. It also had high win rates on Beginner with a 95% win rate, and on Intermediate, an 85% win rate. When compared to a solely CSP AI written by the same person, the AI would have a lower win percentage, and an extremely high time-out percentage, time-out being when the AI could not find a safe tile or bomb tile, with it being a 0% win rate on Advanced, and a 70% Timeout percentage.
 
## AI Method and Tools
From the research and readings done, it was determined that the ideal way to model and create this AI was from using CSP solving techniques, and an additional algorithm to handle cases where the CSP would fail, as seen in the solely CSP based AIs from [1] and [4]. Therefore, Probabilistic Inference was chosen to simulate the way a human would play Minesweeper. When a human player is out of moves to logically infer from the board, they turn to educated guesses. Using CSP and Probabilistic Inference, this AI is made to simulate the way a human would play Minesweeper and compare it to the other Minesweeper AIs.

 For the CSP, Google's OR-TOOLS' CP-SAT solver [5] was used. The CP-SAT solver works perfectly for solving Minesweeper, as a CSP requires variables, in this case Minesweeper's covered tiles, a domain, that being a Boolean 'is a bomb' or 'is not a bomb', and the constraints being the value on the tile indicating the amount of bombs in the neighbouring tiles. Therefore, by defining all three, the CP-SAT solver can return all possible solutions.

To implement this, it first iterates over every visible tile with a value and compares the value of that tile with the number of flags adjacent to it. If there are unknown tiles around, it stores that tile and the amount of bombs required for that 3x3 space into the constraints. It then uses a customised solution collector from the CP-SAT solver to find every possible solution. Then, if, in every possible configuration, a tile is never a bomb, it is stored as a safe move and executed, the same for a bomb to flag.

When the AI is out of moves to solve, it then uses probabilistic inference. It runs through all unknown neighbours and checks how many times that tile appeared in all possible solutions, then picks the tile with the lowest appearance as that would be the tile with the lowest probability of appearing. If it's safe, the AI has more information for the next time it runs the CSP solver.


## Evaluation Method
The initial method to evaluate the AI was to run the program multiple times and achieve a 'high' win rate on Beginner, 'decently high' on Intermediate, and at least a 50% win rate on Expert.

To better reflect the purpose of this project, the win rate of this AI will now be compared against the multiple Minesweeper AIs discussed earlier.

The HCSP Minesweeper AI in [2] had a win rate of 90.5% in Beginner, 76.4% in Intermediate, and 38.1% in Expert, with these results averaged over 105 games.

The CSP-only Minesweeper AI from [3] had a win rate of 80% in Beginner, 45% in Intermediate, and 34% in Expert.

Finally, the CSP and Logic Minesweeper AI [4] had a win rate of 95% in Beginner, 84% in Intermediate, and 70% in Expert, although this is a 24x24, 99 mine Expert instead of the standard 30x16.

Therefore, to call this AI successful, it must be able to achieve over an 83.5% win rate in Beginner, 68% win rate in Intermediate, and a 47.4% win rate in Expert, with these figures being the average of the win rates over the above three Minesweeper AIs. 



##Results
On the first initial sets of testing, where 1000 runs of each mode was done, both Beginner and Intermediate had 63% win rate, and Expert had a 49% win rate. To diagnose why the AI was failing so consistently, a 'flag%' was added, to track how far the AI got into the run before failing. As seen in Figure 1, the AI had around 20-30% of their games being lost to the first few turns. Therefore, the game itself, not the AI needed to be fixed. After adjusting the game to always keep the tile 1,1 and its surroundings safe, the 1000 runs were done again.

<img width="940" height="277" alt="Results of 1000 runs on Beginner, Intermediate, and Expert" src="https://github.com/user-attachments/assets/9dae9541-890d-4f9f-96fd-4f26fdd2cfe2" />

After another 1000 runs with the adjusted game, the AI, as seen in Figure 2, achieved an 83% win rate in Beginner and Intermediate, and a 67% win rate on Expert. Now, when looking at the flag%, a majority of the runs that lost typically lost on the last few flags, due to those being 50/50, or close to, guesses.

<img width="940" height="313" alt="Results of 1000 runs on Beginner, Intermediate, and Expert after fix" src="https://github.com/user-attachments/assets/d38f41b7-1e74-439f-a5f7-1390df30a374" />

 
## Conclusion
From the data seen in Figure 2, it is clear that the AI is sufficient at solving each level of difficulty. Using the evaluation criteria set earlier, the AI surpasses every criterion required of it. It achieved an 85% win rate on Beginner, above 83.5%, an 83% win rate on Intermediate, above the 68% win rate, and a 67.7% win rate on Expert, compared to the criterion 47.4%.

From the runs that the AI loses, it typically loses either in the last 10% of bombs unflagged, or at the start due to too many bombs near the starting location of the AI, meaning it cannot gather enough information to make certain guesses, and has to rely on the Probabilistic Inference to get further information.

Overall, the AI accomplishes what was set out to do; to use CSP solving techniques and Probabilistic Inference to win games in Minesweeper in all three modes. While it doesn't perform as well as expected in the Beginner modes, its high win rate in Expert (67%) means that the AI is still quite capable of clearing the game.

## Acknowledgements


When working on this assignment, Krupke's 'The CP-SAT Primer: Using and Understanding Google OR-Tools' CP-SAT Solver' document on Github [6] was essential in my understanding of the CP-SAT Solver, as it not only explained  most of the modelling and logging of the solver, but also code examples that could be referenced. 

Another major acknowledgement to be made is to the Pygame team who wrote up the documentation for PyGame [7], the library used in this assignment to create the Minesweeper game.

## References
[1] D., Becerra, "Algorithmic Approaches to Playing Minesweeper," Bachelor's thesis, Harvard College, United States, 2015. Accessed: Sep. 2, 2025. [Online]. Available: https://dash.harvard.edu/entities/publication/73120378-eb34-6bd4-e053-0100007fdf3b

[2] O., Buffet, C., Lee, W., Lin, and O., Teytaund. "Optimistic Heuristics for Minesweeper," ICS - International Computer Symposium - 2012, Dec 2012, Hualien, Taiwan. pp. 199-207. Accessed: Sep. 2, 2025. [Online]. Available: https://inria.hal.science/hal-00750577v2/document

[3] J., Ramsdell, "Programmer's Minesweeper," Khoury College of Computer Science. Accessed: Sep. 2, 2025. [Online]. Available: https://web.archive.org/web/20180220164809/http://www.ccs.neu.edu/home/ramsdell/pgms/

[4] “Minesweeper AI,” Stanford University. Accessed: Aug. 20, 2025. [Online]. Available: https://web.stanford.edu/class/archive/cs/cs221/cs221.1192/2018/restricted/posters/thowarth/poster.pdf

[5] “CP-SAT Solver.” Google OR-TOOLS. 2024. Accessed: Aug. 22, 2025. [Online]. Available: https://developers.google.com/optimization/cp/cp_solver

[6] D., Krupke, "The CP-SAT Primer: Using and Understanding Google OR-Tools' CP-SAT Solver." Accessed: Sep. 5, 2025. [Online]. Available: https://github.com/d-krupke/cpsat-primer?tab=readme-ov-file

[7] "Pygame Front Page" Pygame. Accessed: Aug. 15, 2025. [Online]. Available: https://www.pygame.org/docs/



 
## User Guide

To run:
	Ensure python is installed on your computer
	Use pip to download pygame and ortools, using the commands:
		python -m pip install pygame
		python -m pip install ortools
	Run the program
		python main.py

If any errors show up about missing libraries, try using pip again.

To build:
	As this project was done in PyCharm, this will show the configuration to build.
	Import all .pys into a project and set main.py to be the main file.
	In the terminal type:
		python -m pip install pygame
		python -m pip install ortools
	Double check in File > Settings > Project: <project name>, that ortools, pygame, and other libraries have been installed correctly.
	Run main.

To configure:
	In config.json, the difficulty, player, and speed can be set.
	Difficulty can be:
		BEGINNER - 8x8 with 10 bombs
		INTERMEDIATE - 16x16 with 40 bombs
		EXPERT - 24x24 with 99 bombs
	Player can be:
		HUMAN - if you want to play
		AI - if you want AI to play
	Speed can be:
		Any positive float value.
		This sets how fast the AI makes its moves. 0.0 for the fastest your CPU can handle

To get data:
	After running the program, a window will open. This shows the board and updates with the AI.
	After a win or loss, in the CLI it shows the win number, if it won, and the current win%.
	If the AI gets stuck for too long, press R to restart. This counts as a loss.
	To stop the AI, press ESC. In the CLI it will generate the final stats.
	In the same directory, it will also output  AI_stats.csv. This shows every run's Win or Loss, the total win% up to that run, and how many bombs it correctly flagged before it lost.

To play the game:
	If in config.json, player is 'HUMAN'
	Left click to reveal tile
	Right click to flag tile
	Press r to restart
	Press esc to stop the game.
