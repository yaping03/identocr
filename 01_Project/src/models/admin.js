import { observable,action,computed } from 'mobx';
import axios from 'axios';
import qs from 'qs';
import routing from './routing';
import { notification } from 'antd';

import app from './app';

class Admin {

    @observable admin = null;

    constructor() {
    }

    @action
    verify = (username,password) => {
        if(!!username&&!!password) {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/verify',
                data:qs.stringify({ username,password }),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','admin','verify',resp.data);
                const { success,admin } = resp.data;
                if(success==1) {
                    this.admin = admin;
                    notification.open({ message: '操作提示', description: '登录成功' });
                    routing.push('/home');
                } else {
                    notification.open({ message: '操作提示', description: '用户名或密码不正确!'});
                }
                app.updateLoading(false);
            }).catch(e => {
                console.error(e);
                notification.open({ message: '操作提示', description: '用户名或密码不正确!' });
                app.updateLoading(false);
            });
        } else {
            notification.open({ message: '操作提示', description: '请输入用户名和密码!' });
            app.updateLoading(false);
        }
    }

    @action
    update = (old_password,new_password,confirm_password) => {
        if(!!old_password&&!!new_password&&!!confirm_password&&new_password==confirm_password) {
            app.updateLoading(true);
            axios({
                method:'post',
                url:'/api/v1/admin/0',
                data:qs.stringify({ old_password,new_password,confirm_password }),
                headers:{ 'Content-Type': 'application/x-www-form-urlencoded' }
            }).then(resp => {
                console.log('models','admin','update',resp.data);
                const { success,admin } = resp.data;
                if(success==1) {
                    notification.open({ message: '操作提示', description: '修改成功' });
                } else {
                    notification.open({ message: '操作提示', description: '修改失败!'});
                }
                app.updateLoading(false);
            }).catch(e => {
                console.error(e);
                notification.open({ message: '操作提示', description: '修改失败!' });
                app.updateLoading(false);
            });
        } else {
            notification.open({ message: '操作提示', description: '请输入密码!' });
            app.updateLoading(false);
        }
    }

}

export default new Admin();