from time import sleep

import yaml
from pypresence import Presence, InvalidPipe

from plex import PlexConnection
from app_config import AppConfig


def main(app_config: AppConfig):
    plex_client = PlexConnection(url=app_config.plex_server_address, token=app_config.plex_user_token)
    presence_client = Presence(app_config.discord_client_id, pipe=0)
    try:
        presence_client.connect()
        presence_client.clear(app_config.discord_process_id)
    except InvalidPipe as e:
        print(e)
        exit(-1)

    while True:
        try:
            print('Getting New Stream Details')
            stream_details = plex_client.get_plex_stream_details()
            print(stream_details)
            detail_string = f'{stream_details.show_name} {stream_details.episode_number} '
            state_string = f'{stream_details.episode_name}'
            if stream_details:
                presence_client.update(
                    pid=app_config.discord_process_id,
                    state=state_string,
                    details=detail_string,
                    large_image="logo",
                    large_text="Plex",
                    end=stream_details.time_left
                )
            else:
                print('Clearing Presence as no Plex stream was found')
                presence_client.clear(pid=420690)
            sleep(10)
        except BaseException as e:
            print(e)
            break

    presence_client.close()


if __name__ == '__main__':
    with open(r'config.yaml') as config:
        raw_config = yaml.load(config, Loader=yaml.FullLoader)
        parsed_config = AppConfig(
            plex_server_address=raw_config.get("plex", {}).get("server_address", "http://localhost:32400"),
            plex_user_token=raw_config.get("plex", {}).get("user_token", "aabbccdd"),
            discord_client_id=raw_config.get("discord", {}).get("client_id", "aabbccdd"),
            discord_process_id=raw_config.get("discord", {}).get("process_id", 11223344),
        )
        main(parsed_config)
