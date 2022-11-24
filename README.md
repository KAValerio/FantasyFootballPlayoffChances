# FantasyFootballPlayoffChances
Quick little script that I threw together to test how likely you are to make the playoffs with a certain number of wins in Fantasy Football. 

This isn't the most efficient code that I have ever written, I just threw it together in a morning while I was stressing that I wasn't going to make the playoffs haha.

Adjustable params:
  - n_weeks: number of weeks (games) in the season
  - n_teams: number of teams in the league
  - n_playoff: number of teams that make the playoffs
  - n_sims: number of simulations to run

This is for a PPR league. For half PPR, change the scale in the f_rdm function to 15. For std scoring, I'd suggest using 10. I would recommend tinkering with this first though as I have only tested it for PPR!
