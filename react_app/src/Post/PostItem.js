import React, { Component } from 'react'

class PostItem extends Component {
    render() {
        return (
            <a className="list-group-item list-group-item-action flex-column align-items-start">
                <div className="d-flex w-100 justify-content-between">
                    <h5 className="m-0 post-title">{ this.props.post.title }</h5>
                    <h5 className="m-0 text-muted font-weight-light post-nickname">{ this.props.post.name }</h5>
                </div>
            </a>
        )
    }
}

export default PostItem