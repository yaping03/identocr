import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './password.css';

@inject('app','admin')
@observer
export default class Password extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            old_password:'',
            new_password:'',
            confirm_password:''
        }
    }

    emitEmpty = (type) => {
        if(type==1) {
            this.oldPasswordInput.focus();
            this.setState({ old_password:'' });
        } else if(type==2) {
            this.newPasswordInput.focus();
            this.setState({ new_password:'' });
        } else {
            this.confirmPasswordInput.focus();
            this.setState({ confirm_password:'' });
        }
    }
      
    onChangeOldPassword = (e) => {
        this.setState({ old_password: e.target.value });
    }

    onChangeNewPassword = (e) => {
        this.setState({ new_password: e.target.value });
    }

    onChangeConfirmPassword = (e) => {
        this.setState({ confirm_password: e.target.value });
    }

    onClickUpdate = () => {
        this.props.admin.update(this.state.old_password,this.state.new_password,this.state.confirm_password);
    }

    render() {
        console.log(this.props);
        return (
            <Layout style={{ width:'100%',height:'100%' }}>
                <Layout.Header style={{ width:'100%',height:'80px',padding:0,background:'#ffffff' }}>
                    <Top history={ this.props.history }/>
                </Layout.Header>
                <Layout style={{ width:'100%',height:'100%',background:'#fff' }}>
                    <Layout.Sider collapsible theme='light' collapsed={this.props.app.collapsed} onCollapse={()=>{ this.props.app.updateCollapsed() }} style={{ height:'100%' }}>
                        <Left collapsed={this.props.app.collapsed} history={ this.props.history }/>
                    </Layout.Sider>
                    <Layout.Content style={{ width:'100%',height:'100%',overflow: 'auto',background:'#f0f8ff',padding:10 }}>
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading}>
                            <div style={{ height:'100%',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                                <div style={{ width:400,height:300,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Input
                                            placeholder="原密码"
                                            type="password"
                                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                            suffix={this.state.old_password ? <Icon type="close-circle" onClick={this.emitEmpty.bind(this,1)} /> : null}
                                            value={this.state.old_password}
                                            onChange={this.onChangeOldPassword}
                                            ref={node => this.oldPasswordInput = node}
                                            style={{ width:'100%',marginLeft:15,marginRight:15 }}
                                        />
                                    </div>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Input
                                            placeholder="新密码"
                                            type="password"
                                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                            suffix={this.state.new_password ? <Icon type="close-circle" onClick={this.emitEmpty.bind(this,2)} /> : null}
                                            value={this.state.new_password}
                                            onChange={this.onChangeNewPassword}
                                            ref={node => this.newPasswordInput = node}
                                            style={{ width:'100%',marginLeft:15,marginRight:15 }}
                                        />
                                    </div>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Input
                                            placeholder="确认密码"
                                            type="password"
                                            prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                            suffix={this.state.confirm_password ? <Icon type="close-circle" onClick={this.emitEmpty.bind(this,3)} /> : null}
                                            value={this.state.confirm_password}
                                            onChange={this.onChangeConfirmPassword}
                                            ref={node => this.confirmPasswordInput = node}
                                            style={{ width:'100%',marginLeft:15,marginRight:15 }}
                                        />
                                    </div>
                                    <div style={{ width:'100%',display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                                        <Button style={{ width:'100%',marginLeft:15,marginRight:15 }} onClick={ this.onClickUpdate }>
                                            确定
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </Spin>
                    </Layout.Content>
                </Layout>
                <Layout.Footer style={{ width:'100%',height:'40px',padding:0,background:'#99c1d4' }}>
                    <Foot history={ this.props.history } />
                </Layout.Footer>
            </Layout>
        )
    }
}