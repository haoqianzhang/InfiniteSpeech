import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import { MuiThemeProvider, createMuiTheme } from 'material-ui/styles'
import './index.css'

const theme = createMuiTheme()

function Root() {
    return (
        <MuiThemeProvider theme={theme}>
            <App />
        </MuiThemeProvider>
    );
}

ReactDOM.render(<Root />, document.getElementById('root'))