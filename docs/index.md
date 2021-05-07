## Extracting transcript-aligned Acoustic Features using OpenSMILE

###  Introduction

This tutorial provides a walkthrough for setting up a feature set for analysis and extracting speaker metadata from Zoom transcripts. It will cover the pre-requisites for and data structure of the feature extractor, and the `vtt` transcription format used by Zoom. Finally, it will provide a brief description of how to use timestamps in the transcripts to align the text text to the acoustic features and collate a meaningful output file that can be further used for analysis. The code for this tutorial is mainly from the [ToMCAT-Speech repository](https://github.com/clulab/tomcat-speech/), and links to the specific code is available as comments in every script in this repository.

The Git repository contains code and short media files for running unit tests. Be sure to check out the `output` folder and match your output with the expected output. 

This tutorial is still a work in progress, and I appreciate comments and feedback.

**Requirements**:
Before we begin, make sure that you have the following set up and running:

1. [Python 3.0](https://www.python.org/downloads/) or higher 
2. The [FFMPEG](https://ffmpeg.org/ffmpeg.html) command line tool 

###  OpenSMILE

OpenSmile is a open-source, hands-on package for extracting acoustic features from a sound file for a variety of use cases, such as song identification, accent recognition and speech analysis. It allows users to select a feature set and an interval (for a full list of available default features [see this](https://audeering.github.io/opensmile/get-started.html#default-feature-sets). Based on this input, it runs the extractor at the user-provided time interval, and returns a `.csv` file that contains all the feature labels as the first row.

You can learn more about OpenSMILE through their [user manual](https://audeering.github.io/opensmile/about.html#capabilities) and follow their guide to set up OpenSMILE for your device and [get started](https://audeering.github.io/opensmile/get-started.html#get-started).

OpenSMILE's relatively simple setup and lightweight system makes it a great candidate for speech analysis. However, all it can do is give us a feature set. Our audio could have multiple speakers and periods that are of no interest to us. So, we need to find a way to align the feature set with the periods of interest. In this tutorial, we will align utterances to their acoustic feature set.  

###  Zoom Transcription

Zoom's simple interface, its close-captioning service and good audio quality has made it a top choice for extracting transcripts. It also allows for multi-channel recording, so that audio overlap can be avoided. A typical Zoom transcript looks like this:

```python

00:00:00.500 --> 00:00:02.000
The Web is always changing

00:00:02.500 --> 00:00:04.300
and the way we access it is changing
```
[add text file]


###  VTTParser

The Python `webvtt` [library](https://pypi.org/project/webvtt-py/) is a good resource for reading and processing of transcription files. It also allows users to convert their transcripts to more useable formats and write tables into transcriptions. A detailed description can be found in the documentation [here](https://webvtt-py.readthedocs.io/en/latest/usage.html#reading-webvtt-caption-files).

However, the `webvtt` may need to be tweaked in order to extract speaker names, and correctly align speaker information with the transcripts. There are many scripts that help users manage their Zoom transcripts that you can check out below. For this tutorial, I have included a modified script from the [TomCAT-Speech repository](https://github.com/clulab/tomcat-speech) repository that will allow us to read the `.vtt` file, identify the timestamps for every utterance, and align speaker names (if available) with the transcript, and extract each utterance along with its index number.
 
###  Feature Extraction Pipeline

Zoom audio is stored in the `m4a` format. In order to use it fr feature extraction, we first convert it to `.wav` format. Our pipeline accepts an input file destination and:

* Searches for all files in the `.vtt` format paired with an identically names `.m4a` file.
* Searches the output folder for a `.csv` file with the same name and the prefix "processed"
* If final output file is absent, it looks for the corresponding `.wav` file to begin the extraction.
* If `.wav` file is absent, it finds the `.m4a` file and converts it to `.wav`. (you can modify line [ ] in file [ ] to chance this to any input format of your choice).
* Next, it searches for a `.tsv` file with speaker names and transcripts for each transcript. If this is absent, it creates it. Now, the input for the extraction is ready.
* It extracts acoustic features for each `.wav` file
* Finally, it collates the features with the corresponding file and returns a CSV file with the transcript information and acoustic features and stores it in an output folder.

###  Useage
Navigate into the folder containing all the code:

```bash
cd ./code
```

Download OpenSMILE by running the following script:

```python
bash ./download_OpenSMILE.sh
```

First, we will setup our virtual environment. The following lines will create a virtual environment if none present, or create one; and install all requirements listen in setup.py:

```python
bash ./virtual_env.sh
pip install .
```
Next, we will search for all pairs of `.m4a` files and `.vtt` files, and process the `.vtt` file into a useable `.tsv` files, and convert the `m4a` files to `.wav`. We will run the `vtt_to_tsv.py` script, which takes a directory path with files as its argument. For the testing the pipeline let us run this on the input folder in the repository:

```python
python vtt_to_tsv.py ./sample_input/
```

Now that we have our `.tsv` files and `.wav` files, we will move on to extraction. We will run `extract_acoustic_features.py` to look for all `.wav` files in a location, run OpenSMILE on it, and store the features in a unser-defined destination, like so:

```python
python extract_acoustic_features.py ./sample_input ./output
```

Now that our transcript and media files have been processed, we will run the `run_OpenSMILE.py` script using the folder with the `tsv` and `csv` files as the arguments. This will align the transcript with its averaged features, and return a file with our data:

```python
python run_OpenSMILE.py ./output
```
You will see the runtime messages from OpenSmile in the terminal. The folder with the TSV adn CSV file will see new files with the the prefix "provessed_". This will contain all the features appended with speaker name, and the information from the `.vtt` file.

Currently, this pipeline outputs one line of averaged features per utterance. This can be changed by changing the feature extraction function in the above code. 

This process can take a lot of time. In order to customize your run of OpenSMILE, change the `feature_set` variable on line 52 to the appropriate name.