import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, Select, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './org.css';

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
                    { editing ? (
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
                                        if(this.props.dataIndex=='sort') {
                                            return <InputNumber min={1} />;
                                        }
                                        return <InputNumber />;
                                    }
                                    if (this.props.inputType === 'select' && this.props.dataIndex === 'org_type_id') {
                                        return (
                                            <Select placeholder="请选择">
                                                { ([...this.props.optiondatas]).map((c,i)=>(
                                                    <Select.Option key={c.id} value={c.id}>{c.name}</Select.Option>
                                                ))}
                                            </Select>
                                        )
                                    }
                                    return <Input />;
                                }).call(this)
                            )
                        }
                    </FormItem>
                    ) : restProps.children }
                </td>
                );
            }}
            </EditableContext.Consumer>
        );
    }
}

@inject('app','org')
@observer
export default class Org extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editingKey:'',
            selected:[]
        }
    }

    componentWillMount() {
        this.props.org.load();
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
            
            const orgs = [...this.props.org.orgs];
            const index = orgs.findIndex(item => id === item.id);
            if (index > -1) {
                let item = orgs[index];
                item = {...item,...row};

                let rindex = orgs.findIndex(tmp => (tmp.short_name === item.short_name||tmp.full_name === item.full_name)&&tmp.id!=item.id);
                if(rindex>-1){
                    notification.open({ message: '操作提示', description: '单位简称或全称重复!'});
                    return;
                }
                if(item.id===0) {
                    this.props.org.save(item);
                } else {
                    this.props.org.update(item.id,item);
                }
                this.setState({ editingKey: '' });
            } else {
                this.setState({ editingKey: '' });
            }
        });
    }

    cancel = () => {
        this.props.org.cancel();
        this.setState({ editingKey: '' });
    };

    add = () => {
        let hasNew = (([...this.props.org.orgs]).findIndex(item => item.id === 0)>=0);
        if(!hasNew) {
            this.props.org.add();
            this.setState({ editingKey: 0 });
            if(!!this.table){
                let page_count = (this.props.org.orgs.length % this.table.state.pagination.pageSize) != 0 ? parseInt(this.props.org.orgs.length / this.table.state.pagination.pageSize) + 1 : (this.props.org.orgs.length / this.table.state.pagination.pageSize);
                this.table.state.pagination.current = page_count;
            }
        } else {
            notification.open({ message: '操作提示', description: '请先保存'});
        }
    }

    del = () => {
        let ids = []
        this.state.selected.filter((item)=>ids.push(item.id));
        if(ids.length>0) {
            this.props.org.delete(ids);
        }
    }

    do_export = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('export-selected-directory', (event, path) => {
                this.props.org.do_export(path); 
            });
            ipcRenderer.send('export-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.save_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '保存路径'+p});
                    this.props.org.do_export(p);
                }
            });
        }
    }

    do_import = () => {
        try {
            const ipcRenderer = window.require('electron').ipcRenderer;
            ipcRenderer.on('import-selected-directory', (event, path) => {
                this.props.org.do_import(path); 
            });
            ipcRenderer.send('import-open-dialog');
        } catch(e) {
            console.error(e);
        }
        if(!!window.interaction) {
            window.interaction.open_excel_file_dialog((p)=>{
                if(!!p) {
                    notification.open({ message: '操作提示', description: '导入路径'+p});
                    this.props.org.do_import(p);
                }
            });
        }
    }

    render() {
        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            },
        };

        const origanalColumns = [
            {
                title: '序号',
                dataIndex: '',
                width: '8%',
                editable: false,
                align:'center',
                render: (text, record, index) => {
                    return ([...this.props.org.orgs]).findIndex(item => record.id==item.id) + 1;
                }
            },
            {
                title: '单位类型',
                dataIndex: 'org_type_id',
                width: '12%',
                inputType: 'select',
                editable: true,
                render: (text, record, index) => {
                    return (record.org_type||{}).name;
                }
            },
            {
                title: '单位简称',
                dataIndex: 'short_name',
                width: '25%',
                inputType: 'text',
                editable: true,
            },
            {
                title: '单位全称',
                dataIndex: 'full_name',
                width: '30%',
                inputType: 'text',
                editable: true,
            },
            {
                title: '显示顺序',
                dataIndex: 'sort',
                width: '10%',
                inputType: 'number',
                editable: true,
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

        const columns = origanalColumns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => ({
                    record,
                    inputType: col.inputType,
                    dataIndex: col.dataIndex,
                    title: col.title,
                    editing: this.isEditing(record),
                    optiondatas: [...this.props.org.orgtypes]
                }),
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
                            <div style={{ marginBottom: 16,display: 'flex',flexDirection: 'row' }}>
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
                                ref={node => this.table = node}
                                rowKey="id"
                                components={components}
                                dataSource={[...this.props.org.orgs]}
                                columns={columns}
                                rowSelection={{
                                    onChange: (selectedRowKeys, selectedRows) => {
                                        this.setState({ selected:selectedRows })
                                    },
                                    onSelect: (record, selected, selectedRows) => {
                                    },
                                    onSelectAll: (selected, selectedRows, changeRows) => {
                                    }
                                }}
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