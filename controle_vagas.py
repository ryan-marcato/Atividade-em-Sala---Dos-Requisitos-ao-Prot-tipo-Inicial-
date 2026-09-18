"""
Protótipo: Controle de vagas de estacionamento em tempo real via sensores.

Requisito:
    Cada vaga possui um sensor de presença. Quando o sensor detecta a entrada
    ou saída de um veículo, o status da vaga deve ser atualizado em tempo real
    e refletido no painel de controle do estacionamento.

Este protótipo simula os sensores usando uma thread separada que dispara
eventos aleatórios de ocupação/liberação, como aconteceria com hardware real
enviando leituras periódicas.
"""

import random
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class StatusVaga(Enum):
    LIVRE = "livre"
    OCUPADA = "ocupada"


@dataclass
class Sensor:
    """Representa o sensor de presença instalado em uma vaga."""
    id_sensor: str
    ativo: bool = True

    def ler_leitura(self) -> bool:
        """
        Simula a leitura do sensor (em um cenário real, isso seria uma
        chamada a um driver de hardware, GPIO, ou uma mensagem MQTT).
        Retorna True se detectar veículo, False se detectar vaga livre.
        """
        return random.random() < 0.5


@dataclass
class Vaga:
    numero: int
    sensor: Sensor
    status: StatusVaga = StatusVaga.LIVRE
    atualizada_em: datetime = field(default_factory=datetime.now)

    def atualizar_status(self, ocupada: bool) -> bool:
        """Atualiza o status da vaga se houver mudança. Retorna True se mudou."""
        novo_status = StatusVaga.OCUPADA if ocupada else StatusVaga.LIVRE
        if novo_status != self.status:
            self.status = novo_status
            self.atualizada_em = datetime.now()
            return True
        return False


class Estacionamento:
    """Controla o conjunto de vagas e recebe atualizações dos sensores."""

    def __init__(self, total_vagas: int):
        self.vagas = [
            Vaga(numero=i, sensor=Sensor(id_sensor=f"SENSOR-{i:02d}"))
            for i in range(1, total_vagas + 1)
        ]
        self._lock = threading.Lock()
        self._executando = False
        self._log: list[str] = []

    #---------- consultas ----------

    @property
    def total_vagas(self) -> int:
        return len(self.vagas)

    @property
    def vagas_ocupadas(self) -> int:
        return sum(1 for v in self.vagas if v.status == StatusVaga.OCUPADA)

    @property
    def vagas_livres(self) -> int:
        return self.total_vagas - self.vagas_ocupadas

    @property
    def taxa_ocupacao(self) -> float:
        return (self.vagas_ocupadas / self.total_vagas) * 100

    #processamento dos sensores 

    def processar_leitura_sensor(self, vaga: Vaga):
        """Lê o sensor de uma vaga e atualiza seu status em tempo real."""
        ocupada = vaga.sensor.ler_leitura()
        with self._lock:
            mudou = vaga.atualizar_status(ocupada)
            if mudou:
                evento = (
                    f"[{vaga.atualizada_em:%H:%M:%S}] "
                    f"{vaga.sensor.id_sensor} -> vaga {vaga.numero:02d} "
                    f"agora está {vaga.status.value.upper()}"
                )
                self._log.append(evento)
                print(evento)

    def iniciar_monitoramento(self, intervalo_segundos: float = 2.0):
        """Inicia a thread que simula a leitura contínua dos sensores."""
        self._executando = True

        def loop_monitoramento():
            while self._executando:
                vaga = random.choice(self.vagas)
                self.processar_leitura_sensor(vaga)
                time.sleep(intervalo_segundos)

        thread = threading.Thread(target=loop_monitoramento, daemon=True)
        thread.start()
        return thread

    def parar_monitoramento(self):
        self._executando = False

    #painel 

    def exibir_painel(self):
        with self._lock:
            print("\n" + "=" * 46)
            print(f"  PAINEL DE VAGAS — {datetime.now():%d/%m/%Y %H:%M:%S}")
            print("=" * 46)
            for vaga in self.vagas:
                marcador = "🔴" if vaga.status == StatusVaga.OCUPADA else "🟢"
                print(f"  {marcador} Vaga {vaga.numero:02d} — {vaga.status.value.upper()}")
            print("-" * 46)
            print(
                f"  Livres: {self.vagas_livres}  |  "
                f"Ocupadas: {self.vagas_ocupadas}  |  "
                f"Ocupação: {self.taxa_ocupacao:.0f}%"
            )
            print("=" * 46)


def main():
    estacionamento = Estacionamento(total_vagas=10)

    #Inicia a simulação dos sensores em segundo plano (tempo real)
    estacionamento.iniciar_monitoramento(intervalo_segundos=1.5)

    try:
        #Exibe o painel atualizado a cada 5 segundos, enquanto os sensores
        #continuam gerando eventos em paralelo
        while True:
            time.sleep(5)
            estacionamento.exibir_painel()
    except KeyboardInterrupt:
        estacionamento.parar_monitoramento()
        print("\nMonitoramento encerrado.")


if __name__ == "__main__":
    main()
