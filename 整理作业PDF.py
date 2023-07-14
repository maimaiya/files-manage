# Encoding: utf-8
# 生成一段Python程序，要求如下：
# 1、界面大小350*300，添加一个标签1，显示文字是表头，右侧添加一个文本框1，默认文字是运维单位，下一行添加一个标签2，显示文字是筛选值，右侧添加一个文本框2，默认文字是南方电网云南电动汽车服务有限公司，添加一个按钮1，显示文字是选取需要筛选的文件，添加一个单选框，单选框前添加标签，未选中时显示文字是从表格筛选，选中单选框后显示文字变为单条件，同时隐藏标签1、文本框1、标签2、文本框2、按钮1，添加一个标签3，显示文字是请输入需要筛选德表头，右侧添加一个文本框3，标签3正下方添加一个标签4，显示文字是请输入需要筛选的文件的表头，右侧添加一个文本框4，添加3个按钮，显示文字分别是选取筛选条件文件、选取需要筛选的文件、开始筛选，取消选中单选框后，隐藏标签3、文本框3、标签4、文本框4及3个按钮；
# 2、按钮单击事件a、选取需要筛选的文件被单击时，弹出文件选择对话框，选取excel文件(xlsx、xls、csv)，读取选取的文件，从文本框1中获取内容，在读取的文件中筛选表头是该内容的列，筛选条件从文本框2中获取，并把筛选后的结果保存到相同目录下，文件名是原文件名+_已筛选；
# 3、按钮单击事件b、选取筛选条件文件被单击时，弹出文件选择对话框，选取excel文件(xlsx、xls、csv)，读取文件赋值给筛选条件；选取需要筛选的文件被单击时，弹出文件选择对话框，选取excel文件(xlsx、xls、csv)，读取文件转换为Dataframe，赋值给总表；开始筛选被单击时，获取文本框3中内容，存为条件表头，获取文本框4内容，存为待匹配表头，从筛选条件中读取表头是条件表头的列作为筛选条件，总表中表头是待匹配表头列中符合筛选条件的，整行保存到Dataframe_已筛选，最后把Dataframe_已筛选保存为excel文件，文件名是原文件名+_已多项筛选


"""
写python代码，要求如下：
1、创建UI，3个按钮，名称是分别是选取需要筛选条件、选择待整理文件夹、开始筛选、撤销移动；
2、单击按钮1，弹出文件选择对话框，选取excel文件(xlsx、xls、csv)，读取文件中"资产单位"列、"所在地区"列、"站点名称"列，"所在地区"列使用正则(^(.*州|.*市))分成2列，一列为"州市"，一列为"县市"，并把"站点名称"列、"资产单位"列、"州市"列、"县市"列保存到Dataframe，然后对Dataframe中"资产单位"列开头的字符是"云南电网有限责任公司"的替换为"云南电网"，开头是"南方电网云南电动"的替换为"云南电动",保存Dataframe到源文件目录下，文件名是源文件名+_Dataframe；
3、单击按钮2，选取一个文件夹;
4、单击按钮3，获取选取的文件夹下所有pdf文件，使用正则(^(.*?)2023)获取文件名中"2023"前面的字符，查询Dataframe中"站点名称"列，获取对应的"资产单位"列、"州市"列、"县市"列，作为文件夹名称，按照"资产单位"为第一级目录，"州市"为第二级目录,"县市"第三级目录的层级关系，检查文件夹是否存在，不存在则创建文件夹，把pdf文件移动到第三级的文件夹中；
5、单击按钮4，获取选取的文件夹子目录下所有匹pdf文件，把子目录下所有pdf文件移动到选取的文件夹下；
有部分错误，未完全依靠GPT-3生成，需要修改，但是使用NewBing一次生成，没有bug
"""

import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

import pandas as pd

filter_path = ""
folder_path = ""
filter_file_path = ""


