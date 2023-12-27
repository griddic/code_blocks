import pandas as pd 
import datetime 
from collections import defaultdict

def plot_tests_created():
    df = pd.read_csv('selected.csv')

    def to_week_number(smth):
        d = datetime.datetime.strptime(smth[:-1], "%Y-%m-%d")
        return d.isocalendar()[1]


    df['wn'] = df['period'].apply(to_week_number)

    week_max = max(df['wn'])
    week_min = min(df['wn'])

    df1 = df[df['wn'] > week_min]
    df1 = df1[df1['wn'] < week_max]

    di = defaultdict(int)
    for wn, count in zip(df1['wn'].to_list(), df1['total_requests'].to_list()):
        di[wn] += count

    l = sorted(list(di.items()))

    df = pd.DataFrame(l, columns=['week number', 'tests created'])
    df.set_index('week number', inplace=True)

    # return df

    df.plot().get_figure().savefig('plot.png')


def plot_trailes_created():
    df = pd.read_csv('selected_trails.csv')

    def to_week_number(smth):
        d = datetime.datetime.strptime(smth[:-1], "%Y-%m-%d")
        return d.isocalendar()[1]


    df['wn'] = df['period'].apply(to_week_number)

    week_max = max(df['wn'])
    week_min = min(df['wn'])

    df1 = df[df['wn'] > week_min]
    df1 = df1[df1['wn'] < week_max]

    di = defaultdict(int)
    for wn, count in zip(df1['wn'].to_list(), df1['total_requests'].to_list()):
        di[wn] += count

    l = sorted(list(di.items()))

    df = pd.DataFrame(l, columns=['week number', 'trailes created'])
    df.set_index('week number', inplace=True)
    # return df

    # print(df.head())
    df.plot().get_figure().savefig('plot_trailes.png')

df = plot_tests_created()
df1 = plot_trailes_created()
# df['trailed_created'] = df1['trailes created']
# df.plot().get_figure().savefig('plot.png')