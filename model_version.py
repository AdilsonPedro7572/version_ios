from netmiko import ConnectHandler
from tabulate import tabulate

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
ips = ['10.104.48.12', '10.104.48.107', '10.104.48.254']

# Definir o nome de usuário e senha para se conectar aos switches
username = 'adilson.pedro'
password = 'salvador7572'

# Criar uma lista para armazenar as informações dos switches
devices_info = []

# Percorrer os endereços IP e obter as informações do IOS
for ip in ips:
    print(f"Conectando ao IP: {ip}")
    switch_info = obter_informacoes_ios(ip, username, password)
    if switch_info:
        devices_info.append(switch_info)

# Exibir a tabela com o resultado final
headers = ['IP', 'Imagem IOS']
table_data = [[info.get('IP', ''), info.get('Imagem IOS', '')] for info in devices_info]
print(tabulate(table_data, headers=headers, tablefmt='grid'))
