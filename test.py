def str_to_slice(slice_str):
    # 去除方括号
    slice_str = slice_str.strip('[]')
    
    # 分割字符串以提取起始、结束和步长
    parts = slice_str.split(':')
    
    # 根据部分的数量创建切片
    if len(parts) == 1:
        # 如果只有一个部分，则视为结束位置，开始默认为 None
        return slice(None, int(parts[0]), None)
    elif len(parts) == 2:
        # 如果有两个部分，则视为开始和结束位置
        start = None if parts[0] == '' else int(parts[0])
        stop = None if parts[1] == '' else int(parts[1])
        return slice(start, stop, None)
    elif len(parts) == 3:
        # 如果有三个部分，则视为开始、结束和步长
        start = None if parts[0] == '' else int(parts[0])
        stop = None if parts[1] == '' else int(parts[1])
        step = None if parts[2] == '' else int(parts[2])
        return slice(start, stop, step)
    else:
        raise ValueError("Invalid slice string format")

t2c = {
    '[:1]': '#3174f0',
    '[1:2]': '#e53125',
    '[2:3]': '#fbb003',
    '[3:4]': '#3174f0',
    '[4:5]': '#269a43',
    '[5:]': '#e53125',
}

# 将字符串键转换为切片
t2c_slices = {str_to_slice(key): value for key, value in t2c.items()}
print(t2c_slices)