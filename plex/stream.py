

class PlexStream(object):
    show_name: str
    episode_name: str
    episode_number: str
    year: int
    movie_name: str
    director: str
    time_left: int
    is_tv_stream: bool

    def __init__(self, show_name: str,
                 episode_name: str,
                 episode_number: str,
                 year: int,
                 movie_name: str,
                 director: str,
                 time_left: int,
                 is_tv_stream: bool):
        self.show_name = show_name
        self.episode_name = episode_name
        self.episode_number = episode_number
        self.year = year
        self.movie_name = movie_name
        self.director = director
        self.time_left = time_left
        self.is_tv_stream = is_tv_stream
