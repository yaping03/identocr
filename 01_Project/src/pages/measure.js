import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import Foot from '../components/foot';

import './measure.css';

const FormItem = Form.Item;
const EditableContext = React.createContext();

const EditableRow = ({ form, index, ...props }) => (
    <EditableContext.Provider value={form}>
        <tr {...props} />
    </EditableContext.Provider>
);

const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends React.Component {
    getInput = () => {
        if (this.props.inputType === 'number') {
            if(this.props.dataIndex=='weight') {
                return <InputNumber min={0} max={100} formatter={value => `${value}%`} parser={value => value.replace('%', '')} />;
            }
            if(this.props.dataIndex=='sort') {
                return <InputNumber min={1} />;
            }
            return <InputNumber />;
        }
        return <Input />;
    };
  
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
                        {getFieldDecorator(dataIndex, {
                        rules: [{
                            required: true,
                            message: `请输入 ${title}!`,
                        }],
                        initialValue: record[dataIndex],
                        })(this.getInput())}
                    </FormItem>
                    ) : restProps.children}
                </td>
                );
            }}
            </EditableContext.Consumer>
        );
    }
}

@inject('app','measure')
@observer
export default class Measure extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editingKey:'',
            defaultExpandedKeys:['0-0'],
            defaultSelectedKeys:[]
        }
    }

    componentWillMount() {
        this.props.measure.load();
    }

    componentWillReact() {
        if(!!this.props.measure.exam && this.state.defaultSelectedKeys.length==0) {
            let defaultSelectedKeys = [];
            defaultSelectedKeys.push('0-0-'+this.props.measure.exam.id);
            this.setState({ defaultSelectedKeys });
        }
    }

    onSelect = (selectedKeys, info) => {
        let paths = selectedKeys[0].split('-');
        if(paths.length==3) {
            this.props.measure.selectExam(([...this.props.measure.exams]).find(item => parseInt(paths[2])==item.id));
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
            let sum = 0;
            ([...this.props.measure.measures]).map((item,index)=>{
                if(item.id===id){
                    sum += parseFloat(row.weight);
                } else {
                    sum += parseFloat(item.weight);
                }
            });
            if(sum!=100) {
                notification.open({ message: '操作提示', description: '权重之和('+sum+'%)不为100%'});
            }
            this.props.measure.update(id,row);
            this.setState({ editingKey: '' });
        });
    }

    cancel = () => {
        this.setState({ editingKey: '' });
    };

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
                    return ([...this.props.measure.measures]).findIndex(item => record.id==item.id) + 1;
                }
            },
            {
                title: '评价表',
                dataIndex: 'exam_content.exam.name',
                width: '20%',
                editable: false,
            },
            {
                title: '考评内容',
                dataIndex: 'exam_content.content',
                width: '15%',
                editable: false,
            },
            {
                title: '指标名称',
                dataIndex: 'name',
                width: '15%',
                editable: false,
            },
            {
                title: '权重',
                dataIndex: 'weight',
                width: '13%',
                editable: true,
                render: (text, record, index) => {
                    return `${text}%`;
                }
            },
            {
                title: '显示顺序',
                dataIndex: 'sort',
                width: '12%',
                editable: true,
                align:'center'
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
                    inputType: (col.dataIndex === 'weight'||col.dataIndex === 'sort') ? 'number' : 'text',
                    dataIndex: col.dataIndex,
                    title: col.title,
                    editing: this.isEditing(record),
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
                            <div className="split">
                                <div className="tree">
                                    <Tree.DirectoryTree
                                        defaultExpandAll
                                        defaultExpandedKeys={ this.state.defaultExpandedKeys }
                                        defaultSelectedKeys={ this.state.defaultSelectedKeys }
                                        onSelect={ this.onSelect }
                                        showIcon={ false }>
                                        <Tree.TreeNode title="评价指标及权重" key="0-0">
                                            { ([...this.props.measure.exams]).map((m,i)=> {
                                                return (
                                                    <Tree.TreeNode title={ m.name } key={"0-0-"+m.id} isLeaf />
                                                );
                                            })}
                                        </Tree.TreeNode>
                                    </Tree.DirectoryTree>
                                </div>
                                <div className="line"></div>
                                <div className="list">
                                    <Table
                                        rowKey="id"
                                        components={components}
                                        dataSource={ [...this.props.measure.measures] }
                                        columns={columns}
                                        pagination={false}
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