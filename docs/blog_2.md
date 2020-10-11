## 目录
## 一、简介
## 二、代码初步介绍
## 三、代码细节介绍
======================= 大爽歌作，made by big shuang =======================
### 二、代码初步介绍
本文初步介绍下项目各个文件是做什么的
#### 1 文件夹初步介绍
- `css/`: 存放绘制网页所需要的css样式文件
- `docs/`: 存放各种说明文档
- `images/`: 存放项目需要的图片，其中`icons`文件夹存放流程图需要的操作性质图标。
- `js/`: 存放项目js文件
- `node_modules/`: 存放导入的js库文件，例如`jquery`库
- `output/`: 存放一些示例文件
- 其他：其他文件夹暂与流程图绘制工具无关（可能与录像自动分析工具相关），在此不做介绍

#### 2 文件夹详细介绍
##### - `images/nodes`
在此目录下为三个阵营文件夹，
- Allied: 盟军
- Soviet：苏联
- Imperial：帝国
阵营文件夹下为单位种类文件夹：
- Aircraft: 空军
- Defenses: 防御性（支援性）建筑
- Infantry: 步兵单位
- Production: 生产性（科技）建筑
- Superweapons: 超级武器技能
- Top Secret Protocol: 绝密协议
- Vehicles: 载具单位
- Vessels: 船舶单位
种类文件夹下为单位图片，单位图片文件名格式一般如下：`RA3 单位名 Icons.png`
如果说是起义时刻的单位，则开头为`RA3U`；
有几个特殊图片没有这么命名：
 盟军高级许可：`RA3_Heightened_Clearance_Icons.png`
 盟军最高许可：`RA3_Maximum_Clearance_Icons.png`

#### 3 重要文件介绍
##### - main.html / 主页.html
流程图工具绘制页面，项目程序入口，一个是英文版，一个是中文版
##### - README.md / README_ZH.md
基础介绍文档，一个是英文版，一个是中文版
##### - js/global_setting.js
全局设置js文件，存放一些基础性质的js变量，
##### - js/info.js
所有单位的名字和图片文件路径信息，由`util.py`脚本生成，亦可手动修改。
流程图绘制工具栏中内容就是用该文件生成的。
##### - js/main.js
js主文件，实现了一些流程图绘制工具直接调用的方法
##### - js/mynode.js
实现了流程图节点类：DataNode；
以及用于存放节点数据的类：UnitData， LineData
UnitData代表的是每一行起始的节点，根节点，这一行后续所有的节点都是描述这个根节点的
LineData表的是每一行根节点后的节点
##### - js/text.js / js/zh_text.js
存放网页文本变量的js文件，第一个存放英文版，第二个存放中文版
#### - js/util.js
辅助性js文件，实现了一些供main.js和mynode.js调用的方法
