from netmiko import ConnectHandler
from openpyxl import Workbook

def obter_informacoes_ios(ip, username, password):
    # Definir as informações de conexão
    switch = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
    }

    # Conectar ao device
    try:
        net_connect = ConnectHandler(**switch)
    except Exception as e:
        print(f"Erro ao conectar ao device {ip}: {e}")
        return None

    # Obter a imagem do IOS
    try:
        output = net_connect.send_command('show version | include System image file')
        image = output.split('System image file is ')[-1].strip()

        # Fechar a conexão SSH
        net_connect.disconnect()

        return {'IP': ip, 'Imagem IOS': image}

    except Exception as e:
        print(f"Erro ao obter informações do device {ip}: {e}")
        return None


# Definir a lista de endereços IP
ips = ['10.100.48.12', '10.100.48.107', '10.100.48.254']

# Definir o nome de usuário e senha para se conectar aos switches
username = 'adilson.pedro'
password = 'salvador7572'


# Criar uma lista para armazenar as informações dos devices
devices_info = []

# Percorrer os endereços IP e obter as informações do IOS
for ip in ips:
    print(f"Conectando ao IP: {ip}")
    device_info = obter_informacoes_ios(ip, username, password)
    if device_info:
        devices_info.append(device_info)

# Criar um arquivo Excel e adicionar os dados
wb = Workbook()
ws = wb.active
ws.append(['IP', 'Imagem IOS'])

for device_info in devices_info:
    ws.append([device_info.get('IP', ''), device_info.get('Imagem IOS', '')])

# Salvar o arquivo Excel
filename = 'image_devices.xlsx'
wb.save(filename)

print(f"Dados salvos no arquivo: {filename}")
