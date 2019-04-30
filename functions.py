# Import pandas
import numpy as np
import pandas as pd

# reading csv file
data18 = pd.read_csv("2018.csv")
data19 = pd.read_csv("2019.csv")

MAX = len(data18.index)
SAMPLE = 150

# Removing the un-needed columns
columns = ['Photo', 'Flag', 'Club Logo']
data18.drop(columns, inplace=True, axis=1)

# Renaming columns to match
data18.rename(columns={'Preferred Positions': 'Position'}, inplace=True)

# Strip trailing whitespace from end of Positions
data18['Position'] = data18['Position'].str.strip()

# print(list(data18.columns.values))


def check_id(row):
    id18 = row['ID']

    id19 = data19.loc[data19['ID'] == id18]

    if id19.size == 0:
        return True
    return False

# Done
def overall(id =None):
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

# Done
def age():
    """
    Print a list of top 10 players with the most overall rating difference along with their age
    :return:
    """
    print('Is the overall improvement based on age?')

    def link_values(row):

        value18 = row['Overall']

        new_stats = data19.loc[data19['ID'] == row['ID']]
        new_stats = new_stats[['Age', 'Overall']]

        row = pd.Series({'Name': row['Name']})
        if new_stats.size > 0:
            new_stats = new_stats.values[0]
            row['Age'] = new_stats[0]
            row['Overall Difference'] = new_stats[1] - value18
            return row
        else:
            row['Age'] = np.NaN
            row['Overall Difference'] = np.NaN
            return row

    result = pd.DataFrame(data18.apply(link_values, axis=1))
    result = result.dropna(axis='rows')

    result = result.sort_values(by=['Overall Difference'], ascending=False)
    highest_overall = result.head(10)

    print('List of players with the most overall rating along with their age: ')
    print(highest_overall)

# Done
def nationality_overall():
    """
    Prints a list of all countries with their overall average difference
    """
    print('Which nationality has the best overall average?')

    def link_values(row):

        value18 = row[['Nationality', 'Overall']]

        new_stats = data19.loc[data19['ID'] == row['ID']]['Overall']

        row = pd.Series({'Nationality': row['Nationality'], 'Overall 2018': value18['Overall']})
        if new_stats.size > 0:
            new_stats = new_stats.values
            row['Overall 2019'] = new_stats[0]
            row['Overall Difference'] = new_stats[0] - value18['Overall']
            return row
        else:
            row['Overall 2019'] = np.NaN
            row['Overall Difference'] = np.NaN
            return row

    result = pd.DataFrame(data18.apply(link_values, axis=1))
    result = result.dropna(axis='rows')

    result = result.groupby('Nationality').mean()
    result = result.sort_values(by=['Overall Difference'], ascending=False)

    print(result)

# Done
def potential_to_actual():
    print('Is the potential of the 2018 dataset correspond to the overall of the 2019 dataset?')

    def link_values(row):

        value18 = row['Potential']

        new_stats = data19.loc[data19['ID'] == row['ID']]['Overall']

        row = pd.Series({'Name': row['Name']})
        if new_stats.size > 0:
            new_stats = new_stats.values
            row['Potential was correct'] = value18 == new_stats[0]
            return row
        else:
            row['Potential was correct'] = np.NaN
            return row

    result = pd.DataFrame(data18.apply(link_values, axis=1))
    result = result.dropna(axis='rows')

    result = result.sort_values(by=['Name'], ascending=True)

    print(result)

    correct = result.loc[result['Potential was correct'] == True]
    correct_percent = (len(correct.index) / len(result.index)) * 100
    print(str("%.2f" % correct_percent) + '% of the potential predictions were correct.')
    # DataFrame = pd.DataFrame()
    # for i in range(MAX):
    #
    #     potential2018 = data18.loc[i]['Potential']
    #
    #     overall2019 = -1
    #     newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Overall']
    #     if newStats.size > 0:
    #         overall2019 = newStats.tolist()[0]
    #     else:
    #         overall2019 = np.NaN
    #
    #     differencePotential = overall2019 - potential2018
    #     DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], 'Potential 2018': potential2018, 'Overall 2019': overall2019, 'Difference': differencePotential}, ignore_index=True)
    #
    # print(DataFrame)


def over_30():
    print('Do players with age over 30 have a decrement on their overall?')

    DataFrame = pd.DataFrame()
    for i in range(MAX):

        overall2018 = float(data18.loc[i]['Overall'])

        overall2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Overall']
        if newStats.size > 0:
            overall2019 = newStats.tolist()[0]
        else:
            overall2019 = np.NaN

        differencePotential = float(overall2019) - overall2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], 'Age': data18.loc[i]['Age'], 'Overall 2018': overall2018, 'Overall 2019': overall2019, 'Difference': differencePotential}, ignore_index=True)

    print(DataFrame[DataFrame.Age > 30])


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

    return in_both, len(in_both)


def retired():
    """
    What players that were playing in 2018 did not play in 2019 (retired?)
    :return: List of retired playered with their positions
    """
    import time
    start = time.time()

    # Took 13.61 seconds
    result = data18.apply(check_id, axis=1)
    print(data18[result])

    # Took 117.3 seconds
    # for i in range(MAX):
    #     new_stats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]
    #     if new_stats.size == 0:
    #         result = result.append(data18.iloc[i], ignore_index=True)
    # print(result)

    end = time.time()
    print('time: ')
    print(end - start)
