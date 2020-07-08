from datetime import datetime, timezone
from time import sleep

from plexapi.server import PlexServer
from plexapi.video import Episode
from pypresence import Presence, InvalidPipe


def get_plex_stream_details(plex_url, plex_token) -> dict:
    p_server = PlexServer(baseurl=plex_url, token=plex_token)
    if not p_server.sessions():
        print("No Streaming Sessions, Exiting....")
        return {}
    current_session = p_server.sessions()[0]
    if not isinstance(current_session, Episode):
        print("Invalid Media Stream Found, Exiting....")
        return {}
    show_name = current_session.grandparentTitle
    episode_name = current_session.title
    episode_number = current_session.seasonEpisode.upper()
    start_time = int(datetime.now(tz=timezone.utc).timestamp()) - (current_session.viewOffset / 1000)
    return {
        "show_name": show_name,
        "episode_title": episode_name,
        "episode_number": episode_number,
        "start_time": start_time
    }


def main(plex_url, plex_token, discord_client_id):
    presence_client = Presence(discord_client_id, pipe=0)
    try:
        presence_client.connect()
    except InvalidPipe as e:
        print(e)
        exit(-1)

    while True:
        try:
            stream_details = get_plex_stream_details(plex_url, plex_token)
            detail_string = f'{stream_details.get("show_name")} {stream_details.get("episode_number")} '
            state_string = f'{stream_details.get("episode_title")}'
            if stream_details:
                presence_client.update(
                    pid=420690,
                    state=state_string,
                    details=detail_string,
                    large_image="logo",
                    large_text="Plex",
                    start=stream_details.get("start_time")
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
    main(plex_url, plex_token, discord_client_id)
