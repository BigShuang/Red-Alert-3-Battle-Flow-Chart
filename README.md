# Red-Alert-3-Battle-Flow-Chart

[View in Chinese(查看中文版说明)](https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart/blob/master/README_ZH.md)


- 使用`ra3autohander\主程序.exe`可自动读取录像文件信息，导出流程图信息


## Version 1.1 is complete(No detailed testing)
**New function: automatic video reading**
- A tool to draw flow chart for ra3 battle
Open main.html in your browser(Chrome is recommended), then you can draw.
- `ra3autohander\main.exe` can automatically read video file information and export flow chart information.If you have installed python3(No need to install any third-party libraries), run `ra3autohander\main.py` does the same thing.

#### The flow chart drawing effect is as follows:
![](https://github.com/BigShuang/Red-Alert-3-Battle-Flow-Chart/blob/master/output/BV1GE411r79W_3_ps.png)

The video corresponding to this chart is [BV1GE411r79W](https://www.bilibili.com/video/BV1GE411r79W)

## FAQ
- **How to export the chart after drawing?**

I haven't implemented the image export function, but you can use the screenshot API provided by chrome to take screenshots as follows:
In chrome, Ctrl + Shift + I open devtools.
In devtools, Ctrl + Shift + P opens the command menu.
Enter `screenshot` in the command menu.
Click `capture full size screenshot` to complete the screenshot.

## Progress description
- 2020-9-4
Verson 1.0 of the project will be completed in two weeks.
- 2020-9-10
 Version 1.0 is complete(No detailed testing)
- 2020-9-30
 Version 1.1 is complete(No detailed testing)
 `ra3autohander\main.exe` can automatically read video file information and export flow chart information.If you have installed python3(No need to install any third-party libraries), run `ra3autohander\main.py` does the same thing.
 Current restrictions:
1 - Not support the imperial camp.
2 - Not support replay that uses map starting with multi construction yards or other production building that can produce units except the main construction yard.
3 - Not support video of players occupying enemy buildings producing units.