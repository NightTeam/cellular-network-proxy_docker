import subprocess

from jinja2 import Template


def get_nic_list():
    nic_list = subprocess.check_output("ls /dev/ttyUSB*", shell=True).decode()
    nic_list = nic_list.split("\n")
    nic_list.remove("")

    return nic_list


def generate():
    template = Template(open("docker-compose_temp.j2").read())
    nic_list = get_nic_list()
    nic_total_num = int(len(nic_list) / 4)

    nics = [{"num": num, "tty_usb_num": (num + 1) * 4 - 1} for num in range(nic_total_num)]
    text = template.render(nics=nics)
    with open("docker-compose.yml", "w") as f:
        f.write(text)


if __name__ == '__main__':
    generate()
