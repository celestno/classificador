import csv
import random
import unicodedata
from faker import Faker
from datetime import timedelta

# --- CONFIGURAÇÕES ---
QTD_REGISTROS = 1000
ARQUIVO_CSV = "GerarGringo/dados_passaporte.csv"

fake = Faker('pt_BR')

def remover_acentos(texto):
    """Remove acentos: 'JOÃO' vira 'JOAO'"""
    if texto is None: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def gerar_mrz(sobrenome, nome, num_pass, nasc, sexo, validade):

    l1 = f"P<BRA{sobrenome.replace(' ', '<')}<<{nome.replace(' ', '<')}"
    l1 = l1[:44].ljust(44, '<').upper()
    
    nasc_clean = nasc.strftime("%y%m%d")
    val_clean = validade.strftime("%y%m%d")
    l2 = f"{num_pass}<7BRA{nasc_clean}8{sexo}{val_clean}<<<<<<<<<<<<<<"
    l2 = l2[:44].ljust(44, '<').upper()
    return l1, l2

def main():
    print(f"Gerando {QTD_REGISTROS} registros (SEM ACENTOS)...")
    
    with open(ARQUIVO_CSV, mode='w', newline='', encoding='utf-8') as f:
        campos = [
            "passaporte_num", "sobrenome", "nome", "data_nasc", "sexo",
            "naturalidade", "filiacao1", "filiacao2", "autoridade",
            "data_expedicao", "valido_ate", "mrz_linha1", "mrz_linha2", 
            "rg", "nome_assinatura"
        ]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()

        for i in range(QTD_REGISTROS):
            sexo = random.choice(['M', 'F'])
            
            raw_nome = fake.first_name_male() if sexo == 'M' else fake.first_name_female()
            nome = remover_acentos(raw_nome)
            
            raw_sobrenome = fake.last_name()
            sobrenome = remover_acentos(raw_sobrenome)
            
            nome_assinatura = f"{nome} {sobrenome}".title()

            dt_nasc = fake.date_of_birth(minimum_age=18, maximum_age=75)
            dt_exp = fake.date_between(start_date='-5y', end_date='today')
            dt_val = dt_exp + timedelta(days=365*10)
            num_pass = fake.bothify(text='??######').upper()
            
            mrz1, mrz2 = gerar_mrz(sobrenome, nome, num_pass, dt_nasc, sexo, dt_val)
            estado_sigla = fake.state_abbr()
            
            cidade_limpa = remover_acentos(fake.city().upper())
            
            filiacao1 = remover_acentos(fake.name().upper())
            filiacao2 = remover_acentos(fake.name().upper())

            escritor.writerow({
                "passaporte_num": num_pass,
                "sobrenome": sobrenome.upper(),
                "nome": nome.upper(),
                "data_nasc": dt_nasc.strftime("%d/%m/%Y"),
                "sexo": sexo,
                "naturalidade": f"{cidade_limpa}/{estado_sigla}",
                "filiacao1": filiacao1,
                "filiacao2": filiacao2,
                "autoridade": f"SR/PF/{estado_sigla}",
                "data_expedicao": dt_exp.strftime("%d/%m/%Y"),
                "valido_ate": dt_val.strftime("%d/%m/%Y"),
                "mrz_linha1": mrz1,
                "mrz_linha2": mrz2,
                "rg": fake.rg(),
                "nome_assinatura": nome_assinatura
            })

    print(f"✅ CSV recriado sem acentos!")

if __name__ == "__main__":
    main()
