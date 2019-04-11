import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Select, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './result_team.css';

@inject('app','resultteam')
@observer
export default class ResultTeam extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    componentWillMount() {
        this.props.resultteam.load();
    }

    onSelect = (selectedKeys, info) => {
        console.log('onSelect',selectedKeys,info);
        let paths = selectedKeys[0].split('-');
        if(paths.length==4) {
            this.props.resultteam.selectOrg(this.props.resultteam.orgs[parseInt(paths[3])]);
        }
        if(paths.length==5) {
            this.props.resultteam.selectYear(this.props.resultteam.years[parseInt(paths[4])]);
        }
    }

    onChange = (entity_id) => {
        let index = this.props.resultteam.entities.findIndex((tmp)=>tmp.id == entity_id);
        let entity = this.props.resultteam.entities[index];
        this.props.resultteam.entity = entity;
        this.props.resultteam.loadResult();
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.resultteam.do_export(path); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.resultteam.do_export(p);
                }
            });
        }
    }

    render() {
        const columns = [
            {
                title: '序号',
                dataIndex: '',
                width:60,
                editable: false,
                align:'center',
                fixed: 'left',
                render: (text, record, index) => {
                    // return ([...this.props.resultteam.result_teams]).findIndex(item => item.org_id==record.org_id&&item.year==record.year&&item.exam_entity_id==record.exam_entity_id) + 1;
                    return index + 1;
                }
            },
            {
                title: '单位',
                dataIndex: 'org.short_name',
                width: 200,
                editable: true,
                fixed: 'left',
            },
            {
                title: '年份',
                dataIndex: 'year',
                width: 100,
                editable: true,
                fixed: 'left',
            },
            {
                title: '测评主体',
                dataIndex: 'exam_entity.name',
                width: 100,
                fixed: 'left',
                editable: true,
            }
        ];

        ([...this.props.resultteam.measures]).map((measure,measure_index)=>{
            if(measure.exam_content.exam_id == 1 && measure.show == 1){
                columns.push({
                    title: measure.name,
                    dataIndex: '',
                    width: 100,
                    editable: true,
                    align:'right',
                    render:(text, record, index) => {
                        let measure_id = this.props.resultteam.measures.find((item)=>item.name==measure.name).id;
                        if(!!record.score&&!!record.score[measure_id]) {
                            return record.score[measure_id].score;
                        } else {
                            return 10;
                        }
                    }
                });
            }
        });

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
                                    <Tree.DirectoryTree onSelect={this.onSelect} defaultExpandAll showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.resultteam.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i}>
                                                    { this.props.resultteam.orgs.map((o,i)=>{
                                                        if(o.org_type_id==t.id) {
                                                            return (
                                                                <Tree.TreeNode title={ o.short_name } key={"0-0-0-"+i} defaultExpandAll={true}>
                                                                    { (this.props.resultteam.years||[]).map((m,i)=>{
                                                                        if(this.props.resultteam.org.id ==o.id) {
                                                                            return (
                                                                                <Tree.TreeNode title={ m } key={"0-0-0-0-"+i} defaultExpandAll={true} isLeaf/>
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
                                <div className="list" style={{ width:'100%',overflow: 'auto' }}>
                                    <div style={{ marginBottom: 16,display: 'flex',flexDirection: 'row' }}>
                                        <Select value={(this.props.resultteam.entity||{}).id} onChange={this.onChange} style={{ width:120,marginLeft:15,marginRight:15 }}>
                                        { this.props.resultteam.entities.map((y,i)=>{
                                            return (
                                                <Select.Option key={ y.id } value={ y.id }>
                                                    {y.name}
                                                </Select.Option>
                                            );
                                        }) }
                                        </Select>
                                        <div style={{ width:15 }}></div>
                                        <Button
                                            onClick={this.do_export}
                                        >
                                            导出
                                        </Button>
                                    </div>
                                    <Table
                                        rowKey="image_path"
                                        dataSource={ [...this.props.resultteam.result_teams] }
                                        columns={columns}
                                        style={{ width:1500 }}
                                    />
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