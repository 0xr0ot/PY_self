# *Welcme to [ECharts](http://gallery.echartsjs.com/explore.html#sort=rank~timeframe=all~author=all) and [Pyecharts](https://github.com/chenjiandongx/pyecharts) !*

|Team|[qxiu_BI](http://bi.qxiu.com)|
| :---: | :---: |
|Author|ulion.tse|
|Date|2017-09-26|

## *一、[ECharts](http://gallery.echartsjs.com/explore.html#sort=rank~timeframe=all~author=all)快速使用*
*1.demo.html*
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
	<title>my_map</title>
	<!-- 本地引入,地图还是链接
    <script src="./echarts_offical/echarts.js"></script>
    <script src="./echarts_offical/vintage.js"></script>
    <script type="text/javascript" src="http://echarts.baidu.com/gallery/vendors/echarts/map/js/china.js"></script>
    -->

    <!-- 开发者模式获取 	-->
    <script type="text/javascript" src="http://gallerybox.echartsjs.com/dep/echarts/latest/echarts.min.js"></script>
    <script type="text/javascript" src="http://gallerybox.echartsjs.com/dep/echarts/map/js/china.js"></script>

	<!-- 网友提供，但echarts版本已3.7.1
	<script src="http://cdn.bootcss.com/echarts/3.2.2/echarts.min.js"></script>
	<script src="http://echarts.baidu.com/asset/map/js/china.js"></script>
	-->

	<!-- 最新echarts_cdn,须结合china.js
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.1/echarts.min.js"></script>
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.1/extension/bmap.min.js"></script>
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/echarts/3.7.1/extension/dataTool.min.js"></script>
	-->

</head>
<body>
    <div id="main_map" style="width: 1300px;height: 600px;"></div>
    <!--以下是echarts的同级目录js引用-->
    <script src="./demo.js"></script>
</body>
</html>
```

*2.demo.js*
```javascript
/**
 * Created by Administrator on 2017/9/25.
 */
var myChart_map = echarts.init(document.getElementById('main_map'),"vintage");//须手动添加//

function randomData() {
    return Math.round(Math.random()*1000);
}

option_map = {
    title: {
        text: 'iphone销量',
        subtext: '纯属虚构',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:['iphone3','iphone4','iphone5']
    },
    visualMap: {
        min: 0,
        max: 2500,
        left: 'left',
        top: 'bottom',
        text: ['高','低'],// 文本，默认为数值文本
        calculable: true
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    series: [
        {
            name: 'iphone3',
            type: 'map',
            mapType: 'china',
            roam: false,
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {name: '北京',value: randomData() },
                {name: '天津',value: randomData() },
                {name: '上海',value: randomData() },
                {name: '重庆',value: randomData() },
                {name: '河北',value: randomData() },
                {name: '河南',value: randomData() },
                {name: '云南',value: randomData() },
                {name: '辽宁',value: randomData() },
                {name: '黑龙江',value: randomData() },
                {name: '湖南',value: randomData() },
                {name: '安徽',value: randomData() },
                {name: '山东',value: randomData() },
                {name: '新疆',value: randomData() },
                {name: '江苏',value: randomData() },
                {name: '浙江',value: randomData() },
                {name: '江西',value: randomData() },
                {name: '湖北',value: randomData() },
                {name: '广西',value: randomData() },
                {name: '甘肃',value: randomData() },
                {name: '山西',value: randomData() },
                {name: '内蒙古',value: randomData() },
                {name: '陕西',value: randomData() },
                {name: '吉林',value: randomData() },
                {name: '福建',value: randomData() },
                {name: '贵州',value: randomData() },
                {name: '广东',value: randomData() },
                {name: '青海',value: randomData() },
                {name: '西藏',value: randomData() },
                {name: '四川',value: randomData() },
                {name: '宁夏',value: randomData() },
                {name: '海南',value: randomData() },
                {name: '台湾',value: randomData() },
                {name: '香港',value: randomData() },
                {name: '澳门',value: randomData() }
            ]
        },
        {
            name: 'iphone4',
            type: 'map',
            mapType: 'china',
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {name: '北京',value: randomData() },
                {name: '天津',value: randomData() },
                {name: '上海',value: randomData() },
                {name: '重庆',value: randomData() },
                {name: '河北',value: randomData() },
                {name: '安徽',value: randomData() },
                {name: '新疆',value: randomData() },
                {name: '浙江',value: randomData() },
                {name: '江西',value: randomData() },
                {name: '山西',value: randomData() },
                {name: '内蒙古',value: randomData() },
                {name: '吉林',value: randomData() },
                {name: '福建',value: randomData() },
                {name: '广东',value: randomData() },
                {name: '西藏',value: randomData() },
                {name: '四川',value: randomData() },
                {name: '宁夏',value: randomData() },
                {name: '香港',value: randomData() },
                {name: '澳门',value: randomData() }
            ]
        },
        {
            name: 'iphone5',
            type: 'map',
            mapType: 'china',
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {name: '北京',value: randomData() },
                {name: '天津',value: randomData() },
                {name: '上海',value: randomData() },
                {name: '广东',value: randomData() },
                {name: '台湾',value: randomData() },
                {name: '香港',value: randomData() },
                {name: '澳门',value: randomData() }
            ]
        }
    ]
};

myChart_map.setOption(option_map);//须手动添加//
```
*2.使用方法*
```python
1.引用echarts渲染官方必要的js文件在demo.html头部;
2.粘贴你所需要的echats图形的js代码到你的demo.js文件,头部加上如"var myChart_map = echarts.init(document.getElementById('main_map'),"vintage");",尾部加上如"myChart_map.setOption(option_map);",头尾一一对应;
3.最后将你的demo.js引用到你的demo.html文件展示区域即可.
```

## *二、[Pyecharts](https://github.com/chenjiandongx/pyecharts)快速使用*

*Example:*

```python
from pyecharts import Line3D

import math
_data = []
for t in range(0, 25000):
    _t = t / 1000
    x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
    y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
    z = _t + 2.0 * math.sin(75 * _t)
    _data.append([x, y, z])
range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
               '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
line3d = Line3D("3D 折线图示例", width=1200, height=600)
line3d.add("", _data, is_visualmap=True, visual_range_color=range_color, visual_range=[0, 30],
           is_grid3d_rotate=True, grid3d_rotate_speed=180)
line3d.render()#生成一个render.html文件,所见即所得.
```
