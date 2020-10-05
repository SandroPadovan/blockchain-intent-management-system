import React, {Component} from 'react';
import IntentExplanation from '../intents/IntentExplanation';

class Help extends Component {
    render() {
        return (
            <div className="jumbotron" style={{"backgroundColor": "transparent"}}>
                <h2 className="mb-5">Help page</h2>
                <h5 className="lead mb-5">On this help page you will find useful information about the Blockchain Intent
                    Management System. It covers aspects from Intent creation, to updating, deleting etc.</h5>
                <h4>What is the Blockchain Intent Management System?</h4>
                <p>The Blockchain Intent Management System uses Intent-based Management for the process of Blockchain
                    Selection. It let's users create Intents, which are refined into one or multiple Policies. The
                    system let's a user manage Intents, update, or delete them.</p>
                <h4>What is an Intent and Intent-based Management?</h4>
                <p>An Intent can be defined as a high-level policy used to manage a system. It only contains abstract
                    information, i.e. it defines "what" should be done, but not "how" to do it.</p>
                <h4>What is a Policy?</h4>
                <p>A Policy is the result of the Intent Refinement process. It contains much more low-level details than
                    the Intent and is designed to be applied in a system. The Policies corresponding to an Intent can be
                    seen on the Details page of an Intent.</p>
                <IntentExplanation/>
                <h4>How do I edit / update an Intent?</h4>
                <p>In the Intent Overview, select the Intent you want to edit by clicking on Details. Then, in the
                    Intent Details, there is a button which lets you edit the Intent. Note that updating an Intent will
                    update the corresponding policies, or depending on the intent add new or delete existing
                    policies.</p>
                <h4>How do I delete an Intent?</h4>
                <p>In the Intent Overview, select the Intent you want to edit by clicking on Details. Then, in the
                    Intent Details, there is a button which lets you delete the Intent. Note that all policies
                    corresponding to an intent will be deleted. Deleting an Intent is irreversible.</p>
            </div>
        );
    }
}

export default Help;