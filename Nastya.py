import pandas as pd

df = pd.read_csv("df.csv")
print(df)

writer = pd.ExcelWriter('data_analysis.xlsx', engine='xlsxwriter')

# ..........................LIST 1................................
data_df1 = pd.DataFrame({
    'Hostname': df['Hostname'].tolist(),
    'Manufacturer': df['Manufacturer'].tolist(),
    'Port': df['Port'].tolist(),
    'Port type': df['Port type'].tolist(),
    'Status port': df['Status port'].tolist(),
    'MAC-address': df['MAC-address'].tolist(),
    'Number of available ports SC-APC': [''] * len(df),
    'Number of busy ports SC-APC': [''] * len(df),
    'Number of available ports SC-UPC': [''] * len(df),
    'Number of busy ports SC-UPC': [''] * len(df)
})

port_status_counts = df.groupby(['Port type', 'Status port'])['Port'].count()
print(port_status_counts)

available_ports1 = port_status_counts.get(('SC-APC', 'Up'), 0)
busy_ports1 = port_status_counts.get(('SC-APC', 'Down'), 0)
available_ports2 = port_status_counts.get(('SC-UPC', 'Up'), 0)
busy_ports2 = port_status_counts.get(('SC-UPC', 'Down'), 0)

data_df1.at[0, 'Number of available ports SC-APC'] = available_ports1
data_df1.at[0, 'Number of busy ports SC-APC'] = busy_ports1
data_df1.at[0, 'Number of available ports SC-UPC'] = available_ports2
data_df1.at[0, 'Number of busy ports SC-UPC'] = busy_ports2

# ..........................LIST 2................................
data_df2 = pd.DataFrame({
    'Hostname': df['Hostname'].tolist(),
    'Port': df['Port'].tolist(),
    'Manufacturer': df['Manufacturer'].tolist(),
    'MAC-address': df['MAC-address'].tolist(),
    'The highest signal level (Signal in)': [''] * len(df),
    'The lowest signal level (Signal in)': [''] * len(df),
    'Average signal strength (Signal in)': [''] * len(df),
    'The highest signal level (Signal out)': [''] * len(df),
    'The lowest signal level (Signal out)': [''] * len(df),
    'Average signal strength (Signal out)': [''] * len(df) 
})

data_df2.at[0, 'The highest signal level (Signal in)'] = df['Signal in'].max()
data_df2.at[0, 'The lowest signal level (Signal in)'] = df['Signal in'].min()
data_df2.at[0, 'Average signal strength (Signal in)'] = df['Signal in'].mean()

data_df2.at[0, 'The highest signal level (Signal out)'] = df['Signal out'].max()
data_df2.at[0, 'The lowest signal level (Signal out)'] = df['Signal out'].min()
data_df2.at[0, 'Average signal strength (Signal out)'] = df['Signal out'].mean()


# ..........................LIST 3................................
df[['IP']] = df[['IP']].fillna('-')

data_df3 = pd.DataFrame({
    'Hostname': df['Hostname'].tolist(),
    'Port': df['Port'].tolist(),
    'Manufacturer': df['Manufacturer'].tolist(),
    'MAC-address': df['MAC-address'].tolist(),
    'IP': df['IP'].tolist()
}) 

# ..........................LIST 4................................
df[['Packets in', 'Packets out', 'Packets lost']] = df[['Packets in', 'Packets out', 'Packets lost']].fillna(0)

data_df4 = pd.DataFrame({
    'Hostname': df['Hostname'].tolist(),
    'Port': df['Port'].tolist(),
    'Manufacturer': df['Manufacturer'].tolist(),
    'MAC-address': df['MAC-address'].tolist(),
    'Total packets in': [''] * len(df),
    'Total packets out': [''] * len(df),
    'Total packets lost': [''] * len(df)
})

data_df4.at[0, 'Total packets in'] = df['Packets in'].sum()
data_df4.at[0, 'Total packets out'] = df['Packets out'].sum()
data_df4.at[0, 'Total packets lost'] = df['Packets lost'].sum()

# ...............................................................

data_df1.to_excel(writer, sheet_name='Количество портов', index=False)
data_df2.to_excel(writer, sheet_name='Уровни сигналов', index=False)
data_df3.to_excel(writer, sheet_name='LLDP neighbors', index=False)
data_df4.to_excel(writer, sheet_name='Общее количество пакетов', index=False)

worksheet = writer.sheets['Количество портов']
worksheet.set_column('A:F', 15)
worksheet.set_column('G:J', 30)

worksheet = writer.sheets['Уровни сигналов']
worksheet.set_column('A:D', 20)
worksheet.set_column('E:K', 34)

worksheet = writer.sheets['LLDP neighbors']
worksheet.set_column('A:F', 20)

worksheet = writer.sheets['Общее количество пакетов']
worksheet.set_column('A:E', 20)
worksheet.set_column('F:H', 34)

writer._save()