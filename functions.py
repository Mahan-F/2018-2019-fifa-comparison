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

# Strip trailing whitespace from end of preferred Positions
data18['Preferred Positions'] = data18['Preferred Positions'].str.strip()


def check_id(row):
    id18 = row['ID']

    id19 = data19.loc[data19['ID'] == id18]

    if id19.size == 0:
        return True
    return False


def overall():
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

    result = pd.DataFrame(data18.apply(compare_overall, axis=1))
    #
    # for i in range(MAX):
    #     overall2018 = data18.loc[i]['Overall']
    #
    #     new_stats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Overall']
    #     if new_stats.size > 0:
    #         overall2019 = new_stats.tolist()[0]
    #     else:
    #         overall2019 = np.NaN
    #
    #     difference_overall = overall2019 - overall2018
    #     result = result.append({'Player Name': data18.loc[i]['Name'], '2018': overall2018, '2019': overall2019, 'Difference': difference_overall}, ignore_index=True)

    print(result)


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
    result = pd.DataFrame()

    for i in range(MAX):
        result = result.append({
            'Player Name': data18.loc[i]['Name'],
            'Position': data18.loc[i]['Preferred Positions'],
            'Age': data18.loc[i]['Age']
        }, ignore_index=True)

    oldest18 = result.loc[result['Age'] == result['Age'].max()].values[0]
    print('Oldest Player of 2018 is ' + oldest18[1] + ' with the age of ' + str(oldest18[0]) +
          ' with the position: ' + oldest18[2])

    result = pd.DataFrame()

    for i in range(MAX):
        result = result.append({
            'Player Name': data19.loc[i]['Name'],
            'Position': data19.loc[i]['Position'],
            'Age': data19.loc[i]['Age']
        }, ignore_index=True)

    oldest19 = result.loc[result['Age'] == result['Age'].max()].values[0]
    print('Oldest Player of 2019 is ' + oldest19[1] + ' with the age of ' +
          str(oldest19[0]) + ' with the position: ' + oldest19[2])


def value_change():
    print('Which players had the most change in value  and why? is it based on their overall improvement?')

    DataFrame = pd.DataFrame()
    data19['Value'] = data19['Value'].map(lambda x: x.lstrip('€').rstrip('MK'))
    data18['Value'] = data18['Value'].map(lambda x: x.lstrip('€').rstrip('MK'))


    for i in range(MAX):
        overall2018 = float(data18.loc[i]['Value'])

        overall2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Value']
        if newStats.size > 0:
            overall2019 = newStats.tolist()[0]
        else:
            overall2019 = np.NaN

        differenceOverAll = float(overall2019) - overall2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], '2018': overall2018, '2019': overall2019, 'Value': differenceOverAll}, ignore_index=True)

    print('Player with most increase on his value:')
    print(DataFrame[['Player Name', 'Value']][DataFrame['Value'] == DataFrame['Value'].max()])
    print('Player with most decrease on his value:')
    print(DataFrame[['Player Name', 'Value']][DataFrame['Value'] == DataFrame['Value'].min()])


def nationality_overall():
    print('Which nationality has the best overall average?')
    print('The best overall average  for each Nation on 2018 are:')
    DataFrame = pd.DataFrame()
    for i in range(MAX):
        nationality2018 = data18.loc[i]['Nationality']

        DataFrame = DataFrame.append({'Nationality': data18.loc[i]['Nationality'], 'Overall': data18.loc[i]['Overall']}, ignore_index=True)


    print(DataFrame.groupby(['Nationality'], as_index=False).mean())

    print('The best overall average  for each Nation on 2019 are:')
    DataFrame = pd.DataFrame()
    for i in range(MAX):

        nationality2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Nationality']
        if newStats.size > 0:
            nationality2019 = newStats.tolist()[0]
        else:
            nationality2019 = np.NaN

        DataFrame = DataFrame.append({'Nationality': data19.loc[i]['Nationality'], 'Overall': data19.loc[i]['Overall']}, ignore_index=True)

    print(DataFrame.groupby(['Nationality'], as_index=False).mean())


def potential_to_actual():
    print('Is the potential of the 2018 dataset correspond to the overall of the 2019 dataset?')

    DataFrame = pd.DataFrame()
    for i in range(MAX):

        potential2018 = data18.loc[i]['Potential']

        overall2019 = -1
        newStats = data19.loc[data19['ID'] == data18.loc[i, 'ID']]['Overall']
        if newStats.size > 0:
            overall2019 = newStats.tolist()[0]
        else:
            overall2019 = np.NaN

        differencePotential = overall2019 - potential2018
        DataFrame = DataFrame.append({'Player Name': data18.loc[i]['Name'], 'Potential 2018': potential2018, 'Overall 2019': overall2019, 'Difference': differencePotential}, ignore_index=True)

    print(DataFrame)


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
