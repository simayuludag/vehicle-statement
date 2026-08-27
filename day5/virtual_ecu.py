import time
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class CANMessage:
    msg_name: str
    can_id: int
    is_extended: bool
    payload: Dict[str, Any]
    timestamp: float


class BaseECU:
    """Temel Sanal ECU Sınıfı"""
    def __init__(self, name: str):
        self.name = name
        self.alive_counters: Dict[str, int] = {}

    def _next_alive_counter(self, msg_key: str) -> int:
        """4-bitlik (0-15) artan Canlılık Sayacı (Alive Counter) üretir."""
        cnt = self.alive_counters.get(msg_key, 0)
        self.alive_counters[msg_key] = (cnt + 1) & 0x0F
        return cnt


class PowertrainECU(BaseECU):
    """Motor, şanzıman ve pedal dinamiklerinden sorumlu ECU."""
    def __init__(self):
        super().__init__("Powertrain_ECU")
        self.rpm = 850
        self.temp = 90.0

    def generate_powertrain_status(self) -> CANMessage:
        return CANMessage(
            msg_name="PowertrainStatus",
            can_id=0x101,
            is_extended=False,
            payload={
                "EngineRPM": self.rpm,
                "EngineTemp": self.temp,
                "GearPosition": 1,
                "AliveCounter": self._next_alive_counter("powertrain_status")
            },
            timestamp=time.time()
        )

    def generate_pedal_status(self) -> CANMessage:
        return CANMessage(
            msg_name="PedalStatus",
            can_id=0x102,
            is_extended=False,
            payload={
                "ThrottlePosition": 15.5,  # %
                "BrakeApplied": 0,
                "AliveCounter": self._next_alive_counter("pedal_status")
            },
            timestamp=time.time()
        )


class BodyECU(BaseECU):
    """Gövde, konfor, aydınlatma ve kullanıcı verilerinden sorumlu ECU."""
    def __init__(self, user_age: int = 22):
        super().__init__("Body_ECU")
        self.user_age = user_age

    def generate_body_status(self) -> CANMessage:
        return CANMessage(
            msg_name="BodyStatus",
            can_id=0x201,
            is_extended=False,
            payload={
                "DoorLockState": 1,
                "HeadlightStatus": 0,
                "Age": self.user_age,
                "AliveCounter": self._next_alive_counter("body_status")
            },
            timestamp=time.time()
        )


class DiagnosticECU(BaseECU):
    """Hata kodları (DTC) ve teşhis durumundan sorumlu ECU."""
    def __init__(self):
        super().__init__("Diagnostic_ECU")

    def generate_diagnostic_status(self) -> CANMessage:
        return CANMessage(
            msg_name="DiagnosticStatus",
            can_id=0x18DAF110,
            is_extended=True,
            payload={
                "ActiveDTCCount": 0,
                "ECUOperatingMode": 1,  # 1: Normal
                "AliveCounter": self._next_alive_counter("diag_status")
            },
            timestamp=time.time()
        )