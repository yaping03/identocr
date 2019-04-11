import React from 'react';
import { Menu,Input,Button,Icon,Alert } from 'antd';

import './left.css';

const menus = [
    {
        "key":"1",
        "icon":"edit",
        "label":"考核办法定义",
        "menus":[
            {
                "key":"measure",
                "icon":"bars",
                "label":"指标及权重"
            },
            {
                "key":"entity",
                "icon":"edit",
                "label":"测评主体权重"
            }
        ]
    },
    {
        "key":"2",
        "icon":"form",
        "label":"基础信息管理",
        "menus":[
            {
                "key":"org",
                "icon":"schedule",
                "label":"单位管理"
            },
            {
                "key":"score",
                "icon":"layout",
                "label":"班子业绩管理"
            },
            {
                "key":"manager",
                "icon":"idcard",
                "label":"中层干部管理"
            }
        ]
    },
    {
        "key":"4",
        "icon":"tablet",
        "label":"投票数据",
        "menus":[
            {
                "key":"generate",
                "icon":"profile",
                "label":"数据采集"
            },
            {
                "key":"resultteam",
                "icon":"book",
                "label":"领导班子评价票"
            },
            {
                "key":"resultmanager",
                "icon":"solution",
                "label":"中层干部考评票"
            }
        ]
    },
    {
        "key":"5",
        "icon":"pie-chart",
        "label":"分析应用",
        "menus":[
            {
                "key":"check",
                "icon":"safety",
                "label":"考评验证计算"
            },
            {
                "key":"reportteam",
                "icon":"table",
                "label":"领导班子考评汇总"
            },
            {
                "key":"reportmanager",
                "icon":"exception",
                "label":"中层干部评价汇总"
            },
            // {
            //     "key":"reportpeople",
            //     "icon":"idcard",
            //     "label":"中层干部评价汇总(个人)"
            // },
            {
                "key":"reportexam",
                "icon":"area-chart",
                "label":"测评信息"
            }
        ]
    },
    {
        "key":"6",
        "icon":"setting",
        "label":"系统管理",
        "menus":[
            // {
            //     "key":"db",
            //     "icon":"upload",
            //     "label":"系统数据管理"
            // },
            {
                "key":"password",
                "icon":"lock",
                "label":"修改密码"
            }
        ]
    }
];

export default class Left extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            openKeys:[]
        }
    }

    componentWillMount() {
    }

    onOpenChange = (openKeys) => {
        this.setState({ openKeys:[ openKeys[openKeys.length-1] ] });
    }

    render() {
        const pathname = this.props.history.location.pathname.substr(1);
        let openkeys = this.state.openKeys;
        if(openkeys.length==0&&!!pathname&&!this.props.collapsed) {
            let found = false;
            for(let i=0;i<menus.length;i++) {
                let menu = menus[i];
                for(let j=0;j<menu.menus.length;j++) {
                    let sub = menu.menus[j];
                    if(sub.key==pathname) {
                        found = true;
                        openkeys = [menu.key];
                        break;
                    }
                }
                if(found) break;
            }
        }
        return (
            <Menu
                mode="inline"
                theme="light"
                onClick={(item)=>{
                    this.props.history.push(item.key);
                }}
                onOpenChange={this.onOpenChange}
                defaultSelectedKeys={[pathname]}
                openKeys={openkeys}
                >
                { menus.map((submenu,index)=>(
                    <Menu.SubMenu key={submenu.key} title={
                        <span>
                            <Icon type={submenu.icon} />
                            <span>{submenu.label}</span>
                        </span>
                    }>
                        { submenu.menus.map((menu,index)=>(
                            <Menu.Item key={menu.key}>
                                <Icon type={menu.icon} />
                                <span>{menu.label}</span>
                            </Menu.Item>
                        ))}
                    </Menu.SubMenu>
                ))}
            </Menu>
        )
    }
}