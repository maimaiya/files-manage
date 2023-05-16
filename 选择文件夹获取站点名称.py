
# 弹出对话框选择文件夹
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

# 获取所有文件名
file_list = []
for root_folder, sub_folders, files in os.walk(folder_path):
    for file in files:
        file_list.append(file)

# 使用正则^(.*?)2023匹配文件名
pattern = '^(.*?)2023'
for file_name in file_list:
    match = re.search(pattern, file_name)
    if match:
        print(f"文件名：{file_name}，匹配结果：{match.group(1)}")
    else:
        print(f"文件名：{file_name}，无匹配结果")
