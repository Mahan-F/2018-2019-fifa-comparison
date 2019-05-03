# Import pandas
import numpy as np
import pandas as pd
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


def check_id(row):
    print(row.name)
    id18 = row['ID']

    id19 = data19.loc[data19['ID'] == id18]

    if id19.size == 0:
        return True
    return False

# Done
def overall(id = None):
    def compare_overall(row):
        overall2018 = row['Overall']

        new_stats = data19.loc[data19['ID'] == row['ID']]['Overall']
        row = pd.Series({'Name': row['Name'], 'Overall 2018': overall2018})
        if new_stats.size > 0:
            row['Overall 2019'] = new_stats.tolist()[0]
            row['Overall Difference'] = new_stats.tolist()[0] - overall2018
            return row
        else:
            row['Overall 2019'] = np.NaN
            row['Overall Difference'] = np.NaN
            return row

    if id:
        player = data18[data18['ID'] == id]
        result = pd.DataFrame(player.apply(compare_overall, axis=1))
    else:
        result = pd.DataFrame(data18.apply(compare_overall, axis=1))

    return result


def acceleration():
    DataFrame = pd.DataFrame()

    for i in range(MAX):

        accel2018 = float(data18.loc[i]['Acceleration'])

        accel2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Acceleration']
        if newStats.size > 0:
            accel2019 = newStats.tolist()[0]
        else:
            accel2019 = np.NaN

        maxImprove = accel2019 - accel2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], '2018': accel2018, '2019': accel2019, 'Acceleration Improv.': maxImprove}, ignore_index=True)

    print(DataFrame[['Player Name', 'Acceleration Improv.']][DataFrame['Acceleration Improv.'] == DataFrame['Acceleration Improv.'].max()])


def agility():
    DataFrame = pd.DataFrame()

    for i in range(MAX):
        agil2018 = float(data18.loc[i]['Agility'])

        agil2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Agility']
        if newStats.size > 0:
            agil2019 = newStats.tolist()[0]
        else:
            agil2019 = np.NaN

        maxImprove = agil2019 - agil2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], '2018': agil2018, '2019': agil2019, 'Agility Improv.': maxImprove}, ignore_index=True)

    print(DataFrame[['Player Name', 'Agility Improv.']][DataFrame['Agility Improv.'] == DataFrame['Agility Improv.'].max()])


def finishing():
    DataFrame = pd.DataFrame()

    for i in range(MAX):
        fin2018 = float(data18.loc[i]['Finishing'])

        fin2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Finishing']
        if newStats.size > 0:
            fin2019 = newStats.tolist()[0]
        else:
            fin2019 = np.NaN

        maxImprove = fin2019 - fin2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], '2018': fin2018, '2019': fin2019, 'Finishing Improv.': maxImprove}, ignore_index=True)
    print(DataFrame[['Player Name', 'Finishing Improv.']][
                  DataFrame['Finishing Improv.'] == DataFrame['Finishing Improv.'].max()])

# Done
def oldest():
    """
    Returns the oldest player of each year along with their age and position
    :return: void
    """
    print('In which position are the oldest players (eg. Goalkeepers)?')

    oldest18 = data18.loc[data18['Age'] == data18['Age'].max()]
    print('Oldest Player of 2018 is ' + oldest18.iloc[0]['Name'] + ' with the age of ' + str(oldest18.iloc[0]['Age']) +
          ' with the position: ' + oldest18.iloc[0]['Position'])

    oldest19 = data19.loc[data19['Age'] == data19['Age'].max()]
    print('Oldest Player of 2019 is ' + oldest19.iloc[0]['Name'] + ' with the age of ' +
          str(oldest19.iloc[0]['Age']) + ' with the position: ' + oldest19.iloc[0]['Position'])

