import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Route, NavLink, HashRouter } from 'react-router-dom';
import Inicio from './../../components/inicio/inicio.js';
import Citas from './../../components/citas/citas.js';
import Horarios from './../../components/horarios/horarios.js';

function App() {
  return (
    <HashRouter>
        <div>
          <ul className="header">
            <li><NavLink exact to="/">Inicio</NavLink></li>
            <li><NavLink to="/citas">Citas</NavLink></li>
            <li><NavLink to="/horarios">Horarios</NavLink></li>
          </ul>
          <div className="content">
            <Route exact path="/" component={Inicio}/>
            <Route path="/citas" component={Citas}/>
            <Route path="/horarios" component={Horarios}/>
          </div>
        </div>
      </HashRouter>
  );
}

export default App;

/*

<div className="App">
  <header className="App-header">
    <img src={logo} className="App-logo" alt="logo" />
    <p>
      Edit <code>src/App.js</code> and save to reload.
    </p>
    <a
      className="App-link"
      href="https://reactjs.org"
      target="_blank"
      rel="noopener noreferrer"
    >
      Learn React
    </a>
  </header>
</div>

*/
