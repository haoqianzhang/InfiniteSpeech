import React, { Component } from 'react'
import { PostItem } from '../Post'
import axios from 'axios'

const URL_ROOT='http://localhost:8001/'

class App extends Component {
    constructor() {
        super()
        this.state = {
            posts: []
        }
    }

    componentDidMount() {
        let self = this
        axios.get(URL_ROOT + 'posts/10')
            .then(function (response) {
                self.setState({
                    posts: response.data
                })
            })
            .catch(function (error) {
                console.log(error)
            })
    }

    render() {
        let posts = []
        this.state.posts.forEach((element, index) => {
            posts.push(<PostItem key={index} post={element} />)
        })
        return (
            <div className="app">
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div className="container">
                        <div className="navbar-brand">Infinit Speech</div>
                    </div>
                </nav>
                <div className="space-lg"></div>
                <div className="container">
                    <div className="list-group post-item">
                        { posts }
                    </div>
                </div>
            </div>
        )
    }
}

export default App