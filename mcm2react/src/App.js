import React, {Component} from 'react';
import {
  BrowserRouter as Router,
  Route,
} from "react-router-dom";

import NavBar from './NavBar'
import IndexPage from './IndexPage';
import CampaignsPage from './CampaignsPage';

class App extends Component{

  render() {
    return (
      <Router>
        <div>
          <NavBar />
          <Route exact path="/" component={IndexPage} />
          <Route path="/campaigns" component={CampaignsPage} />
        </div>
      </Router>
    )
  }
}
export default App