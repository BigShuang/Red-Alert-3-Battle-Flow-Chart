## python实现红警三录像文件读取与自动分析生成流程图信息——三、拓展给mod使用


## 总目录
## [一、简介](https://blog.csdn.net/python1639er/article/details/108952283)
## [二、项目结构与代码初步介绍](https://blog.csdn.net/python1639er/article/details/108988289)
## 三、拓展给mod使用
======================= 大爽歌作，made by big shuang =======================

## 三、拓展给mod使用
### 1 - 为流程图绘制工具拓展
这个拓展起来还是比较简单的。
主要是添加图片素材就可以，
在`images/nodes`文件夹下，根据单位种类找到其所属于的文件夹添加单位图片，文件夹和命名格式可见
[https://blog.csdn.net/python1639er/article/details/108941354](https://blog.csdn.net/python1639er/article/details/108941354)的->2 文件夹详细介绍 ->images/nodes
添加好之后，
如果电脑安装有python3，运行util.py文件生成info.js
如果不愿意安装python3，手动修改info.js亦可。

- 如果有新的阵营
a - 在`images/nodes`文件夹下新建文件夹，文件夹名称为新阵营的英文名，文件夹内容参考其他三个现有阵营布置
b - 在`js/global_setting.js`内，
修改第16行，在CAMPS中添加new_faction_name
如果不懂怎么修改，就直接将第16行修改为
```javascript
var CAMPS = ["Soviet", "Allied", "Imperial", "new_faction_name"];
```
其中new_faction_name为新阵营的英文名，和a中的要能够对应


### 2 - 为录像自动分析工具拓展
这个拓展起来会比上面麻烦一些，而且有如下限制
- 只支持苏盟两个阵营
- 如果mod苏盟建造方式有变化，拓展可能会失败

*同时这里只是简单的介绍一下新的单位的拓展，更深入的拓展可能需要了解下代码，或者部分变量的意义*

a - 对于新增单位，首先要在`ra3autohander/replay_config.py`的`UNITNAMES`添加单位id和单位名称键值对，id应该mod作者是知道的

单位名称格式要求，要和`images/nodes`中的图片名按照某种规则对应，举例如下（以苏联矿场为例）
其在`images/nodes`下`Production`文件名为
`RA3 Soviet Ore Refinery Icons.png`
在`UNITNAMES`中的单位名称则为`S Soviet Ore Refinery`,
开头为阵营名英文开头大写，后面为图片文件名去掉`RA3 `前缀和` Icons.png`后缀。

如果单位名称不能这样对应，可以在`ra3autohander/fc_units.py`的`IMAGEPATHMAP`字典里面补充对应关系，该字典键为`UNITNAMES`中的单位名称去掉开头的阵营空格，该字典值为其在`images/nodes`下`Production`文件名（不带文件后缀）
举例如下，苏联起重机
其在`UNITNAMES`中的单位名称为`S Crane`，去掉开头的阵营空格为`Crane`，故`ra3autohander/fc_units.py`的`IMAGEPATHMAP`字典里它的键为`Crane`
其在其在`images/nodes`下`Production`文件名为`RA3 Crusher Crane Icons.png`，故故`ra3autohander/fc_units.py`的`IMAGEPATHMAP`字典里它的值为`RA3 Crusher Crane Icons`

b - 对于新增单位，还需要添加设置它的花费（建造价格和建造时间）
在`ra3autohander/replay_config.py`的`UNITCOST`添加单位id和单位花费，花费为由价格和时间组成的二元组

c - 对于新增单位，还需要设置他的类别，是建筑还是单位
如果是建筑，在`ra3autohander/fc_units.py`的`STRUCTURES`里添加其在`UNITNAMES`中设置的单位名称，
生产性建筑放在1中，防御性建筑放在2中。

如果是单位，根据单位的类别，在`ra3autohander/fc_units.py`的`UNITS`里对应类别中添加其在`UNITNAMES`中设置的单位名称。