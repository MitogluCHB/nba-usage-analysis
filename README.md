# Denver Nuggets Usage Analysis (With/Without Nikola Jokic)

This is a beginner project that analyzes how player usage % changes when Nikola Jokic is playing for the Nuggets versus he is not

The goal is to explore how player role shifts using real NBA data and basic data analysis techniques in Python

## Project Overview

- get_usage.py

    * Fetches Denver Nuggets 2025/26 games using the NBA API 
    * Calculates player usage percentage per game
    * Determines whether Nikola Jokic played in a game
    * Saves processed data into a CSV file

- usage_main.py

    * Compares average player usage with and without Jokic
    * Calculates usage difference per player
    * Visualizes results using bar charts


## Usage Formula

Usage Formula is calculated using the formula: 

Usage % = 100 * ((FGA + 0.44 * FTA + TO) * (Team Minutes / 5))
/ (Player Minutes * (Team FGA + 0.44 * Team FTA + Team TO))

