import React, { Component } from 'react'
import { GlobalStore } from '../Utils'

class Post extends Component {
    constructor(props) {
        super(props)
        this.post = GlobalStore.postMap[this.props.match.params.postId]
    }

    render() {
        return (
            <div className="container">
                <h1>{ this.post.title }</h1>
                <h5 className="text-muted">{ this.post.name }</h5>
                <div className="space-lg"></div>
                <p className="post-content">{ this.post.content }</p>
            </div>
        )
    }
}

export default Post