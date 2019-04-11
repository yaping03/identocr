import "babel-polyfill";

import React from 'react';
import ReactDOM from 'react-dom';
import { createBrowserHistory } from 'history';
import { Router, Route, Redirect, Switch } from 'react-router-dom';
import { Provider } from 'mobx-react';
import { syncHistoryWithStore } from 'mobx-react-router';

import './index.css';

import store from './models';

import Login from './pages/login';
import Home from './pages/home';
import Measure from './pages/measure';
import Entity from './pages/entity';
import Org from './pages/org';
import Score from './pages/score';
import Manager from './pages/manager';
import ResultManager from './pages/result_manager';
import ResultTeam from './pages/result_team';
import Db from './pages/db';
import Generate from './pages/generate';
import Check from './pages/check';
import ReportExam from './pages/report_exam';
import ReportManager from './pages/report_manager';
import ReportTeam from './pages/report_team';
import ReportPeople from './pages/report_people';
import Password from './pages/password';

const routing = store.routing;

const browserHistory = createBrowserHistory({
    basename: '/'
});

const history = syncHistoryWithStore(browserHistory, routing);

ReactDOM.render((
    <Provider { ...store }>
        <Router basename='/' history={history}>
            <Switch>
                <Route path="/login" component={ Login } />
                <Route path="/home" component={ Home } />
                <Route path="/measure" component={ Measure } />
                <Route path="/entity" component={ Entity } />
                <Route path="/org" component={ Org } />
                <Route path="/score" component={ Score } />
                <Route path="/manager" component={ Manager } />
                <Route path="/resultmanager" component={ ResultManager } />
                <Route path="/resultteam" component={ ResultTeam } />
                <Route path="/db" component={ Db } />
                <Route path="/generate" component={ Generate } />
                <Route path="/check" component={ Check } />
                <Route path="/reportexam" component={ ReportExam } />
                <Route path="/reportmanager" component={ ReportManager } />
                <Route path="/reportteam" component={ ReportTeam } />
                <Route path="/reportpeople" component={ ReportPeople } />
                <Route path="/password" component={ Password } />
                <Redirect to="/login" />
            </Switch>
        </Router>
    </Provider>
), document.getElementById('root'));