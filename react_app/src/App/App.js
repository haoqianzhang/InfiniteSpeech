import React, { Component } from 'react'
import { BrowserRouter as Router, Route } from "react-router-dom";
import { PostList, Post, SendPost } from '../Post' 

class App extends Component {
    render() {
        return (
            <Router>
                <div className="app">
                    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                        <div className="container">
                            <div className="navbar-brand">Infinit Speech</div>
                        </div>
                    </nav>
                    <div className="space-lg"></div>

                    <Route exact path="/" component={ PostList } />
                    <Route path="/post/:postId" component={ Post } />

                    <div className="space-xl"></div>

                    <SendPost />
                </div>
            </Router>
        )
    }
}

export default App