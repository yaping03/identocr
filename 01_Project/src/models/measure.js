import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Measure {

    @observable exams = [];

    @observable exam = null;
    @observable measures = [];

    constructor() {
    }

    @action
    load() {
        try {
            app.updateLoading(true);
            axios({
                method:'get',
                url:'/api/v1/exam',
                params: {
                },
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,list,message } = resp.data;
                if(success==1) {
                    this.exams = list;
                    if(!!this.exams&&this.exams.length>0) {
                        this.selectExam(this.exams[0]);
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
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            app.updateLoading(false);
        }
    }

    @action
    selectExam(exam) {
        this.exam = exam;
        if(!!this.exams) {
            this.loadMeasure();
        }
    }

    @action
    loadMeasure() {
        try {
            if(!!this.exam) {
                app.updateLoading(true);
                axios({
                    method:'get',
                    url:'/api/v1/exam_measure',
                    params: {
                        exam_id:this.exam.id
                    },
                    headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
                }).then(resp => {
                    const { success,list,message } = resp.data;
                    if(success==1) {
                        this.measures = list;
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
                url:'/api/v1/exam_measure/'+id,
                data:qs.stringify(data),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                const { success,message } = resp.data;
                if(success==1) {
                    this.loadMeasure();
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

export default new Measure();