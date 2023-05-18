# 提问chatgpt：1、创建一个窗口程序，有2个按钮（选择筛选条件、选择文件夹），2、单击筛选条件弹出文件选择对话框，选择一个excel文件(xlsx、xls、csv)，读取这个文件中"所在地区"、"站点名称"两列，使用正则("^(.*州|.*市)")把"所在地区"列分成2列，然后把3列用pandas转为DataFrame，第一列是"站点名称"，然后是"州市"、"县市"，3、单击"选择文件夹"后弹出对话框选择一个文件夹，获取该目录下所有PDF文件，保存列表备用，使用正则(^(.*?)2023)提取每一个文件名中的字符，在DataFrame中查询这个字符对应的"州市"、"县市"名称，检查pdf目录下是否存在对应州市文件夹，不存在则创建，然后在对应州市文件夹下查询是否存在对应县市文件夹，不存在则创建，然后把原pdf文件移动懂对应县市文件夹下。
# 在提问chatgpt：修改：在转换为DataFrame后添加保存到pdf目录，名称是筛选条件文件.xlsx
# 创建：maimaiya
# 编写：chatgpt3.5
# 调试:maimaiya
# 测试:maimaiya
# 测试结果：有2个文件未移动，原因是1、站点名称不一致；2、有个站点在表格中没有


import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

import pandas as pd

file_path = ""


def select_filter_condition():
    # 弹出文件选择对话框，选择Excel文件
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv")])

    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path, sheet_name="Sheet1") if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(
        file_path)

    # 提取"所在地区"和"站点名称"两列数据
    data = df[["所在地区", "站点名称"]].copy()

    # 使用正则表达式将"所在地区"分成两个字符串
    data["州市"] = data["所在地区"].apply(lambda x: re.findall(r"^(.*州|.*市)", str(x))[0])
    data["县市"] = data["所在地区"].apply(lambda x: re.sub(r"^(.*州|.*市)", "", str(x)))

    # 创建新的DataFrame
    new_df = pd.DataFrame({
        "站点名称": data["站点名称"],
        "县市": data["县市"],
        "州市": data["州市"]

    })

    # 保存筛选条件DataFrame为Excel文件
    output_file = os.path.join(os.path.dirname(file_path), '筛选条件文件.xlsx')
    new_df.to_excel(output_file, index=False)
    # 输出DataFrame
    print(new_df)


def select_folder():
    # 弹出文件夹选择对话框，选择文件夹
    folder_path = filedialog.askdirectory()

    # 获取文件夹中的所有PDF文件
    pdf_files = []
    for root_dir, _, file_list in os.walk(folder_path):
        for file_name in file_list:
            if file_name.endswith('.pdf'):
                pdf_files.append(os.path.join(root_dir, file_name))

    # 加载筛选条件DataFrame
    filter_df = pd.read_excel(os.path.join(os.path.dirname(folder_path), '筛选条件文件.xlsx'))

    # 遍历PDF文件，提取州市和县市信息，移动文件到对应的文件夹
    for file in pdf_files:
        file_name = os.path.basename(file)
        pattern = "^(.*?)2023"
        match = re.match(pattern, file_name)
        if match:
            site = match.group(1)
            # 查询对应州市和县市
            result = filter_df.loc[filter_df['站点名称'] == site, ['州市', '县市']]
            if not result.empty:
                state = result.iloc[0]['州市']
                county = result.iloc[0]['县市']
                state_folder = os.path.join(folder_path, state)
                county_folder = os.path.join(state_folder, county)

                # 检查并创建州市文件夹和县市文件夹
                if not os.path.exists(state_folder):
                    os.makedirs(state_folder)
                if not os.path.exists(county_folder):
                    os.makedirs(county_folder)

                # 移动PDF文件到对应县市文件夹下
                dest_path = os.path.join(county_folder, file_name)
                shutil.move(file, dest_path)

    print("文件移动完成。")


# 创建tkinter窗口
root = tk.Tk()

# 创建选择筛选条件按钮
filter_button = tk.Button(root, text="选择筛选条件", command=select_filter_condition)
filter_button.pack()

# 创建选择文件夹按钮
folder_button = tk.Button(root, text="选择文件夹", command=select_folder)
folder_button.pack()

# 运行窗口程序
root.mainloop()
