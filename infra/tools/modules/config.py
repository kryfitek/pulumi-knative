import pulumi
import json

class PulumiConfig:
    def __init__(self) -> None:
        tools_config = pulumi.Config()
        self.environment = tools_config.get("environment", "dev")
    
    def showValues(self) -> None:
        print(json.dumps(self.__dict__, indent=4))