#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "input_folder", help="Input folder with the raw files"
)
args = parser.parse_args()

def create_transcript(input_file):
    records = []

    for i, caption in enumerate(webvtt.read(input_file)):
        # If a speaker is identified, extract the speaker.
        # text_components1 = caption.text.split(": ")
        text_components1 = re.split("^[a-zA-Z\.]+\s[a-zA-Z\.]+\:", caption.text, maxsplit=1)
        #remove empty strings
        text_components = [x for x in text_components1 if x]
        #get speaker name
        speaker_reg = re.search("^[a-zA-Z\.]+\s[a-zA-Z\.]+\:", caption.text)
        # speaker = text_components[0] if len(text_components) > 1 else None
        speaker = speaker_reg.group(0).replace(": ", "") if speaker_reg else None

        # Extract the text
        text = (
            text_components[1] if len(text_components) > 1 else text_components[0]
        )
        #TO DO: If speaker is None, club utterance with previous utterance
        # if speaker is not None:
        records.append(
            {
                "speaker": speaker,
                "timestart": caption.start,
                "timeend": caption.end,
                "utt": text,
                "utt_num": i+1,
            }
        )
        #else:
        # replace records[len(records)-1]["timeend"] and extend records[len(records)-1]["utt"]

    # Create the dataframe
    df = pd.DataFrame(records)


    # Output the dataframe to TSV
    p = Path("output/")
    p.mkdir(parents=True, exist_ok=True)
    q = PurePosixPath(input_file).name
    fn = q.split(".vtt")[0]+".tsv"
    output = p / fn
    df.to_csv(output, index=False, sep="\t")
    return None
def m4a_t0_wav(m, w):
    sp.run(
        [
            "ffmpeg",
            "-i",
            m,
            w,
            "-loglevel",
            "quiet",
        ]
    )
    return None

if __name__ == "__main__":
    import webvtt
    import pandas as pd
    from pathlib import Path
    from pathlib import PurePosixPath
    import re
    import subprocess as sp

    # read all .vtt files:
    vtt_files = Path(args.input_folder).rglob('*.vtt')

    files = [x for x in vtt_files]

    # check if media file with same name exists:
    valid = []
    for i in files:
        media = str(i).split(".vtt")[0]+".m4a"
        wav = str(i).split(".vtt")[0] + ".wav"
        if media:
            valid.append(i)

    # create .wav files for media files:
        if not Path(wav).exists():
            m4a_t0_wav(media, wav)
            print(".wav files created")

    print("valid transcripts identified")
    # extract transcripts in .tsv file:
    for i in valid:
        create_transcript(i)
        print("processed", i)





