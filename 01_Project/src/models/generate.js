import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Generate {

    @observable orgtypes = [];

    @observable orgs = [];
    @observable org = null;

    constructor() {
    }

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
    generate(path,orgs,datetime) {
        try {
            console.log('========',path,orgs,datetime);
            if(!!!orgs||orgs.length==0) {
                notification.open({ message: '操作提示', description: '请选择单位' });
                return;
            }
            if(!!!datetime) {
                notification.open({ message: '操作提示', description: '请输入考评年度' });
                return;
            }
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/generate');
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
                url:'/api/v1/generate',
                data:qs.stringify({orgs,datetime,path},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '文件已生成'});
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

export default new Generate();