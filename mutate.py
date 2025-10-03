import pandas as pd
import os
import re

__all__ = ['mutate_data']


def mutate_data():
    if not os.path.exists('out'):
        os.mkdir('out')

    __mutate_fighter_data()
    __mutate_event_details()
    __mutate_fight_data()
    __mutate_fight_stats()
    __cleanup_all()


def __mutate_fighter_data():
    """
    Combine UFC fighter data keeping all records from both files.
    """

    df_details = pd.read_csv('ufc_fighter_details.csv')
    df_tott = pd.read_csv('ufc_fighter_tott.csv')

    # Outer join to keep all records
    combined_df = pd.merge(df_details, df_tott, on='URL', how='outer')

    if 'FIGHTER' in combined_df.columns:
        combined_df = combined_df.drop('FIGHTER', axis=1)

    combined_df = combined_df.replace('--', '')

    combined_df.to_csv('out/fighters.csv', index=False)


def __mutate_event_details():
    df_events = pd.read_csv('ufc_event_details.csv')

    df_events.rename(columns={'EVENT': 'NAME'}, inplace=True)

    df_events.to_csv('out/events.csv', index=False)


def __mutate_fight_data():
    df_fight_details = pd.read_csv('ufc_fight_details.csv')
    df_fight_results = pd.read_csv('ufc_fight_results.csv')

    combined_df = pd.merge(
        df_fight_details, df_fight_results, on='URL', how='outer')

    combined_df = combined_df.drop(columns=['EVENT_x', 'BOUT_x'])
    combined_df.rename(columns={'EVENT_y': 'EVENT',
                       'BOUT_y': 'BOUT'}, inplace=True)

    combined_df['URL'] = combined_df.pop('URL')

    combined_df.to_csv('out/fights.csv', index=False)


def __mutate_fight_stats():
    df_fight_stats = pd.read_csv('ufc_fight_stats.csv')

    rename_cols = {
        'KD': 'KNOCKDOWNS',
        'SIG.STR.': 'SIGSTRIKES',
        'SIG.STR. %': 'SIGSTRIKESPERCENT',
        'TOTAL STR.': 'TOTALSTRIKES',
        'TD': 'TAKEDOWNS',
        'TD %': 'TAKEDOWNSPERCENT',
        'SUB.ATT': 'SUBMISSIONATTEMPTS',
        'REV.': 'REVERSALS',
        'CTRL': 'CONTROLTIME',
        'HEAD': 'HEADSTRIKES',
        'BODY': 'BODYSTRIKES',
        'LEG': 'LEGSTRIKES'
    }

    # Rename cols
    df_fight_stats.rename(columns=rename_cols, inplace=True)

    # Remove 'Round {x}' text from ROUND col
    df_fight_stats['ROUND'] = df_fight_stats['ROUND'].str.replace(
        'Round ', '', regex=False)

    # Extract '{x} of {y}' stats into separate columns
    df_fight_stats[['SIGSTRIKESHIT', 'SIGSTRIKESATTEMPTED']
                   ] = df_fight_stats['SIGSTRIKES'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('SIGSTRIKES', axis=1, inplace=True)
    df_fight_stats.drop('SIGSTRIKESPERCENT', axis=1, inplace=True)

    df_fight_stats[['TOTALSTRIKESHIT', 'TOTALSTRIKESATTEMPTED']
                   ] = df_fight_stats['TOTALSTRIKES'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('TOTALSTRIKES', axis=1, inplace=True)

    df_fight_stats[['TAKEDOWNSHIT', 'TAKEDOWNSATTEMPTED']
                   ] = df_fight_stats['TAKEDOWNS'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('TAKEDOWNS', axis=1, inplace=True)
    df_fight_stats.drop('TAKEDOWNSPERCENT', axis=1, inplace=True)

    df_fight_stats[['HEADSTRIKESHIT', 'HEADSTRIKESATTEMPTED']
                   ] = df_fight_stats['HEADSTRIKES'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('HEADSTRIKES', axis=1, inplace=True)

    df_fight_stats[['BODYSTRIKESHIT', 'BODYSTRIKESATTEMPTED']
                   ] = df_fight_stats['BODYSTRIKES'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('BODYSTRIKES', axis=1, inplace=True)

    df_fight_stats[['LEGSTRIKESHIT', 'LEGSTRIKESATTEMPTED']
                   ] = df_fight_stats['LEGSTRIKES'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('LEGSTRIKES', axis=1, inplace=True)

    df_fight_stats[['DISTANCEHIT', 'DISTANCEATTEMPTED']
                   ] = df_fight_stats['DISTANCE'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('DISTANCE', axis=1, inplace=True)

    df_fight_stats[['CLINCHHIT', 'CLINCHATTEMPTED']
                   ] = df_fight_stats['CLINCH'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('CLINCH', axis=1, inplace=True)

    df_fight_stats[['GROUNDHIT', 'GROUNDATTEMPTED']
                   ] = df_fight_stats['GROUND'].str.extract(r'(\d+) of (\d+)')
    df_fight_stats.drop('GROUND', axis=1, inplace=True)

    df_fight_stats.to_csv('out/fight_stats.csv', index=False)


def __cleanup_all():

    files = ['out/fighters.csv', 'out/events.csv',
             'out/fights.csv', 'out/fight_stats.csv']

    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)

            # Lowercase headers
            df.columns = [col.lower() for col in df.columns]
            # Strip whitespace from strings
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            # Remove double-spaces
            df = df.map(lambda x: re.sub(r'\s+', ' ', x.strip())
                        if isinstance(x, str) else x)
            df.to_csv(file, index=False)
