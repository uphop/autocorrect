# Text auto-correct with Minimum Edit Distance

## Overview

This project implements a probabilistic spell-checking and auto-correction, based on this article: [How to Write a Spelling Corrector](https://norvig.com/spell-correct.html). 
Mis-spelled words are detected by checking against a vocabulary (built based on [List of English words](https://github.com/dwyl/english-words)).
Auto-correct is implemented by evaluating possible custom edits (single- and double-edit variations) of mis-spelled words, providing a list of suggestions with the minimum number of required edits between the mis-spelled word and the target suggested word.
Required number of edits is calculated based on [Minimum Edit Distance algorithm](https://web.stanford.edu/class/cs124/lec/med.pdf).

The project consists of the following modules:
* `autocorrect-app`: a React application, which captures text input from a user, splits captured text into sentences, sends each sentence via a websocket to `autocorrect-server` for spell-checking, and then visualises suggested edits.
* `autocorrect-server`: a Python-based server, which gets sentences from `autocorrect-app` via a websocket, and then provides back a list of recommended edit suggestions.

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

Type some text into the text area - the app will be capturing text, attempting to split into sentences / provide suggested edits with the count of required edits for all unrecognized words, and visualise those as a set of action buttons. Each action button in turn will implement a specific suggestion edit.

Here is an example of what you should see as the result:
![Screenshot](https://user-images.githubusercontent.com/74451637/103398561-e9118c00-4b45-11eb-942e-fc7818e07751.png)

And [here is a recorded demo of autocorrect.](http://www.youtube.com/watch?v=10VITDvv6Ds)



