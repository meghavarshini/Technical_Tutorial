#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "input_folder",
    help="Input folder for TSV and CSV files",
)
args = parser.parse_args()


def split_zoom_time(timestamp):
    """
    split the hh:mm:ss.sss zoom timestamps to seconds + ms
    used to calculate start and end of acoustic features
    """
    h, m, s = timestamp.split(":")
    return (float(h) * 60 + float(m)) * 60 + float(s)

def create_output(tsv, csv):
    # get holder for averaged acoustic items
    all_acoustic_items = []

    # add the feature file to a dataframe
    acoustic_df = pd.read_csv(csv, sep=";")
    acoustic_df = acoustic_df.drop(columns=["name"])

    # add column names to holder
    col_names = acoustic_df.columns.tolist()
    col_names.append("timestart")  # so that we can join dataframes later

    # add the corresponding dataframe of utterance info
    utt_df = pd.read_table(tsv)

    # ID all rows id df between start and end of an utterance
    for i, row in utt_df.iterrows():
        # get the goal start and end time
        start_str = row['timestart']
        end_str = row['timeend']

        start_time = split_zoom_time(start_str)
        end_time = split_zoom_time(end_str)

        # get the portion of the dataframe that is between the start and end times
        this_utterance = acoustic_df[
            acoustic_df["frameTime"].between(start_time, end_time)
        ]

        # use this_utterance as input for gender_classifier.
        # get the mean values of all columns

        this_utt_avgd = this_utterance.mean().tolist()
        this_utt_avgd.append(
            start_str
        )  # add timestart so dataframes can be joined

        # add means to list
        all_acoustic_items.append(this_utt_avgd)

        # convert all_acoustic_items to pd dataframe
        acoustic = pd.DataFrame(all_acoustic_items, columns=col_names)

    # join the dataframes
    df = pd.merge(utt_df, acoustic, on="timestart")

    # save the joined df as a new TSV
    output = "processed_"+tsv.name
    p = Path(tsv).parents[0]
    print(p / output)
    f = open(p / output, "w+")
    df.to_csv(f, index=False, sep="\t")
    f.close()
    return None
if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path
    tsv = Path(args.input_folder).rglob('*.tsv')
    tsv_files = [file for file in tsv]
    csv = Path(args.input_folder).rglob('*.csv')
    csv_files = [file for file in csv]
    print("searching files...")
    valid = []
    unprocessed = []
    # create list of files with a corresponding csv file:
    for i in tsv_files:
        if str(Path(i).stem+".csv") in [i.name for i in csv_files]:
            valid.append(i)
        else:
            unprocessed.append(i.name)
    #print list of unused files:
    if len(valid) > 0:
        for i in valid:
            # print(Path(i), Path(i).parents[0], str(Path(i).parents[0])+str("/"+Path(i).stem+".csv"))
            create_output(Path(i), str(Path(i).parents[0])+str("/"+Path(i).stem+".csv"))
    if len(unprocessed) != 0:
        print("some unprocessed files exist. Here are there names: ")
        print(*unprocessed, sep=',')
# write a for loop to run this on all pairs of tsv and csv files
#     1. find all files in list
#     2. find tsc and csv pairs
#     3. run function above.
