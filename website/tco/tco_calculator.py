# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:05:58 2019

@author: Jonas Almeida dos Santos

Ferramenta para Cálculo de TCO da nuvem
"""
import configparser
import os


class CalculadoraTco:

    config = None
    base_dir = None

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(self.base_dir, 'dados.ini')
        self.config = configparser.ConfigParser()

        # leitura dos dados
        self.config.sections()
        self.config.read(config_file)
        self.config.sections()

    def calcular(self, memoria=64, HD=1000, nucleos=4):
        if memoria is None or memoria == '':
            memoria = 64

        if HD is None or HD == '':
            HD = 1000

        if nucleos is None or nucleos == '':
            nucleos = 4

        # Conversão dos dados em variaveis do tipo Float
        valor = self.config['DADOS']
        memoria = int(memoria)
        HD = int(HD)
        nucleos = int(nucleos)

        n_servidor = float(valor['nServidor'])
        c_servidor = float(valor['cServidor'])
        p_software_i = float(valor['pSoftwareI'])
        p_software_ii = float(valor['pSoftwareII'])
        p_software_iii = float(valor['pSoftwareIII'])
        ass_tipo_i = float(valor['assTipoI'])
        ass_tipo_ii = float(valor['assTipoII'])
        ass_tipo_iii = float(valor['assTipoIII'])
        n_software_i = float(valor['nSoftwareI'])
        n_software_ii = float(valor['nSoftwareII'])
        n_software_iii = float(valor['nSoftwareIII'])
        n_ni_cservidor = float(valor['nNICservidor'])
        nportas_nic = float(valor['nportasNIC'])
        p_switch = float(valor['pSwitch'])
        nporta_switch_rede = float(valor['nportaSwitchRede'])
        n_administrador_suporte = float(valor['nAdministradorSuporte'])
        tm_sistema_unidade_utilizado = float(valor['tmSistemaUnidadeUtilizado'])
        tg_sistema_inativo = float(valor['tgSistemaInativo'])
        n_classificacao_salario = float(valor['nClassificacaoSalario'])
        c_power_regiao = float(valor['cPowerRegiao'])
        potencia_unico_servidor = float(valor['potenciaUnicoServidor'])
        pue_medio = float(valor['pueMedio'])
        porcentagem_power_resfriamento = float(valor['porcentagemPowerResfriamento'])
        porcentagem_power_network = float(valor['porcentagemPowerNetwork'])
        carga_resfriamento = float(valor['cargaResfriamento'])
        k_redundancia_ar = float(valor['kRedundanciaAR'])
        k_ineficiencia = float(valor['kIneficiencia'])
        n_rack = float(valor['nRack'])
        p_intalacao_rack = float(valor['pIntalacaoRack'])
        c_quadrado_construir_cloud = float(valor['cQuadradoConstruirCloud'])
        pes_quadrado_rack = float(valor['pesQuadradoRack'])
        porcentagem_espaco_ocupado_rack = float(valor['porcentagemEspacoOcupadoRack'])
        peso_servidor = float(valor['pesoServidor'])
        peso_rack = float(valor['pesoRack'])
        unidade_amortizacao = float(valor['unidadeAmortizacao'])
        consumo_hora = float(valor['consumoHora'])

        # escolha da maquina e melhor ajuste de valores para calculo
        if memoria <= 64 and HD <= 1000 and nucleos <= 4:
            self.config.read(os.path.join(self.base_dir, 'PowerEdgeR240.ini'))
            valor1 = self.config['PowerEdge R240']

            n_servidor = memoria / 64 # densidade de VM
            c_servidor = float(valor1['cServidor'])
            n_ni_cservidor = float(valor1['nNICservidor'])
            potencia_unico_servidor = float(valor1['potenciaUnicoServidor'])
            carga_resfriamento = float(valor1['cargaResfriamento'])
            pes_quadrado_rack = float(valor1['pesQuadradoRack'])
            porcentagem_espaco_ocupado_rack = float(valor1['porcentagemEspacoOcupadoRack'])
            peso_servidor = float(valor1['pesoServidor'])
            peso_rack = float(valor1['pesoRack'])

        elif memoria <= 512 and HD <= 4000 and nucleos <= 22:
            self.config.read(os.path.join(self.base_dir, 'PowerEdgeR440.ini'))
            valor1 = self.config['PowerEdge R440']

            n_servidor = memoria/512 # densidade de VM
            c_servidor = float(valor1['cServidor'])
            n_ni_cservidor = float(valor1['nNICservidor'])
            potencia_unico_servidor = float(valor1['potenciaUnicoServidor'])
            carga_resfriamento = float(valor1['cargaResfriamento'])
            pes_quadrado_rack = float(valor1['pesQuadradoRack'])
            porcentagem_espaco_ocupado_rack = float(valor1['porcentagemEspacoOcupadoRack'])
            peso_servidor = float(valor1['pesoServidor'])
            peso_rack = float(valor1['pesoRack'])

        else :
            print('Erro de configuração')

        # chamando funções
        amortizacao = self.custo_amortizacao(unidade_amortizacao, consumo_hora)
        custoServidor = self.custo_servidor(n_servidor, c_servidor, amortizacao)
        custoNetwork = self.custo_network(n_servidor, n_ni_cservidor, nportas_nic, p_switch, nporta_switch_rede, amortizacao)
        custoSoftware = self.custo_software(p_software_i, p_software_ii, p_software_iii, ass_tipo_i, ass_tipo_ii, ass_tipo_iii, n_software_i, n_software_ii, n_software_iii, amortizacao)
        custoManutencao = self.custo_manutencao(n_servidor, n_administrador_suporte, tm_sistema_unidade_utilizado, tg_sistema_inativo, n_classificacao_salario)
        custoPower = self.custo_power(n_servidor, c_power_regiao, potencia_unico_servidor, pue_medio, consumo_hora, porcentagem_power_resfriamento, porcentagem_power_network)
        custoResfriamento = self.custo_resfriamento(custoPower, carga_resfriamento, k_redundancia_ar, k_ineficiencia)
        custoInstalacao = self.custo_instalacao(n_rack, p_intalacao_rack, amortizacao)
        custoImobiliario = self.custo_imobiliario(n_servidor, n_rack, c_quadrado_construir_cloud, pes_quadrado_rack, porcentagem_espaco_ocupado_rack, peso_servidor, peso_rack, amortizacao)
        custoTotal = self.custo_total(custoServidor, custoNetwork, custoSoftware, custoPower, custoManutencao, custoResfriamento, custoInstalacao, custoImobiliario)

        return {
            'type': 'Maquina Física',
            'cloud': 'Maquina Física',
            'cpu': nucleos,
            'hd': HD,
            'ram': memoria,
            'pricing': {
                'region': 'Goiania',
                'price': custoTotal
            }
        }

    # funçoes para cálculo de cada custo
    def custo_amortizacao(self, unidade_amortizacao, consumo_hora):
        n = 1.0 + 0.05
        custo = (n*consumo_hora) / unidade_amortizacao
        return custo

    def custo_servidor(self, n_servidor, c_servidor, amortizacao):
        custo = n_servidor * c_servidor * amortizacao
        return custo

    def custo_network(self, n_servidor, n_nic_servidor, nportas_nic, p_switch, nporta_switch_rede, amortizacao):
        n = n_nic_servidor * nportas_nic * (n_servidor/nporta_switch_rede)
        custo = n * p_switch * amortizacao
        return custo

    def custo_software(self, p_software1, p_software2, p_software3, ass_tipo1, ass_tipo2, ass_tipo3, n_software1, n_software2, n_software3, amortizacao):
        custo = (p_software1 * ass_tipo1 * n_software1 + p_software2 * ass_tipo2 * n_software2 +
                 p_software3 * ass_tipo3 * n_software3) * amortizacao
        return custo

    def custo_manutencao(self, n_servidor, n_administrador_suporte, tm_sistema_unidade_utilizado, tg_sistema_inativo, n_classificacao_salario):
        custo = n_administrador_suporte * (tm_sistema_unidade_utilizado * n_servidor + tg_sistema_inativo) * n_classificacao_salario
        return custo

    def custo_power(self, n_servidor, c_power_regiao, potencia_unico_servidor, pue_medio, consumo_hora, porcentagem_power_resfriamento, porcentagem_power_network):
        custo = (n_servidor * (potencia_unico_servidor / 1000) * c_power_regiao * pue_medio * consumo_hora) / (1 - porcentagem_power_resfriamento + porcentagem_power_network)
        return custo

    def custo_resfriamento(self, custo_power, carga_resfriamento, k_redundancia_ar, k_ineficiencia):
        custo = (carga_resfriamento * (1 + k_redundancia_ar) * custo_power) / k_ineficiencia
        return custo

    def custo_instalacao(self, n_rack, p_intalacao_rack, amortizacao):
        custo = n_rack * p_intalacao_rack * amortizacao
        return custo

    def custo_imobiliario(self, n_servidor, n_rack, c_quadrado_construir_cloud, pes_quadrado_rack, porcentagem_espaco_ocupado_rack, peso_servidor, peso_rack, amortizacao):
        a = (pes_quadrado_rack * n_rack) / porcentagem_espaco_ocupado_rack
        b = (n_servidor * peso_servidor + n_rack * peso_rack) / a
        custo = c_quadrado_construir_cloud * a * amortizacao * b
        return custo

    def custo_total(self, custo_servidor, custo_network, custosoftware, custopower, custo_manutencao, custo_resfriamento, custo_instalacao, custo_imobiliario):
        custo = custo_servidor + custo_network + custosoftware + custopower + custo_manutencao + custo_resfriamento + custo_instalacao + custo_imobiliario
        return custo

