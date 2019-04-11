import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Report {

    @observable contents_1 = [];
    @observable contents_2 = [];

    @observable measures_1 = []
    @observable measures_2 = []

    @observable exam_managers = []

    @observable exam_teams = []

    @observable orgtypes = [];

    @observable orgs = [];
    @observable org = null;

    @observable managers = [];
    @observable manager = null;

    @observable charts = [];

    @observable report_loading = false;

    constructor() {
    }

    @action
    loadTree() {
        try {
            app.updateLoading(true);
            axios({
                method:'get',
                url:'/api/v1/org_type',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','report','load',resp.data);
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.orgtypes = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/org',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','report','load',resp.data);
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.orgs = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/exam_measure',
                params: {
                    exam_id:1
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.measures_1 = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/exam_measure',
                params: {
                    exam_id:2
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.measures_2 = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/exam_content',
                params: {
                    exam_id:1
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.contents_1 = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/exam_content',
                params: {
                    exam_id:2
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.contents_2 = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
            axios({
                method:'get',
                url:'/api/v1/manager',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.managers = list
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    loadExamManagers(year) {
        try {
            app.updateLoading(true);
            this.report_loading = true;
            axios({
                method:'post',
                url:'/api/v1/report_managers',
                data:qs.stringify({year:year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.exam_managers = list;
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
                this.report_loading = false;
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            this.report_loading = false;
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    loadExamTeams(year) {
        try {
            app.updateLoading(true);
            this.report_loading = true;
            axios({
                method:'post',
                url:'/api/v1/report_teams',
                data:qs.stringify({year:year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.exam_teams = list;
                } else {
                    throw new Error(message||'发生错误');
                }
                app.updateLoading(false);
                this.report_loading = false;
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            this.report_loading = false;
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    loadOrgChart(org,start_year,end_year) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/report_teams_chart',
                data:qs.stringify({org_id:org.id,start_year:start_year,end_year:end_year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.charts = list;
                } else {
                    throw new Error(message||'发生错误');
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    loadManagerChart(manager,start_year,end_year) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/report_managers_chart',
                data:qs.stringify({manager_id:manager.id,start_year:start_year,end_year:end_year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.charts = list;
                } else {
                    throw new Error(message||'发生错误');
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    doExportTeam(path,year) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/report_team_export');
                source.onmessage = function(e) {
                    console.log('**********',e);
                    let o = JSON.parse(e);
                    if(!!o["data"]) {
                        app.updateTip('已完成'+o["data"]+'%...');
                    }
                }
            }

            axios({
                method:'post',
                url:'/api/v1/report_team_export',
                data:qs.stringify({path,year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导出完成'});
                app.updateTip('载入中');
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    doExportManager(path,year) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/report_manager_export');
                source.onmessage = function(e) {
                    console.log('**********',e);
                    let o = JSON.parse(e);
                    if(!!o["data"]) {
                        app.updateTip('已完成'+o["data"]+'%...');
                    }
                }
            }

            axios({
                method:'post',
                url:'/api/v1/report_manager_export',
                data:qs.stringify({path,year},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导出完成'});
                app.updateTip('载入中');
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

}

export default new Report();