#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "input_folder",
    help="Input folder for media files",
)
parser.add_argument(
    "output_folder",
    help="Output folder for CSV files",
)
args = parser.parse_args()


def save_acoustic_csv(directory, wav, savename, feature_set= "IS10"):
    conf_dict = {
        "ISO9": "is09-13/IS09_emotion.conf",
        "IS10": "is09-13/IS10_paraling.conf",
        "IS12": "is09-13/IS12_speaker_trait.conf",
        "IS13": "is09-13/IS13_ComParE.conf",
    }

    fconf = conf_dict.get(feature_set, "IS09_emotion.conf")
    smile = "../external/opensmile-3.0"
    # run openSMILE
    sp.run(
        [
            f"{smile}/bin/SMILExtract",
            "-C",
            f"{smile}/config/{fconf}",
            "-I",
            wav,
            "-lldcsvoutput",
            f"{directory}/{savename}",
        ]
    )
# def feats(wav_file):

if __name__ == "__main__":
    from pathlib import Path
    import subprocess as sp
    #find all .wav files
    wav_files = Path(args.input_folder).rglob('*.wav')
    files = [x for x in wav_files]
    # make feature files
    for i in files:
        print(i)
        o = i.name.split("wav")[0]+"csv"
        print(o)
        save_acoustic_csv(directory = args.output_folder, wav = i, savename = o, feature_set= "IS10")