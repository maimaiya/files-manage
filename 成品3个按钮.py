# 提问chatgpt：1、创建一个窗口程序，有2个按钮（选择筛选条件、选择文件夹），2、单击筛选条件弹出文件选择对话框，选择一个excel文件(xlsx、xls、csv)，读取这个文件中"所在地区"、"站点名称"两列，使用正则("^(.*州|.*市)")把"所在地区"列分成2列，然后把3列用pandas转为DataFrame，第一列是"站点名称"，然后是"州市"、"县市"，3、单击"选择文件夹"后弹出对话框选择一个文件夹，获取该目录下所有PDF文件，保存列表备用，使用正则(^(.*?)2023)提取每一个文件名中的字符，在DataFrame中查询这个字符对应的"州市"、"县市"名称，检查pdf目录下是否存在对应州市文件夹，不存在则创建，然后在对应州市文件夹下查询是否存在对应县市文件夹，不存在则创建，然后把原pdf文件移动懂对应县市文件夹下。
# 在提问chatgpt：修改：在转换为DataFrame后添加保存到pdf目录，名称是筛选条件文件.xlsx
# 创建：maimaiya
# 编写：chatgpt3.5
# 调试:maimaiya
# 测试:maimaiya
# 测试结果：有2个文件未移动，原因是1、站点名称不一致；2、有个站点在表格中没有
# 再增加一个按钮(开始移动)，点击选择筛选条件后仅弹出对话框和选取文件，点击选择文件夹后仅选取文件夹，点击开始移动后实现所有功能，窗口界面大小300*300,报错信息已经修复

import tkinter as tk
from tkinter import filedialog
import os
import re
import pandas as pd
import shutil

filter_path = ""
folder_path = ""


def select_filter_condition():
    global filter_path
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

    df_filter = pd.read_excel(filter_path,sheet_name="Sheet1") if filter_path.endswith(('.xlsx', '.xls')) else pd.read_csv(filter_path)

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
            if not result.empty:
                location = result.iloc[0]['所在地区']
                match = re.match(r'(.*?[州市]).*?[县市]', location)
                if match:
                    state = match.group(1)
                    county = location.replace(state, '')
                    state_folder = os.path.join(folder_path, state)
                    county_folder = os.path.join(state_folder, county)

                    if not os.path.exists(state_folder):
                        os.makedirs(state_folder)
                    if not os.path.exists(county_folder):
                        os.makedirs(county_folder)

                    dest_path = os.path.join(county_folder, file_name)
                    shutil.move(file, dest_path)

    print("文件移动完成。")


root = tk.Tk()
root.geometry("300x300")

filter_button = tk.Button(root, text="选择筛选条件", command=select_filter_condition)
filter_button.pack()

folder_button = tk.Button(root, text="选择文件夹", command=select_folder)
folder_button.pack()

start_button = tk.Button(root, text="开始移动", command=start_move)
start_button.pack()

root.mainloop()
