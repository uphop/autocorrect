# Real-time text autocorrect with English dictionary

## Overview

This is a simple web app plus a socket-based server demonstraing a real-time text auto-correction by vocabulary. Auto-correct is implemented by evaluating possible custom edits (single- and double-edit variations). The vocabulary is based on English dictionary. 

The project consists of the following modules:
* `autocorrect-app`: a React application, which captures text input from a user, splits captured text into sentences, sends each sentence via a websocket to `autocorrect-server` for cross-chekcing, and then visualises suggested edits.
* `autocorrect-server`: a Python-based server, which gets sentences from `autocorrect-app` via a websocket, and then provides back a list of recommended text edits. 

The following are key 3rd party components used:
* [sentence-splitter](https://www.npmjs.com/package/sentence-splitter) - used in `autocorrect-app` for splitting captured text into sentences
* [List of English words](https://github.com/dwyl/english-words) - used in `autocorrect-server` for evaluting word correctness and possible edit

## Setting-up

Clone full project:
```
git clone git@github.com:uphop/autocorrect.git && cd autocorrect
```

Install dependencies and prepare configuration for `autocorrect-app`:
```
cd autocorrect-app && yarn install && cp .env.sample .env && cd..
```

Install dependencies and prepare configuration for `autocorrect-server`:
```
cd autocorrect-server && pip3 install -r requrements.txt && cp .example-env .env && cd..
```

## Starting-up

Start `autocorrect-server`:
```
cd autocorrect-server && ./run.sh
```

Start `autocorrect-app`:
```
cd autocorrect-app &&  yarn start
```

## Usage

Type some text into the text area - the app will be capturing text, attempting to split into sentences / provide suggested edits for unrecognized words, and visualise those as a set of action buttons. Each action button in turn will implement a specific suggestion edit.

Here is an example of what you should see as the result:
![Screenshot](https://user-images.githubusercontent.com/74451637/103369209-30f6cb80-4ad2-11eb-8c4d-62fe2911efb8.png)

And here is a recorded example of sentiment score assessment while typing:
[![Recorded_sample](http://img.youtube.com/vi/eA70enkT_Mc.jpg)](http://www.youtube.com/watch?v=eA70enkT_Mc "Auto-correct example")



