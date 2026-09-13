
# Converte IP em string para um numero inteiro
def ip_para_inteiro(ip):
    octetos = ip.split('.')
    resultado = 0
    for octeto in octetos:
        resultado = (resultado << 8) | int(octeto)
    return resultado

# Faz o inverso: inteiro para IP em string
def inteiro_para_ip(n):
    partes = []
    for _ in range(4):
        partes.append(str(n & 0xFF))
        n >>= 8
    return '.'.join(reversed(partes))

# Calcula a mascara a partir do prefixo (/24, /25, etc)
def calc_mascara(prefixo):
    return (0xFFFFFFFF << (32 - prefixo)) & 0xFFFFFFFF

# Acha a quantidade de bits pra caber os hosts (descontando rede e broadcast)
def bits_necessarios(qtd_hosts):
    n = 1
    while (2 ** n - 2) < qtd_hosts:
        n += 1
    return n

# Funcao principal pra calcular a sub-rede
def alocar_rede(ip_inicio, qtd_hosts):
    bits = bits_necessarios(qtd_hosts)
    prefixo = 32 - bits
    
    mascara = calc_mascara(prefixo)
    rede = ip_inicio & mascara
    broadcast = rede | (~mascara & 0xFFFFFFFF)

    return {
        'rede': inteiro_para_ip(rede),
        'mascara': inteiro_para_ip(mascara),
        'prefixo': prefixo,
        'broadcast': inteiro_para_ip(broadcast),
        'primeiro_ip': inteiro_para_ip(rede + 1),
        'ultimo_ip': inteiro_para_ip(broadcast - 1),
        'proximo': broadcast + 1
    }

def main():
    bloco_ip = '172.20.10.0'
    prefixo_bloco = 23

    # Calcula o limite do bloco principal pra validacao
    masc_bloco = calc_mascara(prefixo_bloco)
    rede_bloco = ip_para_inteiro(bloco_ip) & masc_bloco
    bcast_bloco = rede_bloco | (~masc_bloco & 0xFFFFFFFF)

    # Exigencias do projeto (ordenado do maior pro menor - VLSM)
    departamentos = [
        ('Engenharia', 120),
        ('Financeiro', 50),
        ('Marketing', 28),
        ('Visitantes', 10),
    ]

    letras = ['A', 'B', 'C', 'D']
    ip_atual = rede_bloco

    for i in range(len(departamentos)):
        nome = departamentos[i][0]
        demanda = departamentos[i][1]
        letra = letras[i]

        sub = alocar_rede(ip_atual, demanda)

        # Verifica se a rede passou do limite do bloco /23
        ip_rede = ip_para_inteiro(sub['rede'])
        ip_bcast = ip_para_inteiro(sub['broadcast'])
        
        if ip_rede < rede_bloco or ip_bcast > bcast_bloco:
            print(f"\nDeu erro: O bloco estourou na rede {nome}!")
            break

        print(f"\nSub-rede {letra} ({nome}):")
        print(f"Network Address: {sub['rede']}")
        print(f"Subnet Mask: {sub['mascara']}")
        print(f"CIDR: /{sub['prefixo']}")
        print(f"Broadcast: {sub['broadcast']}")
        print(f"Usable IPs: {sub['primeiro_ip']} - {sub['ultimo_ip']}")

        # Prepara o inicio da proxima rede (1 IP depois do broadcast atual)
        ip_atual = sub['proximo']

if __name__ == '__main__':
    main()