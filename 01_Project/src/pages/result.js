import React from 'react';
import { inject, observer } from 'mobx-react';

import { Layout, Alert, Button, Tree, Table, Input, InputNumber, Popconfirm, Form, Icon, notification } from 'antd';

import './result.css';

@inject('app','admin')
@observer
export default class Result extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        }
    }

    componentWillMount() {
    }

    onClickOpen = () => {
        this.props.admin.scan();
    }

    getPoint = (item,index) => {
        let points = item.points;
        for(let point of points) {
            if(point.kpi==index) {
                return (
                    <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center'}}>
                        { point.point>0?point.point:"" }
                    </div>
                )
            }
        }
    }

    render() {
        console.log(this.props);
        return (
            <Spin spinning={this.props.admin.loading} style={{ width:'100%',height:'100%' }}>
                <div style={{ width:'100%',height:'100%',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                    <div style={{ width:'100%',height:20 }}></div>
                    { this.props.admin.title && 
                        <div style={{ width:'100%',height:'30',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>{this.props.admin.title[0].words }</div>
                    }
                    <div style={{ width:'100%',height:20 }}></div>
                    <div style={{ width:'100%',height:'30',display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>
                    { this.props.admin.org && 
                        <div style={{ width:'100%',height:'30',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>{this.props.admin.org[0].words }</div>
                    }
                    { this.props.admin.date && 
                        <div style={{ width:'100%',height:'30',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>{this.props.admin.date[0].words }</div>
                    }
                    </div>
                    <div style={{ width:'100%',height:20 }}></div>
                    { this.props.admin.points &&
                        <div style={{ width:'100%',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center' }}>
                            <div style={{ width:'100%',backgroundColor:'#EEE',height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center',borderBottom:'solid',borderBottomColor:'#DDD',borderBottomWidth:1 }}>
                                <div style={{ width:50,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}></div>
                                <div style={{ flex:3,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'flex-start' }}>考评指标</div>
                                <div style={{ flex:1,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>评分分值</div>
                            </div>
                            { this.props.admin.points.map((item) => (
                                <div style={{ width:'100%',height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center',borderBottom:'solid',borderBottomColor:'#DDD',borderBottomWidth:1 }}>
                                    <div style={{ width:50,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>{ item.kpi }</div>
                                    <div style={{ flex:3,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'flex-start' }}>{ item.name[0].words }</div>
                                    <div style={{ flex:1,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>{ item.point }</div>
                                </div>
                            ))}
                        </div>
                    }
                    { this.props.admin.datas &&
                        <div style={{ width:'100%',display:'flex',flexDirection:'row',alignItems:'flex-start',justifyContent:'center' }}>
                            <div style={{ width:80,backgroundColor:'#EEE',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'flex-start' }}>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}></div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>政治素质</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>职业素养</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>廉洁自律</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>决策能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>执行能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>领导能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>学习能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>创新能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>沟通能力</div>
                                <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>个人贡献</div>
                            </div>
                            <div style={{ flex:1,display:'flex',flexDirection:'column',alignItems:'flex-start',justifyContent:'flex-start' }}>
                                <div style={{ width:'100%',height:40,backgroundColor:'#EEE',display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>
                                    { this.props.admin.datas.map((item) => (
                                        <div style={{ flex:1,height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center'}}>
                                            { !!item.name&&item.name.length>0?item.name[0].words:"" }
                                        </div>
                                    ))}
                                </div>
                                { [9,10,11,12,13,14,15,16,17,18].map((index) => (
                                <div style={{ width:'100%',height:40,display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'center' }}>
                                    { this.props.admin.datas.map((item) => this.getPoint(item,index) )}
                                </div>
                                ))}
                            </div>
                        </div>
                    }
                    <div style={{ width:'100%',flex:1,display:'flex',alignItems:'center',justifyContent:'center',marginTop:5,marginBottom:5 }}>
                        <Button style={{ width:'100%',marginLeft:15,marginRight:15 }} onClick={ this.onClickOpen }>
                            识别文件
                        </Button>
                    </div>
                </div>
            </Spin>
        );
    }
}