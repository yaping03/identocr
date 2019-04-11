import React from 'react';
import { Menu,Input,Button,Icon,Alert } from 'antd';

import fs from 'fs';

import './top.css';

const topjpg = fs.readFileSync(__dirname + '/../static/images/top.jpg');

export default class Top extends React.Component {
    render() {
        return (
            <div style={{ width:'100%',height:'100%',display:'flex',flexDirection:'row',alignItems:'center',justifyContent:'flex-start',padding:'0 15px' }}>
                <div style={{ flex:1,display:'flex',flexDirection:'row' }}>
                    <div style={{ flex:1,display:'flex',justifyContent:'flex-start' }}>
                        <img src={`data:image/png;base64,${topjpg.toString('base64')}`} style={{ width:'100%' }} />
                    </div>
                </div>
                <div style={{ position:'absolute',right:30 }}>
                    <a
                        href="javascript:;"
                        onClick={() => this.props.history.push('/login')}
                        style={{ marginRight: 8 }}
                    >
                        <div style={{ width:160,textAlign:'right',color:'#000',fontSize:24 }}>
                            <span>退出  <Icon type="logout" /></span>
                        </div>
                    </a>
                </div>
            </div>
        )
    }
}