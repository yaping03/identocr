import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Spin, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import Top from '../components/top';
import Left from '../components/left';

import './score.css';

import Foot from '../components/foot';

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
            calcelateValue,
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
                                initialValue: calcelateValue||record[dataIndex],
                            })(
                                (() => {
                                    if (this.props.inputType === 'number') {
                                        if(this.props.dataIndex=='weight') {
                                            return <InputNumber min={0} max={100} formatter={value => `${value}%`} parser={value => value.replace('%', '')} />;
                                        }
                                        if(this.props.dataIndex=='score_1'||this.props.dataIndex=='score_2'||this.props.dataIndex=='score_3') {
                                            return <InputNumber step={0.1} />;
                                        }
                                        if(this.props.dataIndex=='sort') {
                                            return <InputNumber min={1} />;
                                        }
                                        return <InputNumber />;
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

@inject('app','score')
@observer
export default class Score extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editingKey:'',
            selected:[]
        }
    }

    componentWillMount() {
        this.props.score.load();
    }

    componentWillReact() {
        console.log('componentWillReact',this.props.score.model,this.props.score.model == "added",!!this.props.score.weights,this.props.score.weights.length > 0);
        if(this.props.score.model == "added" && !!this.props.score.weights && this.props.score.weights.length > 0) {
            this.props.score.model = 'list';
            this.setState({ editingKey:this.props.score.weights[this.props.score.weights.length-1].id });
            console.log('/*/*/*/*/',this.props.score.weights,this.props.score.weights.length);
        }
    }

    onSelect = (selectedKeys, info) => {
        console.log('onSelect',selectedKeys,info)
        let paths = selectedKeys[0].split('-');
        if(paths.length==4) {
            this.props.score.selectOrg(([...this.props.score.orgs])[parseInt(paths[3])]);
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
            ([...this.props.score.weights]).map((item,index)=>{
                if(item.id===id){
                    sum += parseFloat(row.weight);
                } else {
                    sum += parseFloat(item.weight);
                }
            });
            if(sum!=100) {
                notification.open({ message: '操作提示', description: '权重之和('+sum+'%)不为100%'});
            }
            const newData = [...this.props.score.weights];
            const index = newData.findIndex(item => id === item.id);
            if (index > -1) {
                const item = newData[index];
                if(item.id===0) {
                    this.props.score.save({...item,...row});
                } else {
                    this.props.score.update(item.id,{...item,...row});
                }
                this.setState({ editingKey: '' });
            } else {
                newData.push(row);
                this.setState({ editingKey: '' });
            }
        });
    }

    cancel = () => {
        this.props.score.cancel();
        this.setState({ editingKey: '' });
    };

    add = () => {
        let hasNew = (([...this.props.score.orgs]).findIndex(item => item.id === 0)>=0);
        if(!hasNew) {
            this.props.score.add();
            this.setState({ editingKey: 0 });
        } else {
            notification.open({ message: '操作提示', description: '请先保存'});
        }
    }

    del = () => {
        let ids = []
        this.state.selected.filter((item)=>ids.push(item.id));
        if(ids.length>0) {
            this.props.score.delete(ids);
        }
    }

    calcelate = (dataIndex,record) => {
        if(dataIndex=='score_1') {
            return (this.props.score.scores.find((item)=>{
                if(record.id==0) {
                    return record.id==item.id;
                } else {
                    return item.org_id==record.org_id && item.year==record.year && item.exam_measure.name=='企业党建';
                }
            })||{}).score;
        } else if(dataIndex=='score_2') {
            return (this.props.score.scores.find((item)=>{
                if(record.id==0) {
                    return record.id==item.id;
                } else {
                    return item.org_id==record.org_id && item.year==record.year && item.exam_measure.name=='绩效成果';
                }
            })||{}).score;
        } else {
            return null;
        }
    }

    render() {
        console.log('render:',this.props);

        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            }
        };

        const origanalColumns = [
            {
                title: '序号',
                dataIndex: '',
                width: '8%',
                editable: false,
                align:'center',
                render: (text, record, index) => {
                    return ([...this.props.score.weights]).findIndex(item => record.id==item.id) + 1;
                }
            },
            {
                title: '年度',
                dataIndex: 'year',
                width: '12%',
                editable: false,
                inputType: 'number'
            },
            {
                title: '企业党建',
                dataIndex: 'score_1',
                width: '15%',
                editable: true,
                inputType: 'number',
                // render: (text, record, index) => {
                //     return (
                //         <span>
                //         {
                //             (this.props.score.scores.find((item)=>{
                //                 if(record.id==0) {
                //                     return record.id==item.id;
                //                 } else {
                //                     return item.org_id==record.org_id && item.year==record.year && item.exam_measure.name=='企业党建';
                //                 }
                //             })||{}).score
                //         }
                //         </span>
                //     )
                // }
            },
            {
                title: ((this.props.score.org||{}).org_type||{}).name=='基层单位'?'班子业绩':'部门业绩',
                dataIndex: 'score_2',
                width: '15%',
                editable: true,
                inputType: 'number',
                // render: (text, record, index) => {
                //     return (
                //         <span>
                //         { 
                //             (this.props.score.scores.find((item)=>{
                //                 if(record.id==0) {
                //                     return record.id==item.id;
                //                 } else {
                //                     return item.org_id==record.org_id && item.year==record.year && item.exam_measure.name=='绩效成果';
                //                 }
                //             })||{}).score
                //         }
                //         </span>
                //     )
                // }
            },
            {
                title: '民主评测',
                dataIndex: 'score_3',
                width: '15%',
                editable: false,
                inputType: 'number',
                render: (text, record, index) => {
                    const num = (this.props.score.results.find((item)=>{
                        return item.org_id==record.org_id && item.year==record.year;
                    })||{}).org_score||0;
                    return (
                        <span>
                        { 
                            num>0?num.toFixed(2):0
                        }
                        </span>
                    )
                }
            },
            {
                title: '权重',
                dataIndex: 'weight',
                width: '15%',
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

        const columns = origanalColumns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => ({
                    record,
                    inputType: col.inputType||'text',
                    dataIndex: col.dataIndex,
                    title: col.title,
                    editing: this.isEditing(record),
                    calcelateValue: this.calcelate(col.dataIndex,record)
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
                                    <Tree.DirectoryTree onSelect={this.onSelect} defaultExpandAll={true} showIcon={false}>
                                        <Tree.TreeNode title="中交上航局" key="0-0">
                                            { this.props.score.orgtypes.map((t,i)=>(
                                                <Tree.TreeNode title={ t.name } key={"0-0-"+i} defaultExpandAll={true} >
                                                    { this.props.score.orgs.map((o,i)=>{
                                                        if(o.org_type_id==t.id) {
                                                            return (
                                                                <Tree.TreeNode title={ o.short_name } key={"0-0-0-"+i} defaultExpandAll={true} isLeaf />
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
                                    </div>
                                    <Table
                                        rowKey="id"
                                        components={components}
                                        dataSource={ [...this.props.score.weights] }
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