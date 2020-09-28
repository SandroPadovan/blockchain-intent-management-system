import React, {Component} from 'react';
import PropTypes from 'prop-types';


class IntentInputField extends Component {

    state = {
        intent: this.props.initialValue,
        suggestions: [],
        activeSuggestion: 0,
        hasMistake: false,
    }

    static propTypes = {
        expected: PropTypes.array.isRequired,
        checkIfValid: PropTypes.func.isRequired,
        isValid: PropTypes.bool.isRequired,
        onSubmit: PropTypes.func.isRequired,
        buttonText: PropTypes.string.isRequired,
        initialValue: PropTypes.string.isRequired,
        parserMessage: PropTypes.string.isRequired,
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.state.intent && this.state.intent !== prevState.intent ||
        this.props.expected !== prevProps.expected) {
            this.onSuggestionsFetchRequested(this.state.intent)
        }
    }

    // submit handler, calls function of parent component
    onSubmit = e => {
        e.preventDefault();
        this.props.onSubmit(this.state.intent)
    }

    onChange = e => {
        this.setState({
            [e.target.name]: e.target.value,
            activeSuggestion: 0
        }, () => {
            this.props.checkIfValid(this.state.intent);
            this.onSuggestionsFetchRequested(this.state.intent)
        });
    }

    // handles clicks on a suggestion
    onClick = e => {

        // validPart is equal to the user input without the last word
        const validPart = this.state.intent.split(" ").slice(0,-1).join(" ");

        // intent is set as the validPart plus the suggestion clicked on
        this.setState({intent: validPart + " " + e.currentTarget.innerText}, () => {
            this.props.checkIfValid(this.state.intent);
        });

        // set focus on input field
        this.intentInput.focus();
    }

    // handles key presses (Tab, Enter, Arrow Up, Arrow Down)
    onKeyDown = e => {
        if (e.keyCode === 9 || e.keyCode === 13) {  // Tab or Enter
            e.preventDefault();
            const validPart = this.state.intent.split(" ").slice(0,-1).join(" ");
            const activeSuggestion = this.state.suggestions[this.state.activeSuggestion]
            if (activeSuggestion) {
                this.setState({
                    intent: validPart + " " + activeSuggestion,
                    activeSuggestion: 0
                }, () => {
                    this.props.checkIfValid(this.state.intent);
                });
            }
        } else if (e.keyCode === 40) {   // Arrow Down
            if (this.state.activeSuggestion + 1 === this.state.suggestions.length) {
                return;
            }
            this.setState({ activeSuggestion: this.state.activeSuggestion + 1 });
        } else if (e.keyCode === 38) { // Arrow Up
            if (this.state.activeSuggestion === 0) {
                return;
            }
            this.setState({ activeSuggestion: this.state.activeSuggestion - 1 });
        }
        this.intentInput.focus();
    }

    // filters through array of expected words, returns the words which match the input
    getSuggestions = intent => {
        const value = intent.toString().split(' ').pop();
        const inputValue = value.trim().toLowerCase();
        const inputLength = inputValue.length;

        if (inputLength === 0 && this.props.parserMessage === 'Intent is incomplete') {
            // if inputValue is a space, and the intent so far is valid, hasMistake is set to false
            // all expected words are returned
            if (this.state.hasMistake) {
                this.setState({hasMistake: false});
            }
            return this.props.expected;
        } else if(inputLength === 0 && this.props.parserMessage !== 'Intent is incomplete') {
            // if inputValue is a space, and the intent so far is not valid, intent has a mistake
            // returns an empty array
            this.setState({hasMistake: true});
            return [];
        } else if (this.state.hasMistake) {
            // if intent has a mistake, no suggestions shall be given, no matter what the user types
            return [];
        } else if (inputLength > 0 && this.props.parserMessage !== 'Intent is incomplete') {
            // the user is typing a word, return filtered array with expected words
            return this.props.expected.filter(exp => exp.toLowerCase().slice(0, inputLength) === inputValue)
        } else return [];   // if none of the above conditions are met, no suggestions shall be given
    };

    // sets the suggestions state according to the user input
    onSuggestionsFetchRequested = ( intent ) => {
        this.setState({
            suggestions: this.getSuggestions(intent)
        });
    };


    render() {

        const { isValid } = this.props;
        const { intent, activeSuggestion } = this.state;

        // styling: CSS classNames depending on whether the intent is valid or not
        let classNameFormGroup;
        let classNameInput;
        if (isValid) {
            classNameFormGroup = "form-group has-success mt-5";
            classNameInput = "form-control is-valid";
        } else {
            classNameFormGroup = "form-group has-danger mt-5"
            classNameInput = "form-control is-invalid"
        }

        const suggestions = (
            <div className="position-relative">
                <ul className="list-group position-absolute w-75" style={{"zIndex": "2"}}>
                    {this.state.suggestions.map((suggestion, index) => {
                        let classNameSuggestion;
                        if (index === activeSuggestion) {
                            classNameSuggestion = "list-group-item d-flex justify-content-between align-items-center active"
                        } else {
                            classNameSuggestion = "list-group-item d-flex justify-content-between align-items-center"
                        }
                        return(
                            <li
                                key={suggestion}
                                className={classNameSuggestion}
                                onClick={this.onClick}
                            >{suggestion}</li>
                        )
                    })}
                </ul>
            </div>
        )

        return (
            <form onSubmit={this.onSubmit}>
                <div className={classNameFormGroup}>
                    <input
                        ref={(input) => { this.intentInput = input; }}
                        type="text"
                        value={intent}
                        name="intent"
                        className={classNameInput}
                        id="intentInput"
                        onChange={this.onChange}
                        onKeyDown={this.onKeyDown}
                        autoComplete="off"
                    />
                    {isValid ? <div className="valid-feedback">Valid Intent</div> : <div/>}
                    {this.state.suggestions.length === 0 ?
                        <p className="text-danger">{this.props.parserMessage}</p> : suggestions}
                </div>
                <div className="text-right mb-5">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={!isValid}
                    >{this.props.buttonText}</button>
                </div>
            </form>
        );
    }
}

export default IntentInputField;