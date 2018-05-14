import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class PostItem extends Component {
    render() {
        return (
            <Link 
                to={ '/post/' + this.props.post.post_id } 
                className="list-group-item list-group-item-action flex-column align-items-start"
            >
                <div className="d-flex w-100 justify-content-between">
                    <h5 className={ this.props.post.confirmed ? "m-0 post-title" : "m-0 post-title text-danger"}>{ this.props.post.title }</h5>
                    <h5 className="m-0 text-muted font-weight-light post-nickname">{ this.props.post.name }</h5>
                </div>
            </Link>
        )
    }
}

export default PostItem