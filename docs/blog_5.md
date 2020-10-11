## python实现红警三录像文件读取与自动分析生成流程图信息——二、项目结构与代码初步介绍

## 总目录
## 一、简介
## 二、项目结构与代码初步介绍
## 三、代码细节介绍
======================= 大爽歌作，made by big shuang =======================

## 二、项目结构与代码初步介绍
### 1 - 文件夹介绍
- `ra3autohander/`: 存放该自动分析工具所有相关的python代码
- `replays/`: 存放示例用的录像文件和分析后的json文件
- `ra3autohander/build/`和`ra3autohander/dist/`: 打包python文件成exe时生成的，基本不用去管

### 2 - 文件介绍
- `ra3autohander/main_zh.py`和`ra3autohander/main.py`: 主程序，（工具运行入口），前者是中文版，后者是英文版
- `ra3autohander/主程序.exe`和`ra3autohander/main.exe`: 主程序py文件打包成的exe文件，前者是中文版，后者是英文版

- `ra3autohander/gui.py`: 实现了可视化界面，供`main_zh.py`和`main.py`调用，文件本身则是调用了`hander.py`文件进行的录像的读取和解析
- `ra3autohander/hander.py`: 对录像文件读取分析并导出成需要的json文件功能封装成几个可供`gui.py`的方法，具体的录像读取功能则是调用更底层的`ra3replay.py`来实现，导出流程图信息则是基于`flowchart.py`来实现
- `ra3autohander/flowchart.py`: 对初步解析后的录像进行进一步分析，并格式化为流程图json
- `ra3autohander/fc_units.py`: 实现了流程图解析需要的基础节点类，存放流程图的配置变量

**以下文件实现了对红警三录像文件的读取与解析**
- `ra3autohander/ra3replay.py`: 实现了对红警三录像的读取与解析
的类 `KWReplayWithCommands`和对红警三录像主体（body）内容的解析类`ReplayBody`
- `ra3autohander/kwreplay.py`: 实现了`KWReplayWithCommands`类的父类`KWReplay`（该类本来是用于解析凯恩的愤怒的），也实现了解析录像玩家数据信息的类`Player`
- `ra3autohander/ra3chunks.py`: 实现了`ReplayBody`的基础单元chunk（可以理解为数据块）的解析类`RA3Chunk`
- `ra3autohander/chunks.py`: 实现了`RA3Chunk`类的父类`Chunk`和对基础单元chunk（可以理解为数据块）中的命令的解析类`Command`
- `ra3autohander/replay_config.py`: 存放录像文件配置信息，比如一些命令对应的16进制码，一些单位对应的16进制码

### 3 - 红警三录像文件格式简要介绍
红警三录像文件，后缀名为`RA3Replay`，该文件由16进制码编写
分为录像头（head），录像主体（body），录像尾（footer）
- 录像头一般记录地图信息和玩家初始信息，比如阵营队伍颜色
- 录像体（body）由数据块（chunk）组成，每个数据块内包含0到多个命令（command），每个命令都有一个命令id——cmd_id，为两位16进制码，目前已解析出具体意义的cmd_id存放在`replay_config.py`的`BO_COMMANDS`，具体对应意义存放在`replay_config.py`的`CMDNAMES`中。
- 录像尾暂未研究，应该没记录啥重要信息
