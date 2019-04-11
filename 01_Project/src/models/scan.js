import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Scan {

    constructor() {
    }

    @action
    scan(path,orgs,datetime) {
        try {
            app.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/scan');
                source.onmessage = function(e) {
                    console.log('**********',e);
                    // let o = JSON.parse(e);
                    // if(!!o["data"]) {
                    //     app.updateTip('已完成'+o["data"]+'%...');
                    // }
                    notification.open({ message: '操作提示', description: '错误图片'+e});
                }
            }

            axios({
                method:'post',
                url:'/api/v1/scan',
                data:qs.stringify({path,orgs,datetime:datetime},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                if(!!resp.data) {
                    notification.open({ message: '操作提示', description: '错误图片'+resp.data});
                } else {
                    notification.open({ message: '操作提示', description: '已识别完成'});
                }
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

export default new Scan();