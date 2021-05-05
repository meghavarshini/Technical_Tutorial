## Extracting transcript-aligned Acoustic Features using OpenSMILE

###  Introduction

This tutorial provides a walkthrough for setting up a feature set for analysis and extracting speaker metadata from Zoom transcripts. It will cover the pre-requisites for and data structure of the feature extractor, and the `vtt` transcription format used by Zoom. Finally, it will provide a brief description of how to use timestamps in the transcripts to align the text text to the acoustic features and collate a meaningful output file that can be further used for analysis.  

The Git repository contains code and short media files for running unit tests. Be sure to check out the `output` folder and match your output with the expected output. 

**Requirements**:
Before we begin, make sure that you have the following set up and running:

1. [Python 3.0](https://www.python.org/downloads/) or higher 
2. The [FFMPEG](https://ffmpeg.org/ffmpeg.html) command line tool 
3. [OpenSmile](https://github.com/audeering/opensmile) package

###  OpenSMILE

OpenSmile is a open-source, hands-on package for extracting acoustic features from a sound file for a variety of use cases, such as song identification, accent recognition and speech analysis. It allows users to select a feature set and an interval (for a full list of available default features [see this](https://audeering.github.io/opensmile/get-started.html#default-feature-sets). Based on this input, it runs the extractor at the user-provided time interval, and returns a `.csv` file that contains all the feature labels as the first row. Here is what the output for IS-10 feature set and 10ms interval:

[PUT A TABLE HERE]

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

* Searches for all files in the `.vtt` format
* Searches the output folder for a `.csv` file with the same name and the prefix "processed"
* If final output file is absent, it looks for the corresponding `.wav` file to begin the extraction.
* If `.wav` file is absent, it finds the `.m4a` file and converts it to `.wav`. (you can modify line [ ] in file [ ] to chance this to any input format of your choice).
* Next, it searches for a `.tsv` file with speaker names and transcripts for each transcript. If this is absent, it creates it. Now, the input for the extraction is ready.
* It extracts acoustic features for each `.wav` file
* Finally, it collates the features with the corresponding file and returns a CSV file with the transcript information and acoustic features and stores it in an output folder.

###  Useage

```python
./scripts/acoustic_pipeline.py ./sample_input
```

<!---

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

###  Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

###  Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/meghavarshini/Technical_Tutorial/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
-->
