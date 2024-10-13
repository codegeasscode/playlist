from .models import Songs


def songs_populator(path="../playlist.json"):
    '''    
    :param file_path: The path to the JSON file containing song data

    Populate the Songs model

    '''
    Songs.objects.from_json_file(path)

    return

