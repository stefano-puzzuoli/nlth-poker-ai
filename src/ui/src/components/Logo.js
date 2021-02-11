import React, { Component } from 'react';

class Logo extends Component {
    render() {
        return (
            <div className="logo-main mb-4">
                <span className="navbar-brand">
                    <span ><img className="logo-image mr-2" src="/assets/logo.jpg" /></span>
                    <h3 className="navbar-text">No-Limit Texas Hold'em Poker</h3>
                </span>
            </div>
        )
    }
}

export default Logo;