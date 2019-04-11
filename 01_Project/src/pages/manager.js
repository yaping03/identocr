import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, Select, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './manager.css';

const FormItem = Form.Item;
const EditableContext = React.createContext();

const EditableRow = ({ form, index, ...props }) => (
    <EditableContext.Provider value={form}>
        <tr {...props} />
    </EditableContext.Provider>
);

const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends React.Component {
    render() {
        const {
            editing,
            dataIndex,
            title,
            inputType,
            record,
            index,
            ...restProps
        } = this.props;
        return (
            <EditableContext.Consumer>
            {(form) => {
                const { getFieldDecorator } = form;
                return (
                <td {...restProps}>
                    {editing ? (
                    <FormItem style={{ margin: 0 }}>
                        {
                            getFieldDecorator(dataIndex, {
                                rules: [{
                                    required: true,
                                    message: `请输入 ${title}!`,
                                }],
                                initialValue: record[dataIndex],
                            })(
                                (() => {
                                    if (this.props.inputType === 'number') {
                                        if(this.props.dataIndex=='weight') {
                                            return <InputNumber min={0} max={100} formatter={value => `${value}%`} parser={value => value.replace('%', '')} />;
                                        }
                                        if(this.props.dataIndex=='sort') {
                                            return <InputNumber min={1} />;
                                        }
                                        return <InputNumber />;
                                    }
                                    if (this.props.inputType === 'select') {
                                        return (
                                            <Select placeholder="请选择">
                                                { [...(this.props.optiondatas||[])].map((c,i)=>{
                                                    return (
                                                        <Select.Option key={c.id} value={c.id}>
                                                            {this.props.dataIndex=='org_id'?c.short_name:c.name}
                                                        </Select.Option>
                                                    );
                                                }) }
                                            </Select>
                                        )
                                    }
                                    return <Input />;
                                }).call(this)
                            )
                        }
                    </FormItem>
                    ) : restProps.children}
                </td>
                );
            }}
            </EditableContext.Consumer>
        );
    }
}

