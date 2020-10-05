import React, {Component} from 'react';

class IntentExplanation extends Component {
    render() {
        return (
            <div>
                <h4 className="mb-3">How do I create a valid Intent?</h4>
                <div>
                    <p>An Intent is valid, if it adheres to the rules of a controlled language. The different parameters
                        forming an Intent are shown below.</p>
                    <p>Each Intent starts with the word <mark>For</mark>. As Intents are translated into policies per
                        user, a single <mark>User</mark> or a set of <mark>Users</mark> separated by <mark>,</mark> or
                        <mark>and</mark> is defined next.
                    </p>
                    The next parameter is a Timeframe, which is <strong>optional</strong>. Allowed values are:
                    <ul>
                        <li><mark>in the day</mark></li>
                        <li><mark>in the night</mark></li>
                        <li><mark>in the morning</mark></li>
                        <li><mark>in the afternoon</mark></li>
                    </ul>
                    Next comes <mark>select</mark>, followed by either a profile or a blockchain. For supported
                    blockchains, see below. Allowed values for a profile are:
                    <ul>
                        <li><mark>the cheapest</mark></li>
                        <li><mark>the fastest</mark></li>
                    </ul>
                    Next, a set of <strong>optional</strong> filters can be specified separated by <mark>,</mark> or
                    <mark>and</mark>. Allowed values are:
                    <ul>
                        <li><mark>private</mark></li>
                        <li><mark>public</mark></li>
                        <li><mark>fast</mark></li>
                        <li><mark>cheap</mark></li>
                        <li><mark>stable</mark></li>
                        <li><mark>popular</mark></li>
                    </ul>
                    The filters <mark>private</mark> and <mark>public</mark> are mutually exclusive, while the filters
                    <mark>fast</mark> and <mark>cheap</mark> are only considered if combined with a corresponding
                    profile.
                    <p>The filters are followed by the word <mark>blockchain</mark>.</p>
                    If a profile was specified, a Whitelist or a Blacklist can be specified. A Whitelist is specified by
                    <mark>from</mark>, a Blacklist by <mark>except</mark> followed by a set of blockchains separated by
                    <mark>,</mark> or <mark>and</mark>. Supported blockchains are:
                    <ul>
                        <li><mark>Bitcoin</mark></li>
                        <li><mark>EOS</mark></li>
                        <li><mark>Ethereum</mark></li>
                        <li><mark>Hyperledger</mark></li>
                        <li><mark>IOTA</mark></li>
                        <li><mark>MultiChain</mark></li>
                        <li><mark>Stellar</mark></li>
                    </ul>
                    Next, a set of <strong>optional</strong> modifiers can be specified separated by <mark>,</mark> or
                    <mark>and</mark>. Allowed values are:
                    <ul>
                        <li><mark>redundancy</mark></li>
                        <li><mark>splitting</mark></li>
                        <li><mark>encryption</mark></li>
                    </ul>
                    If you want a default policy, type <mark>as default</mark>. Otherwise, a cost interval,
                    a cost currency and a cost threshold can be specified here. Allowed values for an interval are:
                    <ul>
                        <li><mark>until the daily costs reach</mark></li>
                        <li><mark>until the weekly costs reach</mark></li>
                        <li><mark>until the monthly costs reach</mark></li>
                        <li><mark>until the yearly costs reach</mark></li>
                    </ul>
                    Supported currencies are:
                    <ul>
                        <li><mark>USD</mark></li>
                        <li><mark>CHF</mark></li>
                        <li><mark>EUR</mark></li>
                    </ul>
                    If not specified, the default currency is USD.
                    <p>At the end, a threshold is specified as a number. Notice that a dot at the end of the intent is
                        not valid.</p>
                </div>
                <h4 className="mt-4">Examples</h4>
                <p>Here you find some examples for valid intents.</p>
                <p><mark>For client1 select the cheapest private blockchain as default</mark></p>
                <p><mark>For client2, client3 and client4 in the day select the fastest cheap blockchain except EOS with
                    splitting until the daily costs reach CHF 50</mark></p>
                <p><mark>For client5 in the night select Bitcoin as default</mark></p>
            </div>
        );
    }
}

export default IntentExplanation;