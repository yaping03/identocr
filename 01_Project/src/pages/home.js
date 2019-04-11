import React from 'react';
import { inject, observer } from 'mobx-react';

import fs from 'fs';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';
import Foot from '../components/foot';

import './home.css';

const homepng = fs.readFileSync(__dirname + '/../static/images/home.png');

@inject('app','admin')
@observer
export default class Home extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    render() {
        return (
            <Layout style={{ width:'100%',height:'100%' }}>
                <Layout.Header style={{ width:'100%',height:'80px',padding:0,background:'#ffffff' }}>
                    <Top history={ this.props.history }/>
                </Layout.Header>
                <Layout style={{ width:'100%',height:'100%',background:'#fff' }}>
                    <Layout.Sider collapsible theme='light' collapsed={this.props.app.collapsed} onCollapse={()=>{ this.props.app.updateCollapsed() }} style={{ height:'100%' }}>
                        <Left collapsed={this.props.app.collapsed} history={ this.props.history }/>
                    </Layout.Sider>
                    <Layout.Content style={{ width:'100%',height:'100%',overflow: 'auto',background:'#ffffff',padding:10 }}>
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading}>
                            <div className="image" style={{ width:'100%',display:'flex',justifyContent:'center',alignItems:'center' }}>
                                <img src={`data:image/png;base64,${homepng.toString('base64')}`} style={{ width:'100%',maxWidth:800 }}/>
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