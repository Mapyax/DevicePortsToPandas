import pandas as pd
from Ivan import read_file, to_dict

def to_df(func: object) -> object:
    def wrapper(*args, **kwargs) -> object:
        global df
        dfdict = func(*args)
        df = pd.DataFrame(dfdict)
        df.to_csv('df.csv', index=False)
    return wrapper

@to_df
def to_dfdict(dict: dict) -> dict:
    dfdict = {'Hostname': [], 'Manufacturer': [], 'Port': [], 'Port type': [], 'Status port': [], 'Packets in': [], "Packets out": [], "Signal in": [], "Signal out": [], "Packets lost": [], "MAC-address": [], "IP": []}
    for port, value in dict['port_information'].items():
        dfdict['Hostname'].append(dict['hostname'])
        dfdict['MAC-address'].append(dict['device_info']['MAC-address'])
        dfdict['Manufacturer'].append(dict['device_info']['Manufacturer'])
        dfdict['Port'].append(port)
        dfdict['Port type'].append(dict['port_information'][port]['Port type'])
        dfdict['Signal in'].append(dict['port_information'][port]['Signal in'])
        dfdict['Signal out'].append(dict['port_information'][port]['Signal out'])
        if 'Packets in' in dict['port_information'][port]:
            if 'downlink ip' in dict['port_information'][port]:
                dfdict['IP'].append(dict['port_information'][port]['downlink ip'])
            else:
                dfdict['IP'].append(dict['port_information'][port]['Uplink ip'])
            dfdict['Status port'].append('Up')
            dfdict['Packets in'].append(dict['port_information'][port]['Packets in'])
            dfdict['Packets lost'].append(dict['port_information'][port]['Packets lost'])
            dfdict['Packets out'].append(dict['port_information'][port]['Packets out'])
        else:
            dfdict['IP'].append('NaN')
            dfdict['Status port'].append('Down')
            dfdict['Packets in'].append('NaN')
            dfdict['Packets lost'].append('NaN')
            dfdict['Packets out'].append('NaN')
    return dfdict

def main():
    filename = "Device_output.txt"
    text = read_file(filename)
    dict = to_dict(text)
    to_dfdict(dict)

if __name__ == "__main__":
    main()
    print(df)