# Conference-Email-Parser
For CSC 482.

View the [dashboard](https://gwholland3.github.io/Conference-Email-Parser/).

## Setup
Follow these instructions to set up the codebase locally.

### 1. Clone the Repo
Run your favorite version of the git clone command on this repo. I prefer:

`git clone git@github.com:gwholland3/Conference-Email-Parser.git`

### 2. Install Python
This code was developed and run on Python `3.10`. Make sure you have an appropriate version installed locally.

### 3. Install Requirements
I recommend doing this in a fresh Python virtual environment. Cd into the repo and run:

`pip3 install -r requirements.txt`

### 4. Download Required Data
The following is necessary for the Python library SpaCy to function:

`python3 -m spacy download en_core_web_sm`

## Run the Program:
From the project root, run:

`python3 src/extract_conference_info.py`

Run the following to see all options:

`python3 src/extract_conference_info.py -h`
