# Development Notes

## Data

We need 4 tranches of data, any data available in one must be available in all

### Static
Training, 1 year + consecutive
Dev, 1-3 month subset of training, this is used for public leaderboard scoring, participants have full access to this
Hold-out, 1-3 month subset of training, this will be used for the final scoring, participants never see this

### Live
Live: 10 consecutive days, 20th-30th of April 2024

## Submissions
We can't use kaggle because they don't allow prizes (unless we can meet someone from kaggle)

Participants will fork our git repo and the push their code to a team repo. We will pull that code down, run it against different datasets and display the outcomes on a web application. Participants will choose a final submission for the live portion of the competition.

This system will have 3 main components:

1. repo poller

This code will check each repo every minute for any new submissions. If it sees any it will send a notification to the running component.

2. runner

This system will take a repourl, pull it down, validate it, then run it against a particular dataset (using a simulated battery). All outputs, such as console logs and scores will be saved to a database (or s3 or something).

3. display

This will be a web application accessible to anyone with an API key. It display a public leaderboard, and for each participant it will show them the outputs of every submission they have made (scoring as well as console logs). It also displays the status of the runner and repo poller.
