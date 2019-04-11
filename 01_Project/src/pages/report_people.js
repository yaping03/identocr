import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import './report_people.css';

import moment from 'moment';
import Foot from '../components/foot';

@inject('app','report')
@observer
export default class ReportPeople extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            datetime:moment().format('YYYY')
        }
    }

    componentWillMount() {
        this.props.report.loadTree();
        this.props.report.loadExamManagers(this.state.datetime);
    }

    onChangeDatetime = (value) => {
        this.setState({ datetime: value+'' });
        this.props.report.loadExamManagers(this.state.datetime);
    }

    render() {
        console.log(this.props);

        const columns = [{
            title: '序号',
            dataIndex: '',
            width: '2%',
            align:'center',
            render: (text, record, index) => {
                return index + 1;
            }
        }, {
            title: '单位',
            dataIndex: 'org_name',
            width: '10%'
        }, {
            title: '姓名',
            dataIndex: 'manager_name',
            width: '2%'
        }, {
            title: '职务',
            dataIndex: 'title',
            width: '2%'
        }, {
            title: '汇总得分',
            children: [{
                title: '得分',
                dataIndex: 'manager_score',
                width: '2%'
            }, {
                title: '排名',
                dataIndex: 'manager_sort',
                width: '2%'
            }]
        }];

        ([...this.props.report.contents_2]).map((content,content_index)=>{
            if(content.exam_id == 2 && content.show == 1){
                let content_column = {
                    title: content.content,
                    children: []
                };

                content_column.children.push({
                    title: '小计',
                    dataIndex: 'content_score_'+content.id,
                    width: '2%'
                });

                ([...this.props.report.measures_2]).map((measure,measure_index)=>{
                    if(measure.exam_content_id == content.id && measure.show == 1){
                        content_column.children.push({
                            key:'measure_score_'+measure.id,
                            title: measure.name,
                            dataIndex: 'measure_score_'+measure.id,
                            width: '2%'
                        });
                    }
                });

                columns[columns.length-1].children.push(content_column);
            }
        });

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
                            <div style={{ width:'100%',display: 'flex',flexDirection: 'row',alignItems:'center' }}>
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
                            <Table 
                                title={() => <span>{this.state.datetime}年度机关部门中层领导干部综合考核评价汇总表</span>}
                                rowKey="id"
                                columns={columns} 
                                dataSource={ [...this.props.report.exam_managers] } 
                                bordered
                                style={{ width:1500 }}
                            />
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