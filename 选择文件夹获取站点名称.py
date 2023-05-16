# 弹出文件夹选择对话框，选择一个文件夹，获取包含子目录下的pdf文件，文件名使用正则"^(.*?)2023"匹配文本，得到站点，把站点和文件名使用pandas转换为Dataframe，并打印出来
# chatgpt回复
import tkinter as tk
from tkinter import filedialog
import os
import re
import pandas as pd

# 创建tkinter窗口并隐藏
root = tk.Tk()
root.withdraw()

# 弹出文件夹选择对话框
folder_path = filedialog.askdirectory()

# 获取文件夹中的所有PDF文件
pdf_files = []
for root_dir, _, file_list in os.walk(folder_path):
    for file_name in file_list:
        if file_name.endswith('.pdf'):
            pdf_files.append(os.path.join(root_dir, file_name))

# 使用正则匹配文件名
pattern = "^(.*?)2023"
matches = [re.match(pattern, os.path.basename(file_name)) for file_name in pdf_files]
sites = [match.group(1) if match else None for match in matches]
data = {'站点': sites, '文件名': pdf_files}

# 创建DataFrame
df = pd.DataFrame(data)

# 打印DataFrame
print(df)
