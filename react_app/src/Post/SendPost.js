import React, { Component } from 'react'
import axios from 'axios'
import { URL_ROOT } from '../config'

class SendPost extends Component {
    constructor() {
        super()
        this.state = {
            title: '',
            name: '',
            email: '',
            content: ''
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleChange(event) {
        let state = {}
        state[event.target.name] = event.target.value
        this.setState(state)
    }

    handleSubmit(event) {
        event.preventDefault()

        let data = {
            reply_to: '',
            category: '/hello/world',
            input_time: Math.floor(Date.now() / 1000),
            client: 'Infnote React APP'
        }
        data = Object.assign(data, this.state)

        let self = this
        axios.get(URL_ROOT + 'quota')
            .then(function (response) {
                self.send(response.data, data)
            })
            .catch(function (error) {
                console.log(error)
            })
    }

    send(quota, data) {
        let hex = window.bitcoinPost(quota['txid'], quota['vout'], quota['amount'], data)
        let self = this
        
        axios.post(URL_ROOT + 'post', {hex: hex})
            .then(function (response) {
                self.setState({content: ''})
                alert('Post has been sent, post id: ' + response.data.pid)
                window.location.reload();
            })
            .catch(function (error) {
                console.log(error)
            })
            
    }

    render() {
        return (
            <div className="container">
                <form onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <input type="text" className="form-control" id="send-title" name="title" placeholder="Title" onChange={this.handleChange} />
                    </div>
                    <div className="form-row">
                        <div className="form-group col-md-6">
                            <input type="text" className="form-control" id="send-nickname" name="name" placeholder="Nickname" onChange={this.handleChange} />
                        </div>
                        <div className="form-group col-md-6">
                            <input type="email" className="form-control" id="send-email" name="email" placeholder="Email" onChange={this.handleChange} />
                        </div>
                    </div>
                    <div className="form-group">
                        <textarea className="form-control" id="send-content" name="content" rows="20" onChange={this.handleChange} value={this.state.content} ></textarea>
                    </div>
                    <button type="submit" className="btn btn-primary" data-toggle="modal" data-target="#success-modal">Submit</button>
                </form>
            </div>
        )
    }
}

export default SendPost