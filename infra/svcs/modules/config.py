import pulumi
import json

class PulumiConfig:
    def __init__(self) -> None:
        srvs_config = pulumi.Config()
        self.environment = srvs_config.get("environment", "dev")
    
    def showValues(self) -> None:
        print(json.dumps(self.__dict__, indent=4))