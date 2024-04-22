import pprint


def read_file(filename: str) -> list[str]:
    with open(filename, "r") as file:
        full_text = file.read().split("\n\n")[1:-2]
        return full_text


def split_data(text: list[str]) -> tuple[str, list[str], list[str]]:
    """Writes data in global scope vision"""
    # TODO зарезолвить, что это блок хостнейма, а потом пихать в дикт
    hostname = text[0].split('\n')[1]
    # TODO зарезолвить, что это блок инфы о устройстве
    device_data = text[1].split('\n')[1:]
    # TODO зарезолвить, что это блок инфы о портах
    port_info = text[2].split('\n')
    return hostname, device_data, port_info


def to_dict(text: list[str]) -> dict:
    tmp_dict = {}
    sub_dict = {}

    hostname, device_data, port_info = split_data(text)

    tmp_dict["hostname"] = hostname

    for item in device_data:
        item = item.split(": ")
        sub_dict[item[0]] = item[1]

    tmp_dict["device_info"] = sub_dict
    sub_dict = {}
    current_port = None

    for line in port_info:
        if line.startswith("Up-link port:") or line.startswith("Port"):
            port_name = line.split(":")[0].strip()
            sub_dict[port_name] = {}
            current_port = port_name
        elif current_port:
            key, value = line.split(":", 1)
            value = value.split(" ")
            sub_dict[current_port][key.strip()] = value[1]

    tmp_dict["port_information"] = sub_dict

    return tmp_dict


def main():
    filename = "Device_output.txt"
    text = read_file(filename)
    output_dict = to_dict(text)


if __name__ == "__main__":
    main()