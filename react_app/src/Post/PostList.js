import React, { Component } from 'react'
import axios from 'axios'
import { PostItem } from '.'
import { GlobalStore } from '../Utils'
import { URL_ROOT, PAGE_SIZE } from '../config'

class PostList extends Component {
    constructor() {
        super()
        this.state = {
            posts: [],
            offset: 0
        }
    }

    componentDidMount() {
        this.fetchPosts()
    }

    fetchNextPosts() {
        let offset = this.state.offset
        offset += PAGE_SIZE
        this.fetchPosts(offset)
    }

    fetchPrevPosts() {
        let offset = this.state.offset
        offset -= PAGE_SIZE
        if (offset < 0) {
            return
        }
        this.fetchPosts(offset)
    }

    fetchPosts(offset=0) {
        let self = this
        if (Object.keys(GlobalStore.postMap).length >= PAGE_SIZE + offset) {
            let posts = []
            GlobalStore.postMap.forEach((element, index) => {
                posts.push(<PostItem key={index} post={element} />)
            })
            self.setState({
                posts: posts,
                offset: offset
            })
        } else {
            axios.get(URL_ROOT + 'posts/' + PAGE_SIZE + '/offset/' + offset)
            .then(function (response) {
                let posts = []
                response.data.forEach((element, index) => {
                    GlobalStore.postMap[element.post_id] = element
                    posts.push(<PostItem key={index} post={element} />)
                })
                self.setState({
                    posts: posts,
                    offset: offset
                })
            })
            .catch(function (error) {
                console.log(error)
            })
        }
    }

    render() {
        return (
            <div className="container">
                <div className="list-group post-item">
                    { this.state.posts }
                </div>
                <div className="space-md"></div>
                <nav aria-label="Page navigation">
                    <ul className="pagination justify-content-center">
                        <li 
                            className={this.state.offset > 0 ? 'page-item' : 'page-item disabled'} 
                            onClick={ () => this.fetchPrevPosts() }
                        >
                            <a className="page-link">Previous { PAGE_SIZE }</a>
                        </li>

                        <li 
                            className="page-item" 
                            onClick={ () => this.fetchNextPosts() }
                        >
                            <a className="page-link">Next { PAGE_SIZE }</a>
                        </li>
                    </ul>
                </nav>
            </div>
        )
    }
}

export default PostList