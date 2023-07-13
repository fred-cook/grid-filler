# grid-filler
A program to fit theme words from a small dictionary into a crossword grid, while maintaining the ability to complete the rest of the grid from a full dictionary

## Installation

Clone the repository and make sure you poetry installed using `pip install poetry`

Change directory into the repo and run `poetry shell` to spawn a new virtual environment.

Run `poetry install` and add the flags `--only main` if you don't need dev dependencies.

## Glossary

`grid`: The `NumPy` array which stores
the letters/blocks/empty spaces which make up the crossword.

`Light`: A space in which a word can go in the grid.

`CrosswordGrid`: A lightweight class wrapper with methods to make the `grid` and find all of the `Light`s in the grid

### To do list
- [ ] Save which lights are across and down when they get made.
- [ ] Calculate and store the number and direction of lights