import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';
import { ifError } from 'assert';

class ResultManager {

    @observable measures = [];

    @observable orgtypes = [];

    @observable entities = [];
    @observable entity = null;

    @observable orgs = [];
    @observable org = null;

    @observable managers = [];
    @observable manager = [];

    @observable years = [];
    @observable year = null;

    @observable results = [];

    @observable allyears = [];

    @observable result_managers = [];

    @observable result_loading = false;

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
                        exam_id:2
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }),
                axios({
                    method:'get',
                    url:'/api/v1/exam_result_manager_all_year',
                    params: {
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                })
            ]).then(resps => {
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
                    } else if(index==4) {
                        const { success,list,message } = resp.data;
                        if(success==1) {
                            this.allyears = list;
                        } else {
                            throw new Error(message);
                        }
                    }
                });
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
    selectOrg(org) {
        this.org = org;
        if(!!this.org) {
            this.manager = [];
            this.managers = [];
            this.results = [];
            this.result_managers = [];
            this.loadManager();
        }
    }

    @action
    selectManager(manager) {
        let selectedManager = [...this.manager];
        selectedManager.push(manager);
        this.manager = selectedManager;
        this.do_compute();
    }

    @action
    clearManager() {
        this.manager = [];
        this.do_compute();
    }

    @action
    loadManager() {
        try {
            if(!!this.org) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/manager',
                    params: {
                        org_id:this.org.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.managers = list;
                        if(list.length>0) {
                            this.results = [];
                            this.result_managers = [];
                            this.loadResult();
                        } else {
                            this.results = [];
                            this.result_managers = [];
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
            if(!!this.org) {

                console.log('load result start....');

                this.result_loading = true;
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/exam_result_manager',
                    params: {
                        year:this.year,
                        exam_entity_id:this.entity.id,
                        org_id:this.org.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    console.log('load result end');
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.results = list;
                        this.do_compute();
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
            this.result_loading = false;
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    do_compute() {

        this.result_loading = true;

        let result = [];

        console.log('computed start....',this.results,this.results.length);
        
        for(let i=0;i<this.results.length;i++) {
            let r = this.results[i];

            if(!!this.org&&r.manager.org_id!=this.org.id)
                continue;

            let exist = false;
            for(let k=0;k<this.manager.length;k++) {
                let m = this.manager[k];
                if(r.manager_id == m.id){
                    exist = true;
                }
            }
            if(this.manager.length==0) exist = true;
            if(!exist) continue;

            let found = false;
            for(let j=0;j<result.length;j++) {
                let t = result[j];
                if(t.manager_id==r.manager_id&&t.image_path==r.image_path) {
                    found = true;
                    t.score[r.exam_measure_id] = { 
                        'exam_measure_id':r.exam_measure_id,
                        'exam_measure':r.exam_measure,
                        'score':r.score
                    };
                }
            }
            if(!found) {
                let row_key = r.image_path + '_' + r.manager_id;
                console.log('row_key',row_key);
                let nr = {
                    'row_key':row_key,
                    'image_path':r.image_path,
                    'exam_entity':r.exam_entity,
                    'exam_entity_id':r.exam_entity_id,
                    'manager':r.manager,
                    'manager_id':r.manager_id,
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

        console.log('computed end');

        this.result_managers = result;
        this.result_loading = false;
    }

    @action
    do_export(path) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/result_manager_export');
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
                url:'/api/v1/result_manager_export',
                data:qs.stringify({path,year:this.year,exam_entity_id:this.entity.id},{arrayFormat:'brackets'}),
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

export default new ResultManager();