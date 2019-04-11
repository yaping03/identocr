import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Foot from '../components/foot';

import fs from 'fs';

import './login.css';

const bgjpg = fs.readFileSync(__dirname + '/../static/images/login.jpg');

@inject('app','admin')
@observer
export default class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        }
    }

    emitEmpty = (type) => {
        if(type==1) {
            this.usernameInput.focus();
            this.setState({ username:'' });
        } else {
            this.passwordInput.focus();
            this.setState({ password:'' });
        }
    }
      
    onChangeUsername = (e) => {
        this.setState({ username: e.target.value });
    }

    onChangePassword = (e) => {
        this.setState({ password: e.target.value });
    }

    onClickLogin = () => {
        this.props.admin.verify(this.state.username,this.state.password);
    }

    render() {
        const { username,password } = this.state;
        return (
            <Layout style={{ width:'100%',height:'100%' }}>
                <Layout.Content style={{ width:'100%',height:'100%',background:'#fff',overflow:'auto' }}>
                    <Spin tip={this.props.app.tip} spinning={this.props.app.loading}>
                        <div style={{ position:'absolute',width:'100%',height:'100%',zIndex:1 }}>
                            <img src={`data:image/png;base64,${bgjpg.toString('base64')}`} style={{ width:'100%',height:'100%' }} />
                        </div>

                        <div style={{ height:'100%',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'flex-start' }}>
                            <div style={{ flex:1 }}></div>
                            <div style={{ height:50,fontSize:28,display:'flex',justifyContent:'flex-start',zIndex:100 }}>中交上海航道局有限公司</div>
                            <div style={{ height:50,fontSize:28,display:'flex',justifyContent:'flex-start',zIndex:100 }}>中层干部和司属单位领导班子综合考评系统</div>
                            <div style={{ height:50,fontSize:16 }}></div>
                            <div style={{ width:'100%',height:300,display:'flex',flexDirection:'column',alignItems:'flex-end',justifyContent:'center',paddingRight:'20%',zIndex:100 }}>
                                <div style={{ width:400,height:300,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5,zIndex:100 }}>
                                        <Input
                                            placeholder="用户名"
                                            prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                            suffix={username ? <Icon type="close-circle" onClick={this.emitEmpty.bind(this,1)} /> : null}
                                            value={username}
                                            onChange={this.onChangeUsername}
                                            ref={node => this.usernameInput = node}
                                            style={{ width:'100%',marginLeft:15,marginRight:15 }}
                                        />
                                    </div>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Input
                                            placeholder="密码"
                                            type="password"
                                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                            suffix={password ? <Icon type="close-circle" onClick={this.emitEmpty.bind(this,2)} /> : null}
                                            value={password}
                                            onChange={this.onChangePassword}
                                            ref={node => this.passwordInput = node}
                                            style={{ width:'100%',marginLeft:15,marginRight:15 }}
                                        />
                                    </div>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Button style={{ width:'100%',marginLeft:15,marginRight:15 }} onClick={ this.onClickLogin }>
                                            登录
                                        </Button>
                                    </div>
                                </div>
                            
                                {/* <Button onClick={ ()=>{
                                    alert(window.interaction);
                                    try {
                                        window.interaction.open_dir_dialog((p)=>{
                                            alert(p);
                                        });
                                    } catch(e) {
                                        console.error(e);
                                    }
                                    // window.interaction.open_dir_dialog(function(p){
                                    //     alert(p);
                                    // });
                                } }>Test</Button> */}

                            </div>
                            <div style={{ height:100 }}></div>
                            <div style={{ flex:1 }}></div>
                        </div>
                    </Spin>
                </Layout.Content>
                <Layout.Footer style={{ width:'100%',height:'40px',padding:0,background:'#99c1d4' }}>
                    <Foot history={ this.props.history } />
                </Layout.Footer>
            </Layout>
        );
    }
}