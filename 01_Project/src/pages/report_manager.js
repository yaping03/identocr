import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, AutoComplete, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import './report_manager.css';

import moment from 'moment';
import Foot from '../components/foot';

@inject('app','report')
@observer
export default class ReportManager extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            datetime:moment().format('YYYY'),
            manager:null,
            keyword:null,
            loading:true
        }
    }

    componentWillMount() {
        this.props.report.loadTree();
        this.props.report.loadExamManagers(this.state.datetime);
    }

    componentWillReact() {
    }

    onChangeDatetime = (value) => {
        console.log(value);
        this.setState({ datetime: value+'' });
        this.props.report.loadExamManagers(value);
    }

    onChangeManager = (value) => {
        console.log(value);
        this.setState({ manager: value });
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.report.doExportManager(path,this.state.datetime); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.report.doExportManager(p,this.state.datetime);
                }
            });
        }
    }

    render() {
        console.log(this.props);
        const columns = [{
            title: '序号',
            dataIndex: 'manager_index',
            width: '1.5%',
            align:'center',
            // render: (text, record, index) => {
            //     return index + 1;
            // }
        }, {
            title: '单位',
            dataIndex: 'org_name',
            width: '4%'
        }, {
            title: '姓名',
            dataIndex: 'manager_name',
            width: '3%'
        }, {
            title: '职务',
            dataIndex: 'title',
            width: '4%'
        }, {
            title: '汇总得分',
            children: [{
                title: '得分',
                dataIndex: 'manager_sum_score',
                width: '3%',
                align:'right',
            }, {
                title: '排名',
                dataIndex: 'manager_sum_sort',
                width: '2%',
                align:'right',
            }]
        }, {
            title: '部门业绩得分',
            dataIndex: 'org_score',
            width: '3%',
            align:'right'
        }];
        
        let mzcp_column = {
            title: '民主测评',
            children: [{
                title: '合计',
                dataIndex: 'manager_score',
                width: '3%',
                align:'right'
            }]
        };

        ([...this.props.report.contents_2]).map((content,content_index)=>{
            if(content.exam_id == 2 && content.show == 1){
                let content_column = {
                    title: content.content,
                    children: []
                };

                content_column.children.push({
                    title: '小计',
                    dataIndex: 'content_score_'+content.id,
                    width: '2%',
                    align:'right',
                });

                ([...this.props.report.measures_2]).map((measure,measure_index)=>{
                    if(measure.exam_content_id == content.id && measure.show == 1){
                        content_column.children.push({
                            key:'measure_score_'+measure.id,
                            title: measure.name,
                            dataIndex: 'measure_score_'+measure.id,
                            width: '2%',
                            align:'right',
                        });
                    }
                });

                mzcp_column.children.push(content_column);
            }
        });
        
        columns.push(mzcp_column);

        let years = [];
        let year = moment().format('YYYY');
        for(let y = 2000;y<=parseInt(year);y++){
            years.push(y+'');
        }

        let datas = [...this.props.report.exam_managers];
        let dataSource = [];
        if(!!this.state.manager&&this.state.manager!=0) {
            for(let d=0;d<datas.length;d++){
                if(!!datas[d]&&(datas[d])['manager_id']==this.state.manager) {
                    dataSource.push(datas[d]);
                }
            }
        } else if(!!this.state.keyword) {
            for(let d=0;d<datas.length;d++){
                if(!!datas[d]&&(datas[d])['manager_name'].indexOf(this.state.keyword)>-1) {
                    dataSource.push(datas[d]);
                }
            }
        } else {
            dataSource = datas;
        }

        let last = moment();

        if(dataSource.length>0&&this.state.loading==true) {
            setTimeout(()=>{
                this.setState({loading:false});
            });
        } else if(this.state.loading==true) {
            setTimeout(()=>{
                if(moment().diff(last, 'seconds')>4) {
                    this.setState({loading:false});
                }
            },5000);
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
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading||this.state.loading}>
                            <div className="list" style={{ width:'100%',overflowX:'auto' }}>
                                <div style={{ width:600,display: 'flex',flexDirection: 'row',alignItems:'center' }}>
                                    <div style={{ width:80 }}>
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
                                    <div style={{ width:30 }}></div>
                                    <div style={{ width:80 }}>
                                        选择干部
                                    </div>    
                                    {/* <Select defaultValue={this.state.manager} onChange={this.onChangeManager} style={{ flex:3,marginLeft:15,marginRight:15 }}>
                                        <Select.Option key={0} value={0}>&nbsp;</Select.Option>
                                        { this.props.report.managers.map((y,i)=>{
                                            return (
                                                <Select.Option key={y.id} value={y.id}>
                                                    {y.name}
                                                </Select.Option>
                                            );
                                        }) }
                                    </Select> */}
                                    <Input.Search
                                        placeholder=""
                                        enterButton="搜索"
                                        size="default"
                                        onSearch={ value => {
                                            this.setState({ keyword:value });
                                        }}
                                        style={{ flex:3,marginLeft:15,marginRight:15 }}
                                    />
                                    <div style={{ width:15 }}></div>
                                    <Button
                                        onClick={this.do_export}
                                    >
                                        导出
                                    </Button>
                                </div>
                                <Table 
                                    title={() => <span>{this.state.datetime}年度机关部门中层领导干部综合考核评价汇总表</span>}
                                    rowKey="manager_id"
                                    columns={columns}
                                    dataSource={ dataSource }
                                    bordered
                                    style={{ width: 1700 }}
                                />
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