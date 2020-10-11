## python实现红警三录像文件读取与自动分析生成流程图信息——一、简介
> 之前做了一个红警三的建造出兵流程图绘制工具
有评论建议说能不能够自动读取录像。
同时自己使用的时候，也感觉确实一点点手动绘制太过麻烦。
所以专门为该工具做了个自动录像读取分析工具。
技术路线：python3，未使用第三方库
github地址：[https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart](https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart)

## 总目录
## 一、简介
## 二、项目结构与代码初步介绍
## 三、代码细节介绍
======================= 大爽歌作，made by big shuang =======================

## 一、简介
### 1 - 工具使用介绍，
为了方便没有编程基础的朋友使用，我专门做了gui（可视化程序界面）并且打包成了exe，`主程序.exe`是中文版，`main.exe`是英文版
如果不喜欢运行陌生的exe，建议安装python3，命令行运行`main.py/main_zh/py`即可，
界面效果如图
![](https://img-blog.csdnimg.cn/20201007162941514.png)
选择录像文件后，界面效果如下图
![](https://img-blog.csdnimg.cn/20201007163013771.png)
此时在左侧玩家列表选择一名玩家，点击右边的按钮，即可导出对应信息
其中
- 导出流程图信息按钮，用于导出流程图信息json文件（复制该json文件到之前的流程图绘制页面的加载页面，即可自动生成流程图）
- 导出所有命令信息，用于导出录像本身解析出来的所有命令json文件，给文件主要是方便对录像文件解码感兴趣的人研究使用。

### 2 - 工具使用限制
*以下问题不是短时间能够解决的，所以只能先避免这些情况了*
- 1 - 不支持帝国阵营
- 2 - 不支持地图自带多基地或者除基地外有其他出兵建筑的录像。
- 3 - 不支持玩家占领敌人建筑出兵的录像
- 4 - 不能保证流程图信息导出完全准确

原因说明：红警三录像文件其实基本只保存玩家的操作，而基本不保存状态，
很多信息里面是没有的， 比如单位什么时候建好，建好后的单位的id是多少，玩家什么时候卡钱，什么时候卡电。
所以流程图里面的一些信息，是我在代码里根据一定的规则来猜的。
目前只能说大体上没有什么问题，八九不离十。
但如果对准确度要求很高，只能后期手动矫正。

### 3 - 特别鸣谢
- 首先感谢岚依老哥评论推荐的 KWReplayAutoSaver

- 同时也非常感谢KWReplayAutoSaver的作者forcecore。这好像还是个韩国老哥。
KWReplayAutoSaver的github页面：[https://github.com/forcecore/KWReplayAutoSaver](https://github.com/forcecore/KWReplayAutoSaver)
这个刚好是用我熟悉的python写的，所以研究起来也比较顺手。
这里面实现了红警三录像的读取和一些基本的命令的解析，
极大的节省了我的时间。

- 最后感谢远古大佬R Schneider
KWReplayAutoSaver里的录像格式解码，也是归功于gamereplays.org社区的一个远古大佬R Schneider的作品
其对应的github是
[https://github.com/louisdx/cnc-replayreaders](https://github.com/louisdx/cnc-replayreaders)
这个可以说是目前大多数红警三录像解析工具的源头了
虽然这个使用c语言写的，但是这位远古老哥为这个工具写了一个详细的文档。html格式的，用浏览器打开即可