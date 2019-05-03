import pandas as pd
import time
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'

plt.close('all')

# Removing the un-needed columns
columnsNotIncluded = ['Unnamed: 0', 'Joined', 'Photo', 'Flag', 'Club Logo']
column_dtypes = {
    'Age': 'int64',
    'Overall': 'int64',
    'Potential': 'int64'
}

# reading csv file
data18 = pd.read_csv("2018.csv", dtype=column_dtypes, usecols=lambda column: column not in columnsNotIncluded, low_memory=False)
data19 = pd.read_csv("2019.csv", dtype=column_dtypes, usecols=lambda column: column not in columnsNotIncluded, low_memory=False)

MAX = len(data18.index)

# Renaming columns to match
data18.rename(columns={'Preferred Positions': 'Position'}, inplace=True)

# Strip trailing whitespace from end of Positions
data18['Position'] = data18['Position'].str.strip()

# Convert the Value columns to only numbers so they can be compared
data19['Value'] = data19['Value'].map(lambda x: x.lstrip('€'))
data18['Value'] = data18['Value'].map(lambda x: x.lstrip('€'))

data18['Value'] = (data18['Value'].replace(r'[KM]+$', '', regex=True).astype(float) *
                   data18['Value'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1)
                   .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

data19['Value'] = (data19['Value'].replace(r'[KM]+$', '', regex=True).astype(float) *
                   data19['Value'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1)
                   .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

# Join the 2 datasets together for fast comparisons
data_joined = data18.set_index('ID').join(data19.set_index('ID'), how='left', lsuffix="_18", rsuffix="_19")


def overall():
    """
    Compare the overall score of each player from 2018 to 2019
    Times:
        Old way with .apply()               = 39.78967571258545
        New way with the joined dataframe   = 0.05585455894470215
    """

    result = data_joined.loc[(data_joined['Name_19'].isnull() != True)]  # All players that are not retired

    result['Overall Difference'] = result['Overall_19'] - result['Overall_18']
    result = result.sort_values(by=['Overall Difference'], ascending=False)

    most_increase = result.head(10)
    most_decrease = result.tail(10).iloc[::-1]

    print('\nList of players with the most increase in Overall: ')
    print(most_increase[['Name_19', 'Overall Difference']])
    print('\nList of players with the most decrease in Overall: ')
    print(most_decrease[['Name_19', 'Overall Difference']])


def oldest():
    """
    Returns the oldest player of each year along with their age and position
    """
    print('In which position are the oldest players (eg. Goalkeepers)?')

    oldest18 = data18.loc[data18['Age'] == data18['Age'].max()]
    print('Oldest Player of 2018 is ' + oldest18.iloc[0]['Name'] + ' with the age of ' + str(oldest18.iloc[0]['Age']) +
          ' with the position: ' + oldest18.iloc[0]['Position'])

    oldest19 = data19.loc[data19['Age'] == data19['Age'].max()]
    print('Oldest Player of 2019 is ' + oldest19.iloc[0]['Name'] + ' with the age of ' +
          str(oldest19.iloc[0]['Age']) + ' with the position: ' + oldest19.iloc[0]['Position'])


def value_change():
    """
    Print a list of top 10 players with the most increase/decrease in their value
    Times:
        Old way with .apply()               = 74.08851599693298
        New way with the joined dataframe   = 0.057877540588378906
    """
    print('Which players had the most change in value and why? is it based on their overall improvement?')

    result = data_joined.loc[(data_joined['Name_19'].isnull() != True)]  # All players that are not retired

    result['Overall Difference'] = result['Overall_19'] - result['Overall_18']
    result['Value Difference'] = result['Value_19'] - result['Value_18']
    result = result.sort_values(by=['Value Difference'], ascending=False)

    most_increase = result.head(10)
    most_decrease = result.tail(10).iloc[::-1]

    print('\nList of players with the most increase in value: ')
    print(most_increase[['Name_19', 'Value Difference', 'Overall Difference']])
    print('\nList of players with the most decrease in value: ')
    print(most_decrease[['Name_19', 'Value Difference', 'Overall Difference']])


def age():
    """
    Print a list of top 10 players with the most overall rating difference along with their age
    Times:
        Old way with .apply()               = 52.20204257965088
        New way with the joined dataframe   = 0.053879499435424805
    """
    print('Is the overall improvement based on age?')

    result = data_joined.loc[(data_joined['Name_19'].isnull() != True)]  # All players that are not retired

    result['Overall Difference'] = result['Overall_19'] - result['Overall_18']
    result = result.sort_values(by=['Overall Difference'], ascending=False)
    highest_overall = result.head(10)

    print('List of players with the most overall rating along with their age: ')
    print(highest_overall[['Name_19', 'Age_19', 'Overall Difference']])
    print('\nAverage age of the fastest improving players is ', highest_overall['Age_19'].mean())


def nationality_overall():
    """
    Prints a list of all countries with their overall average difference
    Times:
        Old way with .apply()               = 51.73658752441406
        New way with the joined dataframe   = 0.03989005088806152
    """
    print('Which nationality has the best overall average?')

    result = data_joined.loc[(data_joined['Name_19'].isnull() != True)]  # All players that are not retired

    result = result.groupby('Nationality_19')[['Overall_19', 'Overall_18']].mean()
    result['Overall Difference'] = result['Overall_19'] - result['Overall_18']
    result = result.sort_values(by=['Overall Difference'], ascending=False)

    print(result[['Overall_18', 'Overall_19', 'Overall Difference']])


def potential_to_actual():
    """
        Times:
            Old way with .apply()               = 28.260369539260864
            New way with the joined dataframe   = 0.029920101165771484
    """
    print('Is the potential of the 2018 dataset correspond to the overall of the 2019 dataset?')

    result = data_joined.loc[(data_joined['Name_19'].isnull() != True)] # All players that are not retired
    result['Potential was correct'] = result['Potential_18'] == result['Overall_19']
    print(result[['Name_19', 'Potential was correct']].head(), '\n')

    correct = result.loc[result['Potential was correct'] == True]
    correct_percent = (len(correct.index) / len(result.index)) * 100
    print(str("%.2f" % correct_percent) + '% of the potential predictions were correct.')


def over_30():
    """
        Times:
            Old way with .apply()               = 49.60598850250244
            New way with the joined dataframe   = 0.038903236389160156
    """
    print('Do players with age over 30 have a decrement on their overall?')

    result = data_joined.loc[(data_joined['Club_19'].isnull() != True) & (data_joined['Age_18'] > 30)]
    result['Overall Decreased'] = result['Overall_19'] < result['Overall_18']
    print(result[['Name_18', 'Overall Decreased']])

    had_decrease = result.loc[result['Overall Decreased'] == True]
    decrease_percent = (len(had_decrease.index) / len(result.index)) * 100

    print(str("%.2f" % decrease_percent) + '% of the players over the age of 30 had a decrease in their overall rating.')


def top_10():
    """
    Compares the top 10 players of the 2 years to see what players appeared in both
    :return: A list of player names that were in top 10 of both years
    """
    print('The top 10 ranked players of 2018 are the same with the 2019?')
    top18 = pd.DataFrame()
    top19 = pd.DataFrame()

    in_both = []

    for i in range(10):
        top18 = top18.append({'Player Name': data18.loc[i]['Name'], 'Overall 2018': data18.loc[i]['Overall']}, ignore_index=True)
        top19 = top19.append({'Player Name': data19.loc[i]['Name'], 'Overall 2019': data19.loc[i]['Overall']}, ignore_index=True)

    for i in range(10):
        if top18.iloc[i]['Player Name'] in top19['Player Name'].values:
            in_both.append(top18.iloc[i]['Player Name'])

    print(in_both)
    print(str(len(in_both)) + ' players appeared on the top 10 charts of both years.')


def club_change():
    print('Does the change of club affect the value and overall rating of a player?')

    result = data_joined.loc[(data_joined['Club_19'].isnull() != True) & (data_joined['Club_19'] != data_joined['Club_18'])]
    result['Overall Increased'] = result['Overall_19'] > result['Overall_18']
    result['Value Increased'] = result['Value_19'] > result['Value_18']
    print(result[['Name_18', 'Overall Increased', 'Value Increased']].head(), '\n')

    increased_overall = result.loc[result['Overall Increased'] == True]
    increased_value = result.loc[result['Value Increased'] == True]

    increased_overall_percent = (len(increased_overall.index) / len(result.index)) * 100
    increased_value_percent = (len(increased_value.index) / len(result.index)) * 100

    print(str("%.2f" % increased_overall_percent) + '% of the players who changed club had an increase in overall rating.')
    print(str("%.2f" % increased_value_percent) + '% of the players who changed club had an increase in value.')


def retired():
    """
    What players that were playing in 2018 did not play in 2019 (retired?)
    :return: List of retired playered with their positions
    """
    print('Players that have retired in 2019.')

    result = data_joined.loc[data_joined['Name_19'].isnull()]
    print(result[['Name_18', 'Age_18', 'Position_18']].head())

    result = result.groupby('Position_18')['Age_18'].mean()
    print('\nList of all positions with the average age of retired players from the position')
    print(result.head())


def execute_all():
    start = time.time()

    print('\n\n------------------------------------------------------------------------------------------------------')
    overall()
    print('\n\n------------------------------------------------------------------------------------------------------')
    oldest()
    print('\n\n------------------------------------------------------------------------------------------------------')
    value_change()
    print('\n\n------------------------------------------------------------------------------------------------------')
    age()
    print('\n\n------------------------------------------------------------------------------------------------------')
    nationality_overall()
    print('\n\n------------------------------------------------------------------------------------------------------')
    potential_to_actual()
    print('\n\n------------------------------------------------------------------------------------------------------')
    over_30()
    print('\n\n------------------------------------------------------------------------------------------------------')
    top_10()
    print('\n\n------------------------------------------------------------------------------------------------------')
    club_change()
    print('\n\n------------------------------------------------------------------------------------------------------')
    retired()
    print('\n\n------------------------------------------------------------------------------------------------------')

    end = time.time()
    print('time: ' + str(end - start))
