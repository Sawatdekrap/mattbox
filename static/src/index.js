import React, {Component} from 'react';
import ReactDOM from 'react-dom';

class Form extends Component {
  constructor() {
    super();

    this.state = {
      value: ''
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    const {value} = event.target;
    this.setState({
      value: value
    });
  }

  render() {
    return (
      <div>
        <input
          type='text'
          value={this.state.value}
          onChange={this.handleChange}
        >
        </input>
        <p>{this.state.value}</p>
      </div>
    );
  }
}

const wrapper = document.getElementById('container');
wrapper ? ReactDOM.render(<Form />, wrapper) : false;
