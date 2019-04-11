import React from 'react';
import moment from 'moment';

import './foot.css';

export default class Foot extends React.Component {
    render() {
        return (
            <div style={{ width:'100%',height:40,paddingLeft:80,display:'flex',background:'#99c1d4',flexDirection:'row',justifyContent:'flex-end',alignItems:'flex-end',alignSelf:'flex-end' }}>
                <div style={{ width:20 }}>|</div>
                <div style={{ width:90 }}>{ moment().format('YYYY.MM.DD') }</div>
                <div style={{ width:20 }}>|</div>
                <div style={{ width:290 }}>Copyright @2018 中交上海航道局有限公司</div>
                <div style={{ width:20 }}>|</div>
            </div>
        )
    }
}