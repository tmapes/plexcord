from dataclasses import dataclass

import yaml


@dataclass
class AppConfig:
    """Class for configuring the service"""
    plex_username: str
    discord_client_id: str
    discord_process_id: int

    def __init__(self,
                 plex_username: str,
                 discord_client_id: str,
                 discord_process_id: int) -> None:
        self.plex_username = plex_username
        self.discord_client_id = discord_client_id
        self.discord_process_id = discord_process_id

    @staticmethod
    def from_yaml_file(name: str) -> 'AppConfig':
        with open(name, 'r') as config:
            raw_config = yaml.load(config, Loader=yaml.FullLoader)
            parsed_config = AppConfig(
                plex_username=raw_config.get("plex", {}).get("plex_username", ""),
                discord_client_id=raw_config.get("discord", {}).get("client_id", "aabbccdd"),
                discord_process_id=raw_config.get("discord", {}).get("process_id", 11223344),
            )
        return parsed_config
