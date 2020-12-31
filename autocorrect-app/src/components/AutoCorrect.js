// main imports
import React from 'react';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import TextareaAutosize from '@material-ui/core/TextareaAutosize';
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import SocketClient from '../utils/socketClient.js'
import { split } from "sentence-splitter";
import * as md5 from 'md5';

// {this.renderSuggestions()}
class AutoCorrect extends React.Component {

    // Constructor
    constructor(props) {
        super(props);
        // init state
        this.state = {
            text: '',
            sentences: new Map()
        };

        // init handlers
        this.handleAutocorrectResponse = this.handleAutocorrectResponse.bind(this);
    }

    // after-mount init
    componentDidMount() {
        this.socketClient = new SocketClient(process.env.REACT_APP_SERVER_URL, this.handleAutocorrectResponse);
        this.socketClient.openSocket();
    }

    // before un-mount clean-up
    componentWillUmount() {
        this.socketClient.closeSocket();
        this.socketClient = null;
    }

    // Send new sentence for auto-correct
    autocorrectSentence(key, sentence) {
        this.socketClient.sendRequest(JSON.stringify({ key: key, sentence: sentence }));
    }

    // Update state with sentence classification results
    handleAutocorrectResponse(data) {
        const result = JSON.parse(data);
        const updatedSentences = this.state.sentences;
        updatedSentences.set(result.key, { sentence: result.sentence, suggestions: result.suggestions })
        this.setState({ sentences: updatedSentences });
    }

    // Handler for text entry in text area
    handleCapture(capturedText) {
        // split captured text by sentences
        const splitBySentence = split(capturedText);

        // go through all splitted sentences
        const currentSentences = this.state.sentences;
        const updatedSentences = new Map();

        splitBySentence.forEach((element) => {
            if (element['type'] === 'Sentence') {
                // calculate sentence's hash and check if if is already in the sentence's map
                const sentence = element['raw'];
                const key = md5(sentence);

                if (currentSentences.has(key)) {
                    // seems like an existing sentence - let's simply copy that to the map
                    updatedSentences.set(key, currentSentences.get(key))
                } else {
                    // seems like a new sentence found - let's auto-correct and add suggetions to the map
                    this.autocorrectSentence(key, sentence);
                    updatedSentences.set(key, { sentence: sentence, suggestions: {} });
                }
            }

            // keep updated sentences in state 
            this.setState({ sentences: updatedSentences });
        })

        // keep captured text in state to show that under capture text area
        this.setState({ text: capturedText });
    }

    // render for capture text area
    renderEntry() {
        return (
            <TextareaAutosize
                aria-label="minimum height"
                rowsMin={10}
                placeholder="Enter some text to auto-correct"
                onInput={(event) => this.handleCapture(event.target.value)} value={this.state.text}> </TextareaAutosize>
        );
    }

    acceptSuggestion(key, word, suggested_edit) {
        // update sentence with suggested edit
        const updatedSentences = this.state.sentences;
        const updatedSentence = updatedSentences.get(key).sentence.replace(word, suggested_edit);

        // generate new key and drop old one
        updatedSentences.delete(key);
        const updatedKey = md5(updatedSentence);
        updatedSentences[updatedKey] = updatedSentence;

        // update word in the full text, too
        const updatedFullText = this.state.text.replace(word, suggested_edit);

        // keep updated sentences in state 
        this.setState({ sentences: updatedSentences, text: updatedFullText });
    }

    // render for showing captured and classified text
    renderSuggestions() {
        // prepare an array of suggestions
        const suggestion_array = new Array();
        this.state.sentences.forEach((sentence, key) => {
            const suggestions = sentence.suggestions;
            for (const word in suggestions) {
                suggestions[word].forEach(suggested_edits => {
                    for (const target_word in suggested_edits) {
                        const edit_distance = suggested_edits[target_word];
                        suggestion_array.push({ key: key, word: word, suggested_edit: target_word, edit_distance: suggested_edits[target_word] });
                    }

                });
            }
        });

        // prepare a list of buttons with recommended edits
        const buttonGroup = suggestion_array.map((t) => {
            return (
                <Button variant="contained" size="small"
                    onClick={() => { this.acceptSuggestion(t.key, t.word, t.suggested_edit, t.edit_distance) }}>
                    {t.word} >> {t.suggested_edit} ({t.edit_distance})
                </Button>
            );
        });

        return (
            <div>
                {buttonGroup}
            </div >
        );
    }

    // main rendering function
    render() {
        return (
            <Container maxWidth="sm">
                <Box my={4}>
                    <form noValidate autoComplete="off">
                        {this.renderEntry()}
                        {this.renderSuggestions()}
                    </form>
                </Box>
            </Container>
        );
    }
}

export default AutoCorrect;