from time import sleep

import yaml
from pypresence import Presence, InvalidPipe, ServerError

from app_config import AppConfig
from plex import PlexConnection, StreamsNotFoundException, InvalidStreamException, InvalidParameterException


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
            stream_details = plex_client.get_plex_stream_details(plex_username=app_config.plex_username)
            if stream_details:
                if stream_details.is_tv_stream:
                    presence_client.update(
                        pid=app_config.discord_process_id,
                        details=f'{stream_details.show_name} {stream_details.episode_number} ',
                        state=stream_details.episode_name,
                        large_image="logo",
                        large_text="Plex",
                        end=stream_details.time_left
                    )
                else:
                    presence_client.update(
                        pid=app_config.discord_process_id,
                        details=f'{stream_details.movie_name} ({stream_details.year})',
                        state=stream_details.director,
                        large_image="logo",
                        large_text="Plex",
                        end=stream_details.time_left
                    )
            else:
                print('Clearing Presence as no Plex stream was found')
                presence_client.clear(pid=app_config.discord_process_id)
            sleep(app_config.plex_poll_time)
        except StreamsNotFoundException as e:
            print(f'No streams found, sleeping {app_config.plex_poll_time} seconds {e}')
            presence_client.clear(app_config.discord_process_id)
            sleep(app_config.plex_poll_time)
        except InvalidStreamException as e:
            print(f'Invalid stream found, sleeping {app_config.plex_poll_time} seconds {e}')
            sleep(app_config.plex_poll_time)
        except ServerError as e:
            print(f'Discord Authorization Error Caught, please check Discord configuration. '
                  f'Sleeping {app_config.plex_poll_time} seconds {e}')
            sleep(app_config.plex_poll_time)
        except InvalidParameterException as e:
            print('InvalidParameterException caught, check config | exiting..')
            print(e)
            break
        except BaseException as e:
            print(f'Fatal Exception Caught, exiting....')
            print(e)
            break

    presence_client.close()


if __name__ == '__main__':
    with open(r'config.yaml') as config:
        raw_config = yaml.load(config, Loader=yaml.FullLoader)
        parsed_config = AppConfig(
            plex_server_address=raw_config.get("plex", {}).get("server_address", "http://localhost:32400"),
            plex_user_token=raw_config.get("plex", {}).get("user_token", "aabbccdd"),
            plex_poll_time=raw_config.get("plex", {}).get("poll_time", 60),
            plex_username=raw_config.get("plex", {}).get("plex_username", ""),
            discord_client_id=raw_config.get("discord", {}).get("client_id", "aabbccdd"),
            discord_process_id=raw_config.get("discord", {}).get("process_id", 11223344),
        )
        main(parsed_config)
