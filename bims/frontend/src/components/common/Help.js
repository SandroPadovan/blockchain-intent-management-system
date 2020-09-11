import React, {Component} from 'react';

class Help extends Component {
    render() {
        return (
            <div className="jumbotron" style={{"backgroundColor": "transparent"}}>
                <h2>Help page</h2>
                <p>This is a help page with useful information about the Blockchain Intent Management System. It covers
                 all necessary aspects from intent creation, to updating, deleting etc.</p>
                <h4>What is an Intent?</h4>
                <p>An Intent is defined as a high-level policy used to manage a system.</p>

            </div>
        );
    }
}

export default Help;