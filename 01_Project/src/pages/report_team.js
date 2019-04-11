import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, Select, Search, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import './report_team.css';

import moment from 'moment';
import Foot from '../components/foot';

@inject('app','report')
@observer
export default class ReportTeam extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            datetime:moment().format('YYYY'),
            org:null,
            keyword:null,
            loading:true
        }
    }

    componentWillMount() {
        this.props.report.loadTree();
        this.props.report.loadExamTeams(this.state.datetime);
    }

    componentWillReact() {

    }

    onChangeDatetime = (value) => {
        console.log(value);
        this.setState({ datetime: value+'' });
        this.props.report.loadExamTeams(value);
    }

    onChangeOrg = (value) => {
        console.log(value);
        this.setState({ org: value });
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.report.doExportTeam(path,this.state.datetime); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.report.doExportTeam(p,this.state.datetime);
                }
            });
        }
    }

    render() {
        console.log(this.props);
        const columns = [{
            title: '序号',
            dataIndex: 'org_index',
            width: '1.5%',
            align:'center',
            // render: (text, record, index) => {
            //     return index + 1;
            // }
        }, {
            title: '单位',
            dataIndex: 'org_name',
            width: '4.5%'
        }, {
            title: '汇总得分',
            dataIndex: 'org_sum_score',
            width: '2%',
            align:'right',
        }, {
            title: '排名',
            dataIndex: 'org_sum_sort',
            width: '2%',
            align:'right',
        }, {
            title: '企业党建',
            dataIndex: 'dj_score',
            width: '2%',
            align:'right',
        }, {
            title: '班子业绩',
            dataIndex: 'yj_score',
            width: '2%',
            align:'right',
        }, {
            title: '民主测评',
            dataIndex: 'org_score',
            width: '2%',
            align:'right',
        }];

        ([...this.props.report.contents_1]).map((content,content_index)=>{
            if(content.exam_id == 1 && content.show == 1){
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

                ([...this.props.report.measures_1]).map((measure,measure_index)=>{
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

                columns.push(content_column);
            }
        });

        let years = [];
        let year = moment().format('YYYY');
        for(let y = 2000;y<=parseInt(year);y++){
            years.push(y+'');
        }

        let datas = [...this.props.report.exam_teams];
        let dataSource = [];
        if(!!this.state.org&&this.state.org!=0) {
            for(let d=0;d<datas.length;d++){
                if(!!datas[d]&&(datas[d])['org_id']==this.state.org) {
                    dataSource.push(datas[d]);
                }
            }
        } else if(!!this.state.keyword) {
            for(let d=0;d<datas.length;d++){
                if(!!datas[d]&&(datas[d])['org_name'].indexOf(this.state.keyword)>-1) {
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
                            <div style={{ width:800,display: 'flex',flexDirection: 'row',alignItems:'center' }}>
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
                                    选择单位
                                </div>    
                                {/* <Select defaultValue={this.state.org} onChange={this.onChangeOrg} style={{ flex:3,marginLeft:15,marginRight:15 }}>
                                    <Select.Option key={0} value={0}>&nbsp;</Select.Option>
                                    { this.props.report.orgs.map((y,i)=>{
                                        return (
                                            <Select.Option key={y.id} value={y.id}>
                                                {y.short_name}
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
                                title={() => <span>司属单位领导班子{this.state.datetime}年度综合考核评价汇总表</span>}
                                rowKey="org_id"
                                columns={columns} 
                                dataSource={ dataSource } 
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