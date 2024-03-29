# Conference-Email-Parser

For CSC 482.

View the [dashboard](https://gwholland3.github.io/Conference-Email-Parser/).

## Setup

If you want to run the program yourself, there are two options available.

### Docker

Run the following script and you will be placed in a shell in a streamlined directory structure roughly mirroring the project root, with all dependencies needed to run the program:

```
./develop_in_docker.sh
```

### Manual

Alternatively, you can follow these steps to set up a Python development environment with the program directly on your computer.

#### 1. Clone the Repo

Run your favorite version of the git clone command on this repo. I prefer:

`git clone git@github.com:gwholland3/Conference-Email-Parser.git`

#### 2. Install Python

This code was developed and run on Python `3.10`. Make sure you have an appropriate version installed locally.

#### 3. Install Requirements
I recommend doing this in a fresh Python virtual environment. Cd into the repo and run:

`pip3 install -r requirements.txt`

#### 4. Download Required Data

The following is necessary for the Python library SpaCy to function:

`python3 -m spacy download en_core_web_sm`

The following is necessary to use the NLTK sentence tokenizer:

`python3 nltk_download.py`

## Run the Program:

From the project root, run:

`python3 src/extract_conference_info.py`

Run the following to see all options:

`python3 src/extract_conference_info.py -h`
