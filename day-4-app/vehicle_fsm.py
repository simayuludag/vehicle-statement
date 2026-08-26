from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class State(Enum):
    OFF = auto()
    IGNITION_ON = auto()
    ENGINE_RUNNING = auto()
    DRIVING = auto()
    FAULT = auto()
    RECOVERY = auto()
    SHUTDOWN = auto()

@dataclass
class VehicleInputs:
    ignition: bool = False
    start_button: bool = False
    throttle: float = 0.0      # 0.0 - 100.0 (%)
    brake: float = 0.0         # 0.0 - 100.0 (%)
    gear: str = "P"            # "P", "R", "N", "D"
    fault_trigger: bool = False
    clear_fault: bool = False

class VehicleFSM:
    def __init__(self, dt: float = 0.1):
        self.dt = dt  # 100ms döngü süresi (10 Hz periyodik)
        self.state = State.OFF
        self.speed = 0.0       # km/h
        self.rpm = 0.0         # Devir/dakika
        self.fault_code: Optional[str] = None

    def _entry_action(self, new_state: State):
        """Duruma ilk girişte çalıştırılan eylemler (Entry Actions)"""
        if new_state == State.OFF:
            self.rpm = 0.0
            self.speed = 0.0
            self.fault_code = None
        elif new_state == State.ENGINE_RUNNING:
            self.rpm = 800.0  # Rölanti devri
        elif new_state == State.FAULT:
            self.fault_code = "ERR_CRITICAL_OVERHEAT"
            self.speed = max(0.0, self.speed * 0.5)

    def _exit_action(self, old_state: State):
        """Durumdan çıkışta tetiklenen eylemler (Exit Actions)"""
        if old_state == State.FAULT:
            self.fault_code = None

    def _transition_to(self, new_state: State):
        if self.state != new_state:
            self._exit_action(self.state)
            self.state = new_state
            self._entry_action(new_state)

    def update(self, inputs: VehicleInputs) -> dict:
        """Deterministik periyodik durum geçişleri ve fizik döngüsü"""
        # Global Fault Guard
        if inputs.fault_trigger and self.state not in (State.FAULT, State.OFF):
            self._transition_to(State.FAULT)

        # Durum Geçiş Mantığı (State Transitions & Guards)
        if self.state == State.OFF:
            if inputs.ignition:
                self._transition_to(State.IGNITION_ON)

        elif self.state == State.IGNITION_ON:
            if not inputs.ignition:
                self._transition_to(State.OFF)
            elif inputs.start_button and inputs.brake >= 20.0:  # Guard: Frene basılı marş
                self._transition_to(State.ENGINE_RUNNING)

        elif self.state == State.ENGINE_RUNNING:
            if not inputs.ignition:
                self._transition_to(State.SHUTDOWN)
            elif inputs.gear == "D" and inputs.throttle > 5.0 and inputs.brake < 5.0:
                self._transition_to(State.DRIVING)
            else:
                self.rpm = 800.0
                self.speed = 0.0

        elif self.state == State.DRIVING:
            if not inputs.ignition:
                self._transition_to(State.SHUTDOWN)
            else:
                # Deterministik Araç Dinamiği
                accel = (inputs.throttle * 0.45) - (inputs.brake * 0.90) - (self.speed * 0.04)
                self.speed = max(0.0, self.speed + accel * self.dt)
                
                # Devir-Hız-Gaz ilişkisi
                base_rpm = 800.0 + (self.speed * 40.0)
                throttle_boost = inputs.throttle * 15.0
                self.rpm = max(800.0, base_rpm + throttle_boost)

                # Durma Guard'ı
                if self.speed <= 0.1 and inputs.throttle == 0.0:
                    self.speed = 0.0
                    self._transition_to(State.ENGINE_RUNNING)

        elif self.state == State.FAULT:
            self.speed = max(0.0, self.speed - (20.0 * self.dt))
            self.rpm = 0.0 if self.speed == 0.0 else 600.0
            if inputs.clear_fault and self.speed == 0.0:
                self._transition_to(State.RECOVERY)

        elif self.state == State.RECOVERY:
            # Sistem otomatik kendini test eder ve rölantiye döner
            self._transition_to(State.ENGINE_RUNNING)

        elif self.state == State.SHUTDOWN:
            # Motor kapatma sekansı tamamlanır
            self._transition_to(State.OFF)

        return {
            "state": self.state.name,
            "speed_kmh": round(self.speed, 2),
            "rpm": round(self.rpm, 1)
        }