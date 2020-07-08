import os
import pandas as pd

try:
    WORKING_ROOT = os.path.dirname(os.path.abspath(__file__))
except WindowsError:
    WORKING_ROOT = os.getcwd()

"""
Read the UFC fights data from https://github.com/cunhafh/UFC_bout_prediction.
Credit: Felipe Cunha
"""


def win_lose_data(fights_df):
    fights_df = fights_df.drop(fights_df.columns[0], axis=1)
    losing_fighters = fights_df.iloc[:, 0:15]
    winning_fighters = fights_df.iloc[:, 15:32]

    winning_fighters.columns = winning_fighters.columns.str.replace(r'.1', '')

    index_row = pd.DataFrame({col: [n] for n, col in enumerate(losing_fighters)})
    pd.concat([index_row, winning_fighters], ignore_index=True)
    pd.concat([index_row, losing_fighters], ignore_index=True)
    return winning_fighters, losing_fighters


UFC_fights = pd.read_csv(f"{WORKING_ROOT}/data/UFC_fights.csv")
winners_df, losers_df = win_lose_data(UFC_fights)
