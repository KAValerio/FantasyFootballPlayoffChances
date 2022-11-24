
# %%

import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 200)


def make_day(teams, day):
    # https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm

    day %= (len(teams) - 1)
    if day:
        teams = teams[:1] + teams[-day:] + teams[1:-day]
    half = len(teams) // 2
    return list(zip(teams[:half], teams[half:][::-1]))


def make_schedule(teams, n_weeks):
    assert not len(teams) % 2, "Number of teams must be even!"

    random.shuffle(teams)
    schedule = [make_day(teams, day) for day in range(n_weeks)]

    return schedule


def make_records(teams):
    prods = np.linspace(10, -10, len(teams))
    proj = {team: prods[team - 1] for team in teams}

    d1 = pd.DataFrame(0, index=teams, columns=['wins', 'losses'])
    d2 = pd.Series(proj).rename('proj')
    records = pd.concat([d2, d1], axis=1)
    return records


def run_week(schedule, records):
    for week in range(len(schedule)):
        games = schedule[week]
        for i, j in games:
            pi = records['proj'][i] + f_rdm()
            pj = records['proj'][j] + f_rdm()
            if pi > pj:
                records.loc[i, 'wins'] += 1
                records.loc[j, 'losses'] += 1
            else:
                records.loc[j, 'wins'] += 1
                records.loc[i, 'losses'] += 1


def run_season(n_weeks, n_teams, n_playoffs):
    teams = list(range(1, n_teams + 1))

    schedule = make_schedule(teams, n_weeks)

    records = make_records(teams)

    run_week(schedule, records)

    dsort = records.sort_values('wins', ascending=False)
    inwins = dsort.iloc[n_playoffs - 1]['wins']
    nout = dsort.iloc[n_playoffs:]['wins'].eq(inwins).sum()
    nin = dsort.iloc[:n_playoffs]['wins'].eq(inwins).sum()

    mostwins = records['wins'].max()
    leastwins = records['wins'].min()

    return [inwins, nin, nout, mostwins, leastwins]


# %%
def f_rdm(scale=20):  # default teams range from -10 to +10
    return np.random.normal(scale=scale, loc=0)


def main():
    n_weeks = 14
    n_teams = 14
    n_playoffs = 8

    n_sims = 500

    dresults = pd.DataFrame(
        columns=['nWins', 'nAbove', 'nBelow', 'mostWins', 'leastWins'])

    for sim in tqdm(range(n_sims)):
        output = run_season(n_weeks, n_teams, n_playoffs)
        dresults.loc[sim] = output

    dresults['odds'] = dresults['nBelow'] / dresults['nAbove']
    dresults['odds'] = dresults['nAbove'] / \
        (dresults['nAbove'] + dresults['nBelow'])

    for i in np.sort(dresults['nWins'].unique()):
        omn = dresults.loc[dresults['nWins'].eq(i)]['odds'].mean()
        print(f'-- odds with {i} wins: {omn.round(2)}')

    dresults['mostWins'].value_counts(dropna=False).sort_index()

    return dresults


if __name__ == '__main__':
    dresults = main()

# %%
