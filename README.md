# files-manage
对文件分级整理，逐级建立文件夹，然后把符合的文件放入相应文件夹
使用chatgpt生成代码和改错，逐步测试实现需要的功能，测试步骤如下：

1、测试文件夹内文件名获取并测试正则是否能够提取关键文字（站点），最终确定正则是"^(.*?)2023"，使用该正则把读取的文件名提取出关键字（站点）

2、测试选择excel文件打开读取"所在地区"列，使用正则"^(.*州|.*市)"把所在地区分列成2列，一列为"州市"，一列为"县市"，把3列合并为pandas的DataFrame并打印输出

3、23年5月19日0点52分完成
4、整理作业PDF.py为最终版，添加撤销移动PDF文件功能。
