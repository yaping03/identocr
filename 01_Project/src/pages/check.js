import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, List, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, notification } from 'antd';

import moment from 'moment';
import Foot from '../components/foot';

import Top from '../components/top';
import Left from '../components/left';

import './check.css';

@inject('app','check')
@observer
export default class Check extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            datetime:moment().format('YYYY'),
            orgs:[]
        }
    }

    componentWillMount() {
        this.props.check.load();
    }

    onCheckOrg = (checkedKeys, info) => {
        let orgs = [];
        checkedKeys.filter((item)=>{
            for(let i=0;i<this.props.check.orgs.length;i++){
                if(('0-0-0-'+i)==item) {
                    orgs.push(this.props.check.orgs[i].id);
                }
            }
        });
        this.setState({ orgs });
    }

    onCheck = () => {
        if(!!!this.state.orgs || this.state.orgs.length==0) {
            notification.open({ message: '操作提示', description: '请选择单位' });
            return;
        }
        if(this.state.orgs.length>1) {
            notification.open({ message: '操作提示', description: '只能选择一个单位进行完整性验证' });
            return;
        }

        this.props.check.check(this.state.datetime,this.state.orgs);
    }

    onCompute = () => {
        if(!!!this.state.orgs || this.state.orgs.length==0) {
            notification.open({ message: '操作提示', description: '请选择单位' });
            return;
        }
        if(this.state.orgs.length>1) {
            notification.open({ message: '操作提示', description: '只能选择一个单位进行考评计算' });
            return;
        }

        this.props.check.compute(this.state.datetime,this.state.orgs);
    }

    onChangeDatetime = (value) => {
        this.setState({ datetime: value+'' });
    }

    render() {
        console.log(this.props);

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
                    <Layout.Content style={{ width:'100%',height:'100%',overflow: 'auto',background:'#f0f8ff',padding:10 }}>
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading}>
                            <div style={{ marginBottom: 16,display: 'flex',flexDirection: 'row',alignItems:'center' }}>
                            
                                <div style={{ flex:1 }}>
                                    <Tree.DirectoryTree checkable={true} onCheck={this.onCheckOrg} defaultExpandAll={true} showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.check.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i} defaultExpandAll={true} >
                                                    { this.props.check.orgs.map((o,i)=>{
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
                                
                                    <div style={{ paddingLeft:30,paddingRight:30,display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center' }}>

                                        <div style={{ width:'100%',height:10 }}></div>
                                        
                                        <div style={{ width:'100%',display:'flex',flexDirection:'row',justifyContent:'center',alignItems:'flex-start' }}>

                                            <div style={{ width:200 }}>
                                                <Select defaultValue={this.state.datetime} onChange={this.onChangeDatetime} style={{ width:'100%',marginLeft:15,marginRight:15 }}>
                                                    { years.map((y,i)=>{
                                                        return (
                                                            <Select.Option key={y+''} value={y+''}>
                                                                {y+'年'}
                                                            </Select.Option>
                                                        );
                                                    }) }
                                                </Select>
                                            </div>

                                            <div style={{ width:30 }}></div>

                                            <div style={{ width:200 }}>
                                                <Button style={{ width:'100%' }} onClick={ this.onCheck }>
                                                    检查数据完整性
                                                </Button>
                                                <div style={{ width:'100%',height:10 }}></div>
                                                <Button style={{ width:'100%' }} onClick={ this.onCompute }>
                                                    考评计算
                                                </Button>
                                            </div>

                                            <div style={{ flex:1 }}></div>

                                        </div>
                                        
                                        { [...this.props.check.messages].length>0 &&
                                        <List
                                            size="small"
                                            style={{ width:'100%' }}
                                            bordered
                                            dataSource={[...this.props.check.messages]}
                                            renderItem={item => (<List.Item>{item}</List.Item>)}
                                        />
                                        }
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