def select_filter_condition():
    global filter_path
    global filter_file_path
    filter_file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv")])

    if filter_file_path:
        filter_path = filter_file_path
        print("选择筛选条件文件成功！")
    else:
        print("未选择筛选条件文件！")


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()

    if folder_path:
        print("选择文件夹成功！")
    else:
        print("未选择文件夹！")


def start_move():
    if not filter_path or not folder_path:
        print("未选择筛选条件文件或文件夹！")
        return

    df_filter = pd.read_excel(filter_path, sheet_name="Sheet1") if filter_path.endswith(
        ('.xlsx', '.xls')) else pd.read_csv(filter_path)
    # 读取站点名称列、资产单位列、所在地区列
    df_filter = df_filter[["站点名称", "资产单位", "所在地区"]].copy()
    # 替换"资产单位"列字符，开头是云南电网的整个单元替换成云南电网，开头是南方电网云南电动的整个单元替换成云南电动
    df_filter['资产单位'] = df_filter['资产单位'].apply(
        lambda x: '云南电网' if x.startswith('云南电网') else ('云南电动' if x.startswith('南方电网云南电动') else x))
    # 保存Dataframe到源文件目录下
    filter_folder_path = os.path.dirname(filter_path)
    df_filter.to_excel(os.path.join(filter_folder_path, filter_file_path + '_Dataframe.xlsx'), index=False)
    pdf_files = []
    for root_dir, _, file_list in os.walk(folder_path):
        for file_name in file_list:
            if file_name.endswith('.pdf'):
                pdf_files.append(os.path.join(root_dir, file_name))

    for file in pdf_files:
        file_name = os.path.basename(file)
        pattern = "^(.*?)2023"
        match = re.match(pattern, file_name)
        if match:
            site = match.group(1)
            result = df_filter.loc[df_filter['站点名称'] == site, ['所在地区']]
            ower = df_filter.loc[df_filter['站点名称'] == site, ['资产单位']]
            if not result.empty:
                location = result.iloc[0]['所在地区']
                ower = ower.iloc[0]['资产单位']
                match = re.match(r'(.*?[州市]).*?[县市]', location)
                if match:
                    state = match.group(1)
                    county = location.replace(state, '')
                    ower_folder = os.path.join(folder_path, ower)
                    state_folder = os.path.join(ower_folder, state)
                    county_folder = os.path.join(state_folder, county)


                    if not os.path.exists(ower_folder):
                        os.makedirs(ower_folder)
                    if not os.path.exists(state_folder):
                        os.makedirs(state_folder)
                    if not os.path.exists(county_folder):
                        os.makedirs(county_folder)

                    dest_path = os.path.join(county_folder, file_name)
                    shutil.move(file, dest_path)

    print("文件移动完成。")

def move_pdf_files():
    # 打开文件对话框，选择目录
    selected_directory = filedialog.askdirectory(title="选择目录")

    # 遍历所选目录下的所有子文件夹
    for root, dirs, files in os.walk(selected_directory):
        for file in files:
            if file.endswith(".pdf"):
                # 构造源文件路径和目标文件路径
                source_path = os.path.join(root, file)
                destination_path = os.path.join(selected_directory, file)

                # 移动文件到目标目录
                shutil.move(source_path, destination_path)

    print("移动完成！")

# 创建UI
root = tk.Tk()
root.title("文件筛选工具")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

button1 = tk.Button(frame, text="选取需要筛选条件", command=select_filter_condition)
button1.pack(fill=tk.X, padx=10, pady=5)

button2 = tk.Button(frame, text="选择待整理文件夹", command=select_folder)
button2.pack(fill=tk.X, padx=10, pady=5)

button3 = tk.Button(frame, text="开始筛选", command=start_move)
button3.pack(fill=tk.X, padx=10, pady=5)

button4 = tk.Button(frame, text="撤销移动，我要手动", command=move_pdf_files)
button4.pack(fill=tk.X, padx=10, pady=5)

dataframe = None
selected_folder = None

root.mainloop()
