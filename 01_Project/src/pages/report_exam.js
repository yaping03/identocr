import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, notification } from 'antd';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

import { scalePow, scaleLog } from 'd3-scale';

import Top from '../components/top';
import Left from '../components/left';

import './report_exam.css';

import moment from 'moment';
import Foot from '../components/foot';

@inject('app','report')
@observer
export default class ReportExam extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected_org : null,
            selected_manager : null,
            charts_type : null,
            start_year: parseInt(moment().format('YYYY'))-2,
            end_year: parseInt(moment().format('YYYY'))
        }
    }

    componentWillMount() {
        this.props.report.loadTree();
    }

    onSelect = (selectedKeys, info) => {
        let paths = selectedKeys[0].split('-');
        if(paths.length==4) {
            let selected_org = this.props.report.orgs[parseInt(paths[3])];
            this.setState({ charts_type:1,selected_org:selected_org });
            this.props.report.charts = [];
        }
        if(paths.length==5) {
            let selected_manager = this.props.report.managers[parseInt(paths[4])];
            this.setState({ charts_type:2,selected_manager:selected_manager });
            this.props.report.charts = [];
        }
    }

    onChangeStartDatetime = (value) => {
        this.setState({ start_year: value+'' });
    }

    onChangeEndDatetime = (value) => {
        this.setState({ end_year: value+'' });
    }

    onClickChart = () => {
        if(this.state.charts_type==1) {
            this.props.report.loadOrgChart(this.state.selected_org,this.state.start_year,this.state.end_year);
        } else if(this.state.charts_type==2) {
            this.props.report.loadManagerChart(this.state.selected_manager,this.state.start_year,this.state.end_year);
        }
    }

    render() {
        console.log(this.props);

        let years = [];
        let year = moment().format('YYYY');
        for(let y = 2000;y<=parseInt(year);y++){
            years.push(y+'');
        }

        console.log('=====',this.state,(!!this.state.selected_org||!!this.state.selected_manager)&&!!this.state.start_year&&!!this.state.end_year);

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
                            <div className="split">
                                <div className="tree">
                                    <Tree.DirectoryTree onSelect={this.onSelect} defaultExpandAll={true} showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.report.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i} defaultExpandAll={true} >
                                                    { this.props.report.orgs.map((o,i)=>{
                                                        if(o.org_type_id==t.id) {
                                                            return (
                                                                <Tree.TreeNode title={ o.short_name } key={"0-0-0-"+i} defaultExpandAll={true}>
                                                                    { this.props.report.managers.map((m,i)=>{
                                                                        if(m.org_id==o.id) {
                                                                            return (
                                                                                <Tree.TreeNode title={ m.name } key={"0-0-0-0-"+i} defaultExpandAll={true} isLeaf/>
                                                                            )
                                                                        }
                                                                    })}
                                                                </Tree.TreeNode>
                                                            )
                                                        }
                                                    })}
                                                </Tree.TreeNode>
                                            ))}
                                        </Tree.TreeNode>
                                    </Tree.DirectoryTree>
                                </div>
                                <div className="line"></div>
                                <div style={{ flex:3,flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                                    <div style={{ width:'100%',display: 'flex',flexDirection: 'row',alignItems:'center',paddingLeft:80 }}>
                                        <span>年份</span>
                                        <Select defaultValue={this.state.start_year} onChange={this.onChangeStartDatetime} style={{ width:150,marginLeft:15,marginRight:15 }}>
                                            { years.map((y,i)=>{
                                                return (
                                                    <Select.Option key={y+''} value={y+''}>
                                                        {y+'年'}
                                                    </Select.Option>
                                                );
                                            }) }
                                        </Select>
                                        <span>-</span>
                                        <Select defaultValue={this.state.end_year} onChange={this.onChangeEndDatetime} style={{ width:150,marginLeft:15,marginRight:15 }}>
                                            { years.map((y,i)=>{
                                                return (
                                                    <Select.Option key={y+''} value={y+''}>
                                                        {y+'年'}
                                                    </Select.Option>
                                                );
                                            }) }
                                        </Select>
                                        <Button
                                            onClick={this.onClickChart}
                                        >
                                            生成图表
                                        </Button>
                                    </div>
                                    <div style={{ width:'100%',display: 'flex',flexDirection: 'row',alignItems:'center',paddingLeft:80,paddingTop:15,paddingBottom:15 }}>
                                        { ((!!this.state.selected_org||!!this.state.selected_manager)&&!!this.state.start_year&&!!this.state.end_year) &&
                                            <span style={{ fontSize:24 }}>{this.state.start_year} - {this.state.end_year} { this.state.charts_type==1?(this.state.selected_org||{}).short_name:(this.state.selected_manager||{}).name } 得分趋势图 </span>
                                        }
                                    </div>
                                    <BarChart width={800} height={600} data={ [...this.props.report.charts] } margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                                        <CartesianGrid strokeDasharray="3 3"/>
                                        <XAxis dataKey="year"/>
                                        <YAxis/>
                                        <Tooltip/>
                                        {/* <Legend /> */}
                                        { !!this.state.charts_type&&this.state.charts_type==1 &&
                                        <Bar dataKey="org_sum_score" fill="#82ca9d" />
                                        }
                                        { !!this.state.charts_type&&this.state.charts_type==2 &&
                                        <Bar dataKey="manager_sum_score" fill="#82ca9d" />
                                        }
                                    </BarChart>
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