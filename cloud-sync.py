import paho.mqtt.client as mqtt
from typing import Dict, Any
import yaml
from pathlib import Path
import time
import threading

class Service:
    def __init__(self):
        config = self.get_config('config.yaml')
        credentials = self.get_config('credentials.yaml')

        source_mqtt_host = config['source_host']
        source_mqtt_port = config['source_port']
        source_mqtt_user = credentials['source_user']
        source_mqtt_pw = credentials['source_pw']

        target_mqtt_host = config['target_host']
        target_mqtt_port = config['target_port']
        target_mqtt_user = credentials['target_user']
        target_mqtt_pw = credentials['target_pw']

        self.source_mqtt_client = mqtt.Client()
        self.source_mqtt_client.on_connect = self.mqtt_on_connect_source
        self.source_mqtt_client.on_message = self.mqtt_on_message
        self.source_mqtt_client.username_pw_set(source_mqtt_user, source_mqtt_pw)
        self.source_mqtt_client.connect(host=source_mqtt_host, port=source_mqtt_port, keepalive=60)
        self.source_mqtt_client.subscribe("#")
        
        self.target_mqtt_client = mqtt.Client()
        self.target_mqtt_client.on_connect = self.mqtt_on_connect_target
        self.target_mqtt_client.username_pw_set(target_mqtt_user, target_mqtt_pw)
        self.target_mqtt_client.connect(host=target_mqtt_host, port=target_mqtt_port, keepalive=60)

    @staticmethod
    def get_config(filename: str) -> Dict:
        with open(Path(__file__).parent / filename, 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)
        
    def mqtt_on_connect_source(self, client: mqtt.Client, userdata: Any, flags: Dict, rc: int):
        print("Connected to Source Mqtt")

    def mqtt_on_connect_target(self, client: mqtt.Client, userdata: Any, flags: Dict, rc: int):
        print("Connected to Target Mqtt")

    def mqtt_on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        try:
            self.target_mqtt_client.reconnect()
            self.target_mqtt_client.publish(msg.topic, msg.payload)
        except:
            pass 

    def run(self):
        thread1 = threading.Thread(target = self.source_mqtt_client.loop_forever)
        thread2 = threading.Thread(target = self.target_mqtt_client.loop_forever)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

if __name__ == '__main__':
    service = Service()
    service.run()
