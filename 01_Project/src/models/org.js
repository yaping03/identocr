import 'babel-polyfill';
import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Org {

    @observable orgs = [];

    @observable orgtypes = [];

    @observable model = 'list';

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
                resps.map((res,index)=>{
                    if(index==0) {
                        const { success,list,message } = res.data;
                        if(success==1) {
                            this.orgtypes = list;
                        } else {
                            throw new Error(message);
                        }
                    } else {
                        const { success,list,message } = res.data;
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
    update(id,data) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/org/'+id,
                data:qs.stringify(data),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.load();
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
        const data = {
            id: 0,
            org_type_id: null,
            org_type: null,
            short_name: '',
            full_name: '',
            sort: 1,
            create_at: null,
            update_at: null
        };
        this.orgs.push(data);
    }

    @action
    cancel() {
        if(!!this.orgs&&!!this.orgs[this.orgs.length-1]&&this.orgs[this.orgs.length-1].id==0){
            this.orgs.splice(-1,1);
        }
    }

    @action
    save(data) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/org',
                data:qs.stringify(data),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.load();
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
    delete(ids=[]) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/org/delete',
                data:qs.stringify({ids},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.load();
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
    do_import(path) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/org_import');
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
                url:'/api/v1/org_import',
                data:qs.stringify({path},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导入完成'});
                app.updateTip('载入中');
                app.updateLoading(false);
                this.load();
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
                var source = new EventSource('/api/v1/org_export');
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
                url:'/api/v1/org_export',
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

export default new Org();