import { observable,action,computed } from 'mobx';
import axios from 'axios';
import { notification } from 'antd';
import qs from 'qs';

class App {

    @observable loading = false;

    @observable collapsed = true;

    @observable tip = '载入中...';

    constructor() {
    }

    @action
    updateCollapsed() {
        this.collapsed = !this.collapsed;
    }

    @action
    updateLoading(loading) {
        this.loading = loading;
    }

    @action
    updateTip(tip) {
        this.tip = tip;
    }

    @action
    do_import(path) {
        try {
            this.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/db_import');
                source.onmessage = function(e) {
                    console.log('source.onmessage',e);
                    // let o = JSON.parse(e);
                    // if(!!o["data"]) {
                    //     this.updateTip('已完成'+o["data"]+'%...');
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

            console.log(path);

            axios({
                method:'post',
                url:'/api/v1/db_import',
                data:qs.stringify({path},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导入完成'});
                this.updateTip('载入中');
                this.updateLoading(false);
                this.load();
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            this.updateLoading(false);
        }
    }

    @action
    do_export(path) {
        try {
            this.updateLoading(true);

            if (!!window.EventSource) {
                var source = new EventSource('/api/v1/db_export');
                source.onmessage = function(e) {
                    console.log('**********',e);
                    let o = JSON.parse(e);
                    if(!!o["data"]) {
                        this.updateTip('已完成'+o["data"]+'%...');
                    }
                }
            }

            console.log(path);

            axios({
                method:'post',
                url:'/api/v1/org_export',
                data:qs.stringify({path},{arrayFormat:'brackets'}),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','generate','generate',resp.data);
                notification.open({ message: '操作提示', description: '已导出完成'});
                this.updateTip('载入中');
                this.updateLoading(false);
            }).catch(e => {
                throw e;
            });
        } catch(e) {
            console.error(e);
            notification.open({ message: '操作提示', description: e.message||'发生错误'});
            this.updateLoading(false);
        }
    }

}

export default new App();