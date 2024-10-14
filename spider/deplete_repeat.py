import pandas as pd
# 读取CSV文件
df = pd.read_csv('tempData.csv')

# 去除重复数据（保留第一个出现的）
df_unique = df.drop_duplicates()



# 将处理后的数据写回CSV文件
df_unique.to_csv('tempData.csv', index=False)



