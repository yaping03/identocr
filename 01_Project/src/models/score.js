import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Score {

    @observable model = 'list';

    @observable orgtypes = [];

    @observable orgs = [];
    @observable org = null;

    @observable weights = [];
    @observable scores = [];

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
                    url:'/api/v1/org',
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
                            this.orgs = list;
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
            mnotification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    selectOrg(org) {
        this.org = org;
        if(!!this.org) {
            this.loadData();
        }
    }

    @action
    loadData() {
        try {

            console.log('score loadData',this.org);

            if(!!this.org) {
                app.updateLoading(true);
                Promise.all([
                    axios({
                        method:'get',
                        url:'/api/v1/team_year_weight',
                        params: {
                            org_id:this.org.id
                        },
                        headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                    }),
                    axios({
                        method:'get',
                        url:'/api/v1/team_score',
                        params: {
                            org_id:this.org.id
                        },
                        headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                    }),
                    axios({
                        method:'get',
                        url:'/api/v1/exam_result_team_score',
                        params: {
                            org_id:this.org.id
                        },
                        headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                    })
                ]).then(resps => {
                    resps.map((resp,index)=>{
                        if(index==0) {
                            const { success,list,message } = resp.data;
                            if(success==1) {
                                if(this.model=='add') {
                                    this.model = "added";
                                }
                                this.weights = list;
                            } else {
                                throw new Error(message);
                            }
                        } else if(index==1) {
                            const { success,list,message } = resp.data;
                            if(success==1) {
                                this.scores = list;
                            } else {
                                throw new Error(message);
                            }
                        } else if(index==2) {
                            const { success,list,message } = resp.data;
                            if(success==1) {
                                this.results = list;
                            } else {
                                throw new Error(message);
                            }                        
                        }
                        if(this.weights.length>0&&this.scores.length>0) {
                            let weights = [];
                            ([...this.weights]).map((weight,index)=>{
                                weight.score_1 = (this.scores.find((item)=>{
                                    return item.org_id==weight.org_id && item.year==weight.year && item.exam_measure.name=='企业党建';
                                })||{}).score;
                                weight.score_2 = (this.scores.find((item)=>{
                                    return item.org_id==weight.org_id && item.year==weight.year && item.exam_measure.name=='绩效成果';
                                })||{}).score;
                                weights.push(weight);
                            });
                            this.weights = weights;
                        }
                    });
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
    update(id,data) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/team_year_weight/'+id,
                data:qs.stringify(data),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.loadData();
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
    add() {
        try {
            if(!!this.org) {
                app.updateLoading(true);
                axios({
                    method:'post',
                    url:'/api/v1/team_year_weight',
                    data:qs.stringify({ org_id:this.org.id }),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        this.model = "add";
                        this.loadData();
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            } else {
                throw new Error('请选择单位');
            }
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    cancel() {
        if(!!this.weights&&!!this.weights[this.weights.length-1]&&this.weights[this.weights.length-1].id==0&&
           !!this.scores&&!!this.scores[this.scores.length-1]&&this.scores[this.scores.length-1].id==0){
            this.weights.splice(-1,1);
            this.scores.splice(-1,1);
        }
    }

    @action
    delete(ids=[]) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/team_year_weight/delete',
                data:qs.stringify({ids},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.loadData();
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

}

export default new Score();