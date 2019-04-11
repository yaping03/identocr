import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './db.css';

@inject('app')
@observer
export default class DB extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    onImport = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('db-selected-directory', (event, path) => {
                this.props.app.do_import(path); 
            });
            ipcRenderer.send('db-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.open_db_file_dialog((p)=>{
                console.log(p);
                if(!!p) {
                    notification.open({ message: '操作提示', description: '路径'+p});
                    this.props.app.do_import(p);
                }
            });
        }
    }

    onExport = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('db-selected-directory', (event, path) => {
                this.props.app.do_export(path); 
            });
            ipcRenderer.send('db-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_db_file_dialog((p)=>{
                console.log(p);
                if(!!p) {
                    notification.open({ message: '操作提示', description: '路径'+p});
                    this.props.app.do_export(p);
                }
            });
        }
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
                            <div style={{ paddingLeft:30,paddingRight:30 }}>
                                <Button style={{ width:'100%' }} onClick={ this.onImport } style={{ width:200 }}>
                                    数据库导入
                                </Button>
                            </div>
                            <div style={{ height:20 }}></div>
                            <div style={{ paddingLeft:30,paddingRight:30 }}>
                                <Button style={{ width:'100%' }} onClick={ this.onExport } style={{ width:200 }}>
                                    数据库导出
                                </Button>
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