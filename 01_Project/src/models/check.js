import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Check {

    constructor() {
    }

    @observable orgtypes = [];

    @observable orgs = [];
    @observable org = null;

    @observable messages = [];

    @action
    load() {
        try {
            app.updateLoading(true);
            axios({
                method:'get',
                url:'/api/v1/org_type',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','score','load',resp.data);
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
                console.log('models','score','load',resp.data);
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
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    check(year,orgs) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/check',
                data:qs.stringify({year,orgs},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','check','check',resp.data);
                const { success,message } = resp.data;
                if(success==1) {
                    this.messages = message;
                    notification.open({ message: '操作提示', description: '已验证完成'});
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
    compute(year,orgs) {
        try {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/compute',
                data:qs.stringify({year,orgs},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','check','check',resp.data);
                const { success,message } = resp.data;
                if(success==1) {
                    this.messages = message;
                    notification.open({ message: '操作提示', description: '已计算完成'});
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

export default new Check();