import pandas as pd
import numpy as np
import random
import datetime
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 500)

df = pd.read_excel("Election polls results.xlsx")

df.drop(df.loc[:, df.columns.str.contains("Un")].columns.to_list(), 1, inplace=True)

# Define the mean and standard deviation of each candidate's vote share
erdo_mean = np.mean(df["Erdoğan"])
erdo_std = np.std(df["Erdoğan"])
kili_mean = np.mean(df["Kılıçdaroğlu"])
kili_std = np.std(df["Kılıçdaroğlu"])
ogan_mean = np.mean(df["Oğan"])
ogan_std = np.std(df["Oğan"])
ince_mean = np.mean(df["İnce"])
ince_std = np.std(df["İnce"])

# Define the number of simulations to run
num_simulations = 10000

# Define the number of days in the month
num_days = 30

# Initialize counters for each candidate's wins for each day
erdo_wins = [0] * num_days
kili_wins = [0] * num_days
ogan_wins = [0] * num_days
ince_wins = [0] * num_days

# Loop over each day in the month
for day in range(num_days):
    # Initialize counters for each candidate's wins for the current day
    erdo_wins_day = 0
    kili_wins_day = 0
    ogan_wins_day = 0
    ince_wins_day = 0

    # Run the Monte Carlo simulation for the current day
    for i in range(num_simulations):
        # Generate a random sample from the normal distribution for each candidate
        erdo_vote_share = random.normalvariate(erdo_mean, erdo_std)
        kili_vote_share = random.normalvariate(kili_mean, kili_std)
        ogan_vote_share = random.normalvariate(ogan_mean, ogan_std)
        ince_vote_share = random.normalvariate(ince_mean, ince_std)

        # Add a win to the candidate with the higher vote share in the simulation for the current day
        if erdo_vote_share > kili_vote_share and erdo_vote_share > ogan_vote_share and erdo_vote_share > ince_vote_share:
            erdo_wins_day += 1
        elif kili_vote_share > erdo_vote_share and kili_vote_share > ogan_vote_share and kili_vote_share > ince_vote_share:
            kili_wins_day += 1
        elif ogan_vote_share > erdo_vote_share and ogan_vote_share > kili_vote_share and ogan_vote_share > ince_vote_share:
            ogan_wins_day += 1
        else:
            ince_wins_day += 1

    # Store the percentage of wins for each candidate for the current day
    erdo_wins[day] = erdo_wins_day / num_simulations * 100
    kili_wins[day] = kili_wins_day / num_simulations * 100
    ogan_wins[day] = ogan_wins_day / num_simulations * 100
    ince_wins[day] = ince_wins_day / num_simulations * 100

# Plot the percentage of wins for each candidate for each day
plt.plot(range(num_days), erdo_wins, 'o-', label='Erdoğan')
plt.plot(range(num_days), kili_wins, 'o-', label='Kılıçdaroğlu')
plt.plot(range(num_days), ogan_wins, 'o-', label='Oğan')
plt.plot(range(num_days), ince_wins, '', label='İnce', linestyle='dashed')
plt.xlabel('Day')
plt.ylabel('Percentage of wins')
plt.title('Monte Carlo Simulation Results for 30 Days')
plt.legend()
plt.show()

# Plot a additional one
erdo_probs = np.array(erdo_wins)
kili_probs = np.array(kili_wins)
ogan_probs = np.array(ogan_wins)
ince_probs = np.array(ince_wins)
today = datetime.date.today()

# Define the days as the number of days from today to the election day
days = [(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]

# Create the fan chart
fig, ax = plt.subplots()
ax.stackplot(days, erdo_probs, kili_probs, ogan_probs, ince_probs, labels=['Erdoğan', 'Kılıçdaroğlu', 'Oğan', 'İnce'], alpha=0.7)
ax.legend(loc='upper left')
ax.set_title('Winning Probabilities for Each Candidate by Day')
ax.set_ylabel('Probability (%)')
# Set x-axis tick label spacing to 3
plt.xticks(range(0, len(days), 3))
plt.show()