@inject('app','manager')
@observer
export default class Manager extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editingKey:'',
            selected:[]
        }
    }

    componentWillReact() {
        if(this.props.manager.view == "added" && !!this.props.manager.weights && this.props.manager.weights.length > 0) {
            console.log('++++++',this.props.manager);
            this.props.manager.view = 'list';
            this.setState({ editingKey:this.props.manager.weights[this.props.manager.weights.length-1].id });
            console.log('/*/*/*/*/',this.props.manager.weights,this.props.manager.weights.length);
        }
    }

    componentWillMount() {
        this.props.manager.load();
    }

    onSelect = (selectedKeys, info) => {
        console.log('onSelect',selectedKeys,info);
        let paths = selectedKeys[0].split('-');
        if(paths.length==2) {
            // this.props.manager.selectAll();
            // this.props.manager.view = '';
        }
        if(paths.length==3) {
            // this.props.manager.selectOrgType(this.props.manager.orgtypes[parseInt(paths[2])]);
            // this.props.manager.view = '';
        }
        if(paths.length==4) {
            this.props.manager.view = 'list';
            this.props.manager.selectOrg(this.props.manager.orgs[parseInt(paths[3])]);
        }
        if(paths.length==5) {
            this.props.manager.view = 'list';
            this.props.manager.selectManager(this.props.manager.managers[parseInt(paths[4])]);
        }
    }

    isEditing = (record) => {
        return record.id === this.state.editingKey;
    };

    edit(id) {
        this.setState({ editingKey: id });
    }

    save(form, id) {
        form.validateFields((error, row) => {
            if (error) {
                return;
            }
            if(this.props.manager.model=="manager") {
                const newData = [...this.props.manager.managers];
                const index = newData.findIndex(item => id === item.id);
                if (index > -1) {
                    const item = newData[index];
                    if(item.id===0) {
                        this.props.manager.save({...item,...row});
                    } else {
                        this.props.manager.update(item.id,{...item,...row});
                    }
                    this.setState({ editingKey: '' });
                } else {
                    this.setState({ editingKey: '' });
                }
            } else {
                const newData = [...this.props.manager.weights];
                const index = newData.findIndex(item => id === item.id);
                if (index > -1) {
                    const item = newData[index];

                    let sum = 0;
                    newData.map((item,index)=>{
                        if(id === item.id){
                            sum += parseFloat(row.weight);
                        } else {
                            sum += parseFloat(item.weight);
                        }
                    });
                    if(sum!=100) {
                        notification.open({ message: '操作提示', description: '权重之和('+sum+'%)不为100%' });
                    }

                    if(item.id===0) {
                        this.props.manager.save({...item,...row});
                    } else {
                        this.props.manager.update(item.id,{...item,...row});
                    }
                    this.setState({ editingKey: '' });
                } else {
                    this.setState({ editingKey: '' });
                }
            }
        });
    }

    cancel = () => {
        this.props.manager.cancel();
        this.setState({ editingKey: '' });
    };

    add = () => {
        if (this.props.manager.model=="manager") {
            if(!!this.props.manager.org) {
                let hasNew = (this.props.manager.managers.findIndex(item => item.id === 0)>-1);
                if(!hasNew) {
                    this.props.manager.add();
                    this.setState({ editingKey: 0 });
                } else {
                    notification.open({ message: '操作提示', description: '请先保存' });
                }
            } else {
                notification.open({ message: '操作提示', description: '请先选择单位' });
            }
        } else {
            if(!!this.props.manager.manager) {
                let hasNew = (this.props.manager.weights.findIndex(item => item.id === 0)>-1);
                if(!hasNew) {
                    this.props.manager.add();
                    this.setState({ editingKey: 0 });
                } else {
                    notification.open({ message: '操作提示', description: '请先保存' });
                }
            } else {
                notification.open({ message: '操作提示', description: '请先选择中层干部' });
            }
        }
    }

    del = () => {
        let ids = []
        this.state.selected.filter((item)=>ids.push(item.id));
        if(ids.length>0) {
            this.props.manager.delete(ids);
        }
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.manager.do_export(path); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.manager.do_export(p);
                }
            });
        }
    }

    do_import = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('import-selected-directory', (event, path) => {
                this.props.manager.do_import(path); 
            });
            ipcRenderer.send('import-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.open_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '导入路径'+p});
                    this.props.manager.do_import(p);
                }
            });
        }
    }

    render() {

        console.log(this.props.manager);

        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            },
        };

        const managerColumns = [
            {
                title: '序号',
                dataIndex: '',
                width: '8%',
                editable: false,
                align:'center',
                render: (text, record, index) => {
                    return ([...this.props.manager.managers]).findIndex(item => record.id==item.id) + 1;
                }
            },
            {
                title: '所属单位',
                dataIndex: 'org_id',
                width: '25%',
                inputType: 'select',
                editable: true,
                optionDatas: [...this.props.manager.orgs],
                render: (text, record, index) => {
                    return (record.org||{}).short_name;
                }
            },
            {
                title: '姓名',
                dataIndex: 'name',
                width: '20%',
                inputType: 'text',
                editable: true,
            },
            {
                title: '人员类型',
                dataIndex: 'manager_type_id',
                width: '15%',
                inputType: 'select',
                editable: true,
                optionDatas: [...this.props.manager.managertypes],
                render: (text, record, index) => {
                    return (record.manager_type||{}).name;
                }
            },
            {
                title: '职务',
                dataIndex: 'title',
                width: '15%',
                inputType: 'text',
                editable: true,
                // optionDatas: [...this.props.manager.managertitles],
                // render: (text, record, index) => {
                //     return (record.manager_title||{}).name;
                // }
            },
            {
                title: '排序',
                dataIndex: 'sort',
                width: '15%',
                inputType: 'text',
                editable: true,
                // optionDatas: [...this.props.manager.managertitles],
                // render: (text, record, index) => {
                //     return (record.manager_title||{}).name;
                // }
            },
            {
                title: '',
                dataIndex: '',
                align:'center',
                render: (text, record) => {
                    const editable = this.isEditing(record);
                    return (
                    <div>
                        {editable ? (
                        <span>
                            <EditableContext.Consumer>
                            {form => (
                                <a
                                    href="javascript:;"
                                    onClick={() => this.save(form, record.id)}
                                    style={{ marginRight: 8 }}
                                >
                                保存
                                </a>
                            )}
                            </EditableContext.Consumer>
                            <a
                                href="javascript:;"
                                onClick={() => this.cancel(record.id)}
                                style={{ marginRight: 8 }}
                            >
                            取消
                            </a>
                        </span>
                        ) : (
                        <a onClick={() => this.edit(record.id)}>修改</a>
                        )}
                    </div>
                    );
                },
            },
        ];

        const mcolumns = managerColumns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => (
                    {
                        record,
                        inputType: col.inputType,
                        dataIndex: col.dataIndex,
                        title: col.title,
                        editing: this.isEditing(record),
                        optiondatas: col.optionDatas
                    }
                ),
            };
        });

        const weightsColumns = [
            {
                title: '序号',
                dataIndex: '',
                width: '8%',
                editable: false,
                align:'center',
                render: (text, record, index) => {
                    return ([...this.props.manager.weights]).findIndex(item => record.id===item.id) + 1;
                }
            },
            {
                title: '所属单位',
                dataIndex: '',
                width: '20%',
                inputType: 'text',
                editable: false,
                render: (text, record, index) => {
                    return ((record.manager||{}).org||{}).short_name;
                }
            },
            {
                title: '姓名',
                dataIndex: '',
                width: '13%',
                editable: false,
                inputType: 'text',
                render: (text, record, index) => {
                    return (record.manager||{}).name;
                }
            },
            {
                title: '人员类型',
                dataIndex: 'manager_id',
                width: '10%',
                editable: false,
                inputType: 'text',
                render:(text, record, index) => {
                    return ((record.manager||{}).manager_type||{}).name;
                }
            },
            {
                title: '职务',
                dataIndex: 'title',
                width: '13%',
                editable: false,
                inputType: 'text',
                render:(text, record, index) => {
                    return (record.manager||{}).title;
                }
            },
            {
                title: '年份',
                dataIndex: 'year',
                width: '12%',
                editable: false,
                inputType: 'number'
            },
            {
                title: '权重',
                dataIndex: 'weight',
                width: '12%',
                editable: true,
                inputType: 'number',
                render: (text, record, index) => {
                    return `${text}%`;
                }
            },
            {
                title: '',
                dataIndex: '',
                align:'center',
                render: (text, record) => {
                    const editable = this.isEditing(record);
                    return (
                    <div>
                        {editable ? (
                        <span>
                            <EditableContext.Consumer>
                            {form => (
                                <a
                                    href="javascript:;"
                                    onClick={() => this.save(form, record.id)}
                                    style={{ marginRight: 8 }}
                                >
                                保存
                                </a>
                            )}
                            </EditableContext.Consumer>
                            <a
                                href="javascript:;"
                                onClick={() => this.cancel(record.id)}
                                style={{ marginRight: 8 }}
                            >
                            取消
                            </a>
                        </span>
                        ) : (
                        <a onClick={() => this.edit(record.id)}>修改</a>
                        )}
                    </div>
                    );
                },
            },
        ];

        const wcolumns = weightsColumns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => (
                    {
                        record,
                        inputType: col.inputType,
                        dataIndex: col.dataIndex,
                        title: col.title,
                        editing: this.isEditing(record),
                    }
                ),
            };
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
                                    <Tree.DirectoryTree onSelect={this.onSelect} defaultExpandAll={true} showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.manager.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i} defaultExpandAll={true} >
                                                    { this.props.manager.orgs.map((o,i)=>{
                                                        if(o.org_type_id==t.id) {
                                                            return (
                                                                <Tree.TreeNode title={ o.short_name } key={"0-0-0-"+i} defaultExpandAll={true}>
                                                                    { this.props.manager.managers.map((m,i)=>{
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
                                <div className="list">
                                    <div style={{ marginBottom: 16,display: 'flex',flexDirection: 'row' }}>
                                        <Input.Search
                                            placeholder=""
                                            enterButton="搜索"
                                            size="default"
                                            onSearch={ value => {
                                                this.props.manager.search_name = value;
                                                this.props.manager.view = 'list';
                                                this.props.manager.loadManager();
                                            }}
                                            style={{ width:200 }}
                                        />
                                        <div style={{ width:15 }}></div>
                                        <Button
                                            onClick={this.add}
                                        >
                                            新增
                                        </Button>
                                        <div style={{ width:15 }}></div>
                                        <Popconfirm placement="bottom" title="确定删除吗?" onConfirm={this.del} okText="确定" cancelText="取消">
                                            <Button>
                                                删除
                                            </Button>
                                        </Popconfirm>
                                        <div style={{ width:15 }}></div>
                                        <Button
                                            onClick={this.do_import}
                                        >
                                            导入
                                        </Button>
                                        <div style={{ width:15 }}></div>
                                        <Button
                                            onClick={this.do_export}
                                        >
                                            导出
                                        </Button>
                                    </div>
                                    <Table
                                        rowKey="id"
                                        components={ components }
                                        dataSource={ this.props.manager.view!='list'?[]:(this.props.manager.model=='manager'?[...this.props.manager.managers]:[...this.props.manager.weights].filter(item=>item.manager_id==this.props.manager.manager.id)) }
                                        columns={ this.props.manager.model=='manager'?mcolumns:wcolumns }
                                        rowSelection={{
                                            onChange: (selectedRowKeys, selectedRows) => {
                                                this.setState({ selected:selectedRows })
                                            },
                                            onSelect: (record, selected, selectedRows) => {
                                            },
                                            onSelectAll: (selected, selectedRows, changeRows) => {
                                            }
                                        }}
                                        // pagination={ false }
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