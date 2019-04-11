import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Select, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './result_manager.css';

@inject('app','resultmanager')
@observer
export default class ResultManager extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            treeData:[
                { title: '中交上航局', key: '0' }
            ]
        }
    }

    componentWillMount() {
        this.props.resultmanager.load();
    }

    onSelect = (selectedKeys, info) => {
        let paths = selectedKeys[0].split('-');
        if(paths.length==4) {
            let org_type_id = paths[1];
            let org_id = paths[2];
            let year = paths[3];
            this.props.resultmanager.year = year;
            let org_index = this.props.resultmanager.orgs.findIndex((tmp)=>tmp.id == org_id);
            let org = this.props.resultmanager.orgs[org_index];
            this.props.resultmanager.selectOrg(org);
        }
    }

    onChangeEntity = (entity_id) => {
        let index = this.props.resultmanager.entities.findIndex((tmp)=>tmp.id == entity_id);
        let entity = this.props.resultmanager.entities[index];
        this.props.resultmanager.entity = entity;
        this.props.resultmanager.loadResult();
    }

    onChangeManager = (manager_ids) => {
        this.props.resultmanager.manager = [];
        if(!!!manager_ids||manager_ids.length==0){
            this.props.resultmanager.clearManager();
        } else {
            manager_ids.map((manager_id)=>{
                let index = this.props.resultmanager.managers.findIndex((tmp)=>tmp.id == manager_id);
                let manager = this.props.resultmanager.managers[index];
                this.props.resultmanager.selectManager(manager);
            });
        }
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.resultmanager.do_export(path); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.resultmanager.do_export(p);
                }
            });
        }
    }

    renderTreeNodes = (data) => {
        return data.map((item) => {
            if (item.children) {
                return (
                    <Tree.TreeNode title={item.title} key={item.key} dataRef={item}>
                        {this.renderTreeNodes(item.children)}
                    </Tree.TreeNode>
                );
            }
            return <Tree.TreeNode {...item} dataRef={item} />;
        });
    }

    onLoadData = (treeNode) => {
        return new Promise((resolve) => {
            if (treeNode.props.children) {
                resolve();
                return;
            }
            setTimeout(() => {
                let keypath = treeNode.props.eventKey.split('-');
                treeNode.props.dataRef.children = [];
                if(keypath.length==1) {
                    this.props.resultmanager.orgtypes.map((ot,index)=>{
                        treeNode.props.dataRef.children.push({
                            title: ot.name,
                            key: `${treeNode.props.eventKey}-${ot.id}`
                        });
                    });
                } else if(keypath.length==2) {
                    let orgtype = keypath[keypath.length-1];
                    this.props.resultmanager.orgs.map((org,index)=>{
                        if(org.org_type_id==orgtype) {
                            treeNode.props.dataRef.children.push({
                                title: org.short_name,
                                key: `${treeNode.props.eventKey}-${org.id}`
                            });
                        }
                    });
                } else if(keypath.length==3) {
                    let org = keypath[keypath.length-1];
                    if(!!this.props.resultmanager.allyears&&this.props.resultmanager.allyears.length>0) {
                        this.props.resultmanager.allyears.map((year,index)=>{
                            treeNode.props.dataRef.children.push({
                                title: year,
                                key: `${treeNode.props.eventKey}-${year}`,
                                isLeaf: true
                            });
                        });
                    }
                }
                this.setState({
                    treeData: [...this.state.treeData],
                });
                resolve();
            });
        });
      }

    render() {
        const columns = [
            {
                title: '序号',
                dataIndex: '',
                width: '5%',
                editable: false,
                align:'center',
                render: (text, record, index) => {
                    // return ([...this.props.resultmanager.result_managers]).findIndex(item => item.managar_id==record.managar_id&&item.year==record.year&&item.exam_entity_id==record.exam_entity_id) + 1;
                    return index + 1;
                }
            },
            {
                title: '单位',
                dataIndex: 'manager.org.short_name',
                width: '12%',
                editable: true,
            },
            {
                title: '年份',
                dataIndex: 'year',
                width: '5%',
                editable: true,
            },
            {
                title: '姓名',
                dataIndex: 'manager.name',
                width: '7%',
                editable: true,
            },
            {
                title: '测评主体',
                dataIndex: 'exam_entity.name',
                width: '6%',
                editable: true,
            },
            {
                title: '政治素质',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='政治素质').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '职业素养',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='职业素养').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '廉洁自律',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='廉洁自律').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '决策能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='决策能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '执行能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='执行能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '领导能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='领导能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '学习能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='学习能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '创新能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='创新能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '沟通能力',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='沟通能力').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '内控管理',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='内控管理').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
            {
                title: '履职绩效',
                dataIndex: '',
                width: '5.5%',
                editable: true,
                align:'right',
                render:(text, record, index) => {
                    let measure_id = this.props.resultmanager.measures.find((item)=>item.name=='履职绩效').id;
                    if(!!record.score&&!!record.score[measure_id]) {
                        return record.score[measure_id].score;
                    } else {
                        return 10;
                    }
                }
            },
        ];

        let selectedManager = [];
        [...this.props.resultmanager.manager].map((m)=>{
            selectedManager.push(m.id);
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
                        <Spin tip={this.props.app.tip} spinning={this.props.app.loading||this.props.resultmanager.result_loading}>
                            <div className="split">
                                <div className="tree">
                                    <Tree loadData={this.onLoadData} onSelect={this.onSelect}>
                                        { this.renderTreeNodes(this.state.treeData) }
                                    </Tree>
                                </div>
                                <div className="line"></div>
                                <div className="list" style={{ width:'100%',overflow: 'auto' }}>
                                    <div style={{ marginBottom:16,display:'flex',flexDirection:'row',alignItems:'center' }}>
                                        <span>姓名:</span>
                                        <Select mode="multiple" defaultValue={selectedManager} onChange={this.onChangeManager} style={{ width:120,marginLeft:15,marginRight:15 }}>
                                        { this.props.resultmanager.managers.map((m,i)=>{
                                            return (
                                                <Select.Option key={ m.id } value={ m.id }>
                                                    {m.name}
                                                </Select.Option>
                                            );
                                        }) }
                                        </Select>
                                        <div style={{ width:15 }}></div>
                                        <span>测评主体:</span>
                                        <Select value={(this.props.resultmanager.entity||{}).id} onChange={this.onChangeEntity} style={{ width:120,marginLeft:15,marginRight:15 }}>
                                        { this.props.resultmanager.entities.map((y,i)=>{
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
                                        rowKey="row_key"
                                        dataSource={ [...this.props.resultmanager.result_managers] }
                                        columns={columns}
                                        style={{ width:1600 }}
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