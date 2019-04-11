import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import moment from 'moment';
import Foot from '../components/foot';

import './generate.css';

@inject('app','generate','scan')
@observer
export default class Generate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            datetime:moment().format('YYYY'),
            orgs:[]
        }
    }

    componentWillMount() {
        this.props.generate.load();
    }

    onCheck = (checkedKeys, info) => {
        let orgs = [];
        checkedKeys.filter((item)=>{
            for(let i=0;i<this.props.generate.orgs.length;i++){
                if(('0-0-0-'+i)==item) {
                    orgs.push(this.props.generate.orgs[i].id);
                }
            }
        });
        this.setState({ orgs });
    }

    onChangeDatetime = (value) => {
        this.setState({ datetime: value+'' });
    }

    generate = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('import-selected-directory', (event, path) => {
                this.props.generate.generate(path,this.state.orgs,this.state.datetime);
            });
            ipcRenderer.send('import-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.open_dir_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.generate.generate(p,this.state.orgs,this.state.datetime);
                }
            });
        }
    }

    onOpen = () => {
        try {
            if(!!!this.state.orgs || this.state.orgs.length==0) {
                notification.open({ message: '操作提示', description: '请选择单位' });
                return;
            }
            if(this.state.orgs.length>1) {
                notification.open({ message: '操作提示', description: '只能选择一个单位进行识别' });
                return;
            }
            if(!!!this.state.datetime) {
                notification.open({ message: '操作提示', description: '请输入考评年度' });
                return;
            }

            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('scan-selected-directory', (event, path) => {
                this.props.scan.scan(path,this.state.orgs,this.state.datetime); 
            });
            ipcRenderer.send('scan-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.open_multi_file_dialog((p)=>{
                console.log(p);
                if(!!p) {
                    notification.open({ message: '操作提示', description: '识别路径'+p});
                    this.props.scan.scan(p,this.state.orgs,this.state.datetime);
                }
            });
        }
    }

    render() {
        let years = [];
        let year = moment().format('YYYY');
        for(let y = 2000;y<=parseInt(year);y++){
            years.push(y+'');
        }

        return (
            <Layout style={{ width:'100%',height:'100%' }}>
                <Layout.Header style={{ width:'100%',height:'80px',padding:0,background:'#ffffff' }}>
                    <Top history={ this.props.history }/>
                </Layout.Header>
                <Layout style={{ width:'100%',height:'100%',background:'#fff' }}>
                    <Layout.Sider collapsible theme='light' collapsed={this.props.app.collapsed} onCollapse={()=>{ this.props.app.updateCollapsed() }} style={{ height:'100%' }}>
                        <Left collapsed={this.props.app.collapsed} history={ this.props.history }/>
                    </Layout.Sider>
                    <Layout.Content style={{ width:'100%',height:'100%',overflow:'auto',background:'#f0f8ff',padding:10 }}>
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading}>
                            <div style={{ marginBottom: 16,display: 'flex',flexDirection: 'row',alignItems:'center' }}>

                                <div style={{ flex:1 }}>
                                    <Tree.DirectoryTree checkable={true} onCheck={this.onCheck} defaultExpandAll={true} showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.generate.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i} defaultExpandAll={true} >
                                                    { this.props.generate.orgs.map((o,i)=>{
                                                        if(o.org_type_id==t.id) {
                                                            return (
                                                                <Tree.TreeNode title={ o.short_name } key={"0-0-0-"+i} defaultExpandAll={true} isLeaf/>
                                                            )
                                                        }
                                                    })}
                                                </Tree.TreeNode>
                                            ))}
                                        </Tree.TreeNode>
                                    </Tree.DirectoryTree>
                                </div>

                                <div style={{ flex:4 }}>

                                    <div style={{ width:500,height:40 }}>
                                        提醒：<br/>
                                        &nbsp;&nbsp;&nbsp;&nbsp;在单位信息、领导人员信息以及相关信息录入完毕后，才能生成完整的投票表!
                                    </div>

                                    <div style={{ height:20 }}></div>

                                    <div style={{ width:520,display: 'flex',flexDirection: 'row',alignItems:'center' }}>
                                        <div style={{ width:120 }}>
                                            选择年度
                                        </div>    
                                        <Select defaultValue={this.state.datetime} onChange={this.onChangeDatetime} style={{ flex:1,marginLeft:15,marginRight:15 }}>
                                            { years.map((y,i)=>{
                                                return (
                                                    <Select.Option key={y+''} value={y+''}>
                                                        {y+'年'}
                                                    </Select.Option>
                                                );
                                            }) }
                                        </Select>
                                    </div>

                                    <div style={{ height:20 }}></div>

                                    <div style={{ width:500,display: 'flex',flexDirection: 'row',alignItems:'center',justifyContent:'flex-start' }}>
                                        <div style={{ width:165 }}></div>
                                    
                                        <Button onClick={this.generate} style={{ width:200 }}>
                                            生成投票表
                                        </Button>

                                        <div style={{ width:20 }}></div>
                                        
                                        <Button onClick={ this.onOpen } style={{ width:200 }}>
                                            识别文件
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