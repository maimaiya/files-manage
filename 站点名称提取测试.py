import re
import tkinter as tk
from tkinter import filedialog

import pandas as pd

# 创建Tkinter根窗口
root = tk.Tk()
root.withdraw()

# 弹出文件选择对话框，选择Excel文件
file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv")])

# 使用pandas读取Excel文件
df = pd.read_excel(file_path, sheet_name="Sheet1") if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)

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

# 输出DataFrame
print(new_df)
