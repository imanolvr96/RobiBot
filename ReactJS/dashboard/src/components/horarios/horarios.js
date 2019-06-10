import React, { Component } from "react";

import axios from 'axios';

export default class Horarios extends React.Component {
  state = {
    horarios: []
  }

  componentDidMount() {
    axios.get(`http://b280ed02.ngrok.io/horarios`)
      .then(res => {
        const horarios = res.data;
        this.setState({ horarios });
      })
  }

  render() {
    return (
      <table>
        <tr>
          <th>ID</th>
          <th>HORAS</th>
          <th>PLAZAS</th>
          <th></th>
        </tr>
        <tr>
          <td>{this.state.horarios.map(horarios => <li>{horarios.id}</li>)}</td>
          <td>{this.state.horarios.map(horarios => <li>{horarios.horas}</li>)}</td>
          <td>{this.state.horarios.map(horarios => <li>{horarios.plazas}</li>)}</td>
          <td>{this.state.horarios.map(horarios => <li><button>Borrar</button></li>)}</td>
        </tr>
      </table>
    )
  }
}
