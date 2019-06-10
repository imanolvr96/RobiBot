import React, { Component } from "react";
import axios from 'axios';
import './citas.css';

export default class Citas extends React.Component {
  state = {
    citas: [],
    id: ''
  }

  componentDidMount() {
    axios.get(`http://b280ed02.ngrok.io/citas`)
      .then(res => {
        const citas = res.data;
        this.setState({ citas });
      })
  }


  handleChange = event => {
    this.setState({ id: event.target.value });
  }

  handleSubmit = event => {
    event.preventDefault();

    axios.delete(`http://b280ed02.ngrok.io/deleteR/${this.state.id}`)
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
  }

  render() {
    return (
      <div>

        <div>
          <form onSubmit={this.handleSubmit}>
            <label>
              Person ID:
              <input type="text" name="id" onChange={this.handleChange} />
            </label>
            <button type="submit">Delete</button>
          </form>
        </div>

        <hr/><hr/>


        <table>
          <tr>
            <th>ID</th>
            <th>FECHA</th>
            <th>HORA</th>
            <th>TELEFONO</th>
          </tr>
          <tr>
            <td>{this.state.citas.map(citas => <li>{citas.id}</li>)}</td>
            <td>{this.state.citas.map(citas => <li>{citas.fecha}</li>)}</td>
            <td>{this.state.citas.map(citas => <li>{citas.hora}</li>)}</td>
            <td>{this.state.citas.map(citas => <li>{citas.telefono}</li>)}</td>
          </tr>
        </table>
      </div>
    )
  }
}
