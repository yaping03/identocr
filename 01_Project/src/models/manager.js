import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import moment from 'moment';

import app from './app';

class Manager {

    @observable model = 'manager';
    @observable view = 'list';

    @observable orgtypes = [];
    @observable orgtype = null;

    @observable managertypes = [];
    // @observable managertitles = [];

    @observable orgs = [];
    @observable org = null;

    @observable managers = [];
    @observable manager = null;

    @observable weights = [];

    @observable search_name = null;

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
                    url:'/api/v1/manager_type',
                    params: {
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }),
                // axios({
                //     method:'get',
                //     url:'/api/v1/manager_title',
                //     params: {
                //     },
                //     headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                // }),
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
                            this.managertypes = list;
                        } else {
                            throw new Error(message);
                        }
                    } else if(index==2) {
                    //     const { success,list,message } = resp.data;
                    //     if(success==1) {
                    //         this.managertitles = list;
                    //     } else {
                    //         throw new Error(message);
                    //     }
                    // } else if(index==3) {
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
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    selectAll() {
        this.model = 'manager';
        this.loadManager();
    }

    @action
    selectOrgType(org_type) {
        this.orgtype = org_type;
        this.org = null;
        this.model = 'manager';
        if(!!this.orgtype){
            this.loadManager();
        }
    }

    @action
    selectOrg(org) {
        this.org = org;
        this.model = 'manager';
        if(!!this.org) {
            this.loadManager();
        }
    }

    @action
    selectManager(manager) {
        this.manager = manager;
        this.model = 'weight';
        if(!!this.manager) {
            this.loadWeight(); 
        }
    }

    @action
    loadManager() {
        try {
            let params = {};
            if(!!this.org) {
                params.org_id = this.org.id;
            }
            if(!!this.orgtype) {
                params.org_type_id = this.orgtype.id;
            }
            if(!!this.search_name) {
                params.search_name = this.search_name;
            }
            app.updateLoading(true);
            axios({
                method:'get',
                url:'/api/v1/manager',
                params: params,
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.managers = list;
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
    loadWeight() {
        try {
            if(!!this.manager) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/manager_year_weight',
                    params: {
                        manager_id:this.manager.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.weights = list
                        if(this.view=='add') {
                            this.view = "added";
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
    update(id,data) {
        try {
            if(this.model=='manager') {
                app.updateLoading(true);
                axios({
                    method:'post',
                    url:'/api/v1/manager/'+id,
                    data:qs.stringify(data),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        this.loadManager();
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            } else {
                axios({
                    method:'post',
                    url:'/api/v1/manager_year_weight/'+id,
                    data:qs.stringify(data),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        this.loadWeight();
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
    add() {
        if(this.model=='manager') {
            const data = {
                id: 0,
                org_id: this.org.id,
                org: this.org,
                name: '',
                manager_type_id: null,
                manager_type: null,
                title:'',
                // manager_title_id: null,
                // manager_title: null,
                sort: 1,
                create_at: null,
                update_at: null
            };
            this.managers.push(data);
        } else {
            // const data = {
            //     id: 0,
            //     manager_id: this.manager.id,
            //     manager: this.manager,
            //     year: 0,
            //     weight: 0,
            //     sort: 1,
            //     create_at: null,
            //     update_at: null
            // };
            // if(this.weights.length==0){
            //     data.weight = 100;
            //     data.year = moment().format('YYYY');
            // }
            // if(this.weights.length==1){
            //     let w = this.weights[0];
            //     if(!!w) {
            //         data.weight = 50;
            //         data.year = w.year - 1;
            //         if(w.year!=moment().format('YYYY')){
            //             data.year = moment().format('YYYY');
            //         }
            //     }
            // }
            // if(this.weights.length==2){
            //     let w = this.weights[1];
            //     if(!!w) {
            //         data.weight = 30;
            //         data.year = w.year - 1;
            //         if(this.weights[0].year!=moment().format('YYYY')){
            //             data.year = moment().format('YYYY');
            //         }
            //     }
            // }
            // this.weights.push(data);
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/manager_year_weight',
                data:qs.stringify({ manager_id:this.manager.id,year:0,weight:0,sort:1 }),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.view = "add";
                    this.loadWeight();
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        }
    }

    @action
    cancel() {
        if(this.model=='manager') {
            if(!!this.managers&&!!this.managers[this.managers.length-1]&&this.managers[this.managers.length-1].id==0){
                this.managers.splice(-1,1);
            }
        } else {
            if(!!this.weights&&!!this.weights[this.weights.length-1]&&this.weights[this.weights.length-1].id==0){
                this.weights.splice(-1,1);
            }
        }
    }

    @action
    save(data) {
        try {
            if(this.model=='manager') {
                app.updateLoading(true);
                axios({
                    method:'post',
                    url:'/api/v1/manager',
                    data:qs.stringify(data),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        this.loadManager();
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            } else {
                // app.updateLoading(true);
                // axios({
                //     method:'post',
                //     url:'/api/v1/manager_year_weight',
                //     data:qs.stringify(data),
                //     headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                // }).then(resp => {
                //     const { success,message } = resp.data;
                //     if(success==1) {
                //         this.loadWeight();
                //     } else {
                //         throw new Error(message);
                //     }
                //     app.updateLoading(false);
                // }).catch(e => {
                //     throw e;
                // });
            }
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    delete(ids=[]) {
        try {
            if(this.model=='manager') {
                app.updateLoading(true);
                axios({
                    method:'post',
                    url:'/api/v1/manager/delete',
                    data:qs.stringify({ids},{arrayFormat:'brackets'}),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        if(this.model=='manager') {
                            this.loadManager();
                        } else {
                            this.loadWeight();
                        }
                    } else {
                        throw new Error(message);
                    }
                    app.updateLoading(false);
                }).catch(e => {
                    throw e;
                });
            } else {
                app.updateLoading(true);
                axios({
                    method:'post',
                    url:'/api/v1/manager_year_weight/delete',
                    data:qs.stringify({ids},{arrayFormat:'brackets'}),
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,message } = resp.data;
                    if(success==1) {
                        if(this.model=='manager') {
                            this.loadManager();
                        } else {
                            this.loadWeight();
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
    do_import(path) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/manager_import');
                source.onmessage = function(e) {
                    console.log('source.onmessage',e);
                    // let o = JSON.parse(e);
                    // if(!!o["data"]) {
                    //     app.updateTip('已完成'+o["data"]+'%...');
                    // }
                    // if(!!o["message"]) {
                    //     notification.open({ message: '操作提示', description: o["message"]});
                    // }
                };
                source.onerror = function(e) {
                    console.error("EventSource failed.");
                    source.close();
                };
            }

            axios({
                method:'post',
                url:'/api/v1/manager_import',
                data:qs.stringify({path},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导入完成'});
                app.updateTip('载入中');
                app.updateLoading(false);
                this.loadManager();
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
    do_export(path) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/manager_export');
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
                url:'/api/v1/manager_export',
                data:qs.stringify({path},{arrayFormat:'brackets'}),
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

export default new Manager();