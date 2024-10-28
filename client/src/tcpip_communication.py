import socket
import json

from custom_types.model_type import ModelType
from custom_types.optimization_mode import OptimizationMode
from custom_types.domain_type import DomainType

class TcpipCommunication:
    
    def __init__(self, remote_host, remote_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(100)        
        self.is_connected = self.connect(remote_host, remote_port)

    def connect(self, remote_host, remote_port) -> bool:
        try:
            self.client_socket.connect((remote_host, remote_port))
            is_connected = True
        except socket.error as e:
            print(f"Connection error: {e}")
            is_connected = False
        finally:
            return is_connected
    
    def run_simulation(self):
        message = "RUN;"

        received_message = self._send(message)

        result_json = json.loads(received_message)
        return result_json

    def load_model(self, model_type: ModelType):
        message = f"LOAD model {model_type.name};"

        received_message = self._send(message)

        model_data_json = json.loads(received_message)
        return model_data_json
    
    def set_optimization_mode(self, optimization_mode: OptimizationMode):
        message = f"SET optimization_mode {optimization_mode.name};"

        received_message = self._send(message)

        result_json = json.loads(received_message)
        return result_json

    def set_primary_domain(self, domain_type: DomainType):
        message = f"SET primary_domain {domain_type.name};"

        received_message = self._send(message)

        result_json = json.loads(received_message)
        return result_json
    
    def _send(self, message: str) -> str:
        self.client_socket.sendall(message.encode())

        received_message = b''
        while True:
            fragment = self.client_socket.recv(4096)
            if not fragment or fragment == b'\x00':
                break
            received_message += fragment

        received_message = received_message.split(b';', 1)[0]
        received_message = received_message.decode('utf-8', errors='replace')
        return received_message
