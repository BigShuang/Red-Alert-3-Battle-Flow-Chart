# Red-Alert-3-Battle-Flow-Chart

## 1.1 版本已完成（未详细测试）
**新增功能：自动读取录像**

【红警三】建造出兵流程图制作工具——基于jquery实现
- 用浏览器（推荐chromw）打开 主页.html 即可开始绘制
- 使用`ra3autohander\主程序.exe`可自动读取录像文件信息，导出流程图信息;
 如果你安装了python3（无需安装任何第三方库），也可以运行`ra3autohander\main_zh.py`, 效果一样。


#### 流程图绘制效果如下：
![](https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart/blob/master/output/BV1GE411r79W_3_ps.png)

对应的录像视频是[BV1GE411r79W](https://www.bilibili.com/video/BV1GE411r79W)


## 常见问题
- **绘制完成后如何截图?**
  
我没有实现图片导出功能，不过你可以用chrome自带的截图api来截图，方法如下:
在chrome中, CTRL+SHIFT+I 打开开发者工具（DevTools）,
在开发者工具（DevTools）中，CTRL+SHIFT+P打开命令菜单（Command Menu）,
在命令菜单中输入 screenshot,
单击capture full size screenshot即完成截图。


## 进度时间表
- 2020-9-4
已经做好了大部分了，还有些也是很重要的功能要补充，预计这两周内应该就能好。
具体见[record_1_0.md](https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart/blob/master/docs/record_1_0.md), 如果你在看我的直播的话，推荐看下这个，你就能知道我当前和接下来大概在干啥
- 2020-9-10
 1.0 版本已完成（未详细测试）
- 2020-9-30
 1.1 版本已完成（未详细测试）
 ra3autohander\主程序.exe 可自动读取录像文件信息，导出流程图信息
 如果你安装了python3（无需安装任何第三方库），也可以运行`ra3autohander\main_zh.py`, 效果一样。
 目前限制：
 1 - 不支持帝国阵营
 2 - 不支持地图自带多基地或者除基地外有其他出兵建筑的录像。
 3 - 不支持玩家占领敌人建筑出兵的录像