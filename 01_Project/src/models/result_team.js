import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class ResultTeam {

    @observable measures = [];

    @observable orgtypes = [];

    @observable entities = [];
    @observable entity = null;

    @observable orgs = [];
    @observable org = null;

    @observable years = [];
    @observable year = null;

    @observable results = [];

    constructor() {
    }

    @action
    load() {
        try {
            app.updateLoading(true);
            Promise.all([
                axios({
                    method:'get',
                    url:'/api/v1/org_type',
                    params: {
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }),
                axios({
                    method:'get',
                    url:'/api/v1/exam_entity',
                    params: {
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }),
                axios({
                    method:'get',
                    url:'/api/v1/org',
                    params: {
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }),
                axios({
                    method:'get',
                    url:'/api/v1/exam_measure',
                    params: {
                        exam_id:1
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                })
            ]).then(resps => {
                app.updateLoading(false);
                resps.map((resp,index)=>{
                    if(index==0) {
                        const { success,list,message } = resp.data;
                        if(success==1) {
                            this.orgtypes = list;
                        } else {
                            throw new Error(message);
                        }
                    } else if(index==1) {
                        const { success,list,message } = resp.data;
                        if(success==1) {
                            this.entities = list;
                            if(!!this.entities&&[...this.entities].length>0) {
                                this.entity = this.entities[0];
                            }
                        } else {
                            throw new Error(message);
                        }
                    } else if(index==2) {
                        const { success,list,message } = resp.data;
                        if(success==1) {
                            this.orgs = list;
                        } else {
                            throw new Error(message);
                        }
                    } else if(index==3) {
                        const { success,list,message } = resp.data;
                        if(success==1) {
                            this.measures = list;
                        } else {
                            throw new Error(message);
                        }
                    }
                });
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
    selectOrg(org) {
        this.org = org;
        if(!!this.org) {
            this.results = [];
            this.loadYear();
        }
    }

    @action
    selectYear(year) {
        this.year = year;
        if(!!this.year) {
            this.loadResult();
        }
    }

    @action
    loadYear() {
        try {
            if(!!this.org) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/exam_result_team_year',
                    params: {
                        org_id:this.org.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.years = list
                        if(!!this.years&&[...this.years].length>0) {
                            this.selectYear(list[0]);
                        }
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            }
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    loadResult() {
        try {
            console.log(this.year,this.org,this.entity);
            if(!!this.year&&!!this.org&&!!this.entity) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/exam_result_team',
                    params: {
                        year:this.year,
                        org_id:this.org.id,
                        exam_entity_id:this.entity.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    console.log('models','ResultTeam','loadResult',resp.data);
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.results = list
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            }
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    do_export(path) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/result_org_export');
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
                url:'/api/v1/result_org_export',
                data:qs.stringify({path,year:this.year,org_id:this.org.id,exam_entity_id:this.entity.id},{arrayFormat:'brackets'}),
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

    @computed get result_teams() {
        let result = [];
        let results = [...this.results];
        for(let i=0;i<results.length;i++) {
            let r = results[i];
            let found = false;
            for(let j=0;j<result.length;j++) {
                let t = result[j];
                if(t.org_id==r.org_id&&t.year==r.year&&t.image_path==r.image_path&&t.exam_entity_id==r.exam_entity_id) {
                    found = true;
                    t.score[r.exam_measure_id] = { 
                        'exam_measure_id':r.exam_measure_id,
                        'exam_measure':r.exam_measure,
                        'score':r.score
                    };
                }
            }
            if(!found) {
                let nr = {
                    'image_path':r.image_path,
                    'exam_entity':r.exam_entity,
                    'exam_entity_id':r.exam_entity_id,
                    'org':r.org,
                    'org_id':r.org_id,
                    'validity':r.validity,
                    'year':r.year,
                    'score':{
                    }
                };
                nr.score[r.exam_measure_id] = { 
                    'exam_measure_id':r.exam_measure_id,
                    'exam_measure':r.exam_measure,
                    'score':r.score
                };
                result.push(nr);
            }
        }
        return result;
    }

}

export default new ResultTeam();