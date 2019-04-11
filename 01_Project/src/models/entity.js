import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Entity {

    @observable systems = [];
    @observable system = null;

    @observable weights = [];

    constructor() {
    }

    @action
    load() {
        try {
            app.updateLoading(true);
            axios({
                method:'get',
                url:'/api/v1/exam_system',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.systems = list;
                    if(!!this.systems&&this.systems.length>0) {
                        this.selectSysten(this.systems[0]);
                    }
                } else {
                    throw new Error(message);
                }
                app.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误' });
            app.updateLoading(false);
        }
    }

    @action
    selectSysten(system) {
        this.system = system;
        if(!!this.system) {
            this.loadWeight();
        }
    }

    @action
    loadWeight() {
        try {
            if(!!this.system) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/exam_entity_weight',
                    params: {
                        exam_system_id:this.system.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.weights = list
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
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/exam_entity_weight/'+id,
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
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

}

export default new Entity();