# Done
def value_change():
    """
    Print a list of top 10 players with the most increase/decrease in their value
    """
    print('Which players had the most change in value and why? is it based on their overall improvement?')

    data19['Value'] = data19['Value'].map(lambda x: x.lstrip('€'))
    data18['Value'] = data18['Value'].map(lambda x: x.lstrip('€'))

    data18['Value'] = (data18['Value'].replace(r'[KM]+$', '', regex=True).astype(float) *
                       data18['Value'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1)
                       .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

    data19['Value'] = (data19['Value'].replace(r'[KM]+$', '', regex=True).astype(float) *
                       data19['Value'].str.extract(r'[\d\.]+([KM]+)', expand=False).fillna(1)
                       .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

    def link_values(row):

        value18 = row[['Value', 'Overall']]

        new_stats = data19.loc[data19['ID'] == row['ID']]
        new_stats = new_stats[['Value', 'Overall']]

        row = pd.Series({'ID': row['ID'], 'Name': row['Name'], 'Value 2018': value18['Value'], 'Overall 2018': value18['Overall']})
        if new_stats.size > 0:
            new_stats = new_stats.values[0]
            row['Value 2019'] = new_stats[0]
            row['Overall 2019'] = new_stats[1]
            row['Overall Difference'] = new_stats[1] - value18['Overall']
            return row
        else:
            row['Value 2019'] = np.NaN
            row['Overall 2019'] = np.NaN
            row['Overall Difference'] = np.NaN
            return row

    result = pd.DataFrame(data18.apply(link_values, axis=1))
    result = result.dropna(axis='rows')

    change = pd.DataFrame({'ID': result['ID'], 'Name': result['Name'], 'Value Change': result['Value 2019'] - result['Value 2018'], 'Overall Change': result['Overall Difference']})

    change = change.sort_values(by=['Value Change'], ascending=False)
    most_increase = change.head(10)
    most_decrease = change.tail(10).iloc[::-1]

    print('List of players with the most increase in value: ')
    print(most_increase)
    print('List of players with the most decrease in value: ')
    print(most_decrease)


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

    # def link_values(row):
    #
    #     value18 = row[['Club', 'Overall', 'Value']]
    #
    #     new_stats = data19.loc[data19['ID'] == row['ID']]
    #     new_stats = new_stats[['Club', 'Overall', 'Value']]
    #
    #     row = pd.Series({'Name': row['Name']})
    #     if new_stats.size > 0:
    #         new_stats = new_stats.values[0]
    #         row['Club Changed'] = new_stats[0] != value18['Club']
    #         row['Overall Increased'] = new_stats[1] > value18['Overall']
    #         row['Value Increased'] = new_stats[2] > value18['Value']
    #         return row
    #     else:
    #         row['Club Changed'] = np.NaN
    #         row['Overall Increased'] = np.NaN
    #         row['Value Increased'] = np.NaN
    #         return row
    #
    # result = pd.DataFrame(data18.apply(link_values, axis=1))
    #
    # result = result.where(result['Club Changed'] == True)
    # result = result.dropna(axis='rows')
    # result = result.sort_values(by=['Name'], ascending=True)
    # print(result)
    #
    # increased_overall = result.loc[result['Overall Increased'] == True]
    # increased_value = result.loc[result['Value Increased'] == True]
    #
    # increased_overall_percent = (len(increased_overall.index) / len(result.index)) * 100
    # increased_value_percent = (len(increased_value.index) / len(result.index)) * 100
    #
    # print(str("%.2f" % increased_overall_percent) + '% of the players who changed club had an increase in overall rating.')
    # print(str("%.2f" % increased_value_percent) + '% of the players who changed club had an increase in value.')


def retired():
    """
    What players that were playing in 2018 did not play in 2019 (retired?)
    :return: List of retired playered with their positions
    """
    print('All the players that have retired in 2019.')

    result = data_joined.loc[data_joined['Name_19'].isnull()]
    print(result[['Name_18', 'Age_18', 'Position_18']])

    result = result.groupby('Position_18').mean()
    print('\nList of all positions with the average age of retired players from the position')
    print(result['Age_18'])

