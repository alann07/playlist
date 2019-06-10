class ServiceError:

    NO_ACTION_DEFINED_ERR = '1000'
    NO_USER_DEFINED_ERR = '1001'
    NO_SONG_DEFINED_ERR = '1002'
    NO_PLAYLIST_DEFINED_ERR = '1003'
    INPUT_ERR = '1004'
    SONG_LIST_EMPTY_ERR = '1005'
    PLAYLIST_EMPTY_ERR = '1006'
    USERLIST_EMPTY_ERR = '1007'
    SONG_EXIST_ERR = '1008'
    PLAYLIST_EXIST_ERR = '1009'

    Errors = {NO_ACTION_DEFINED_ERR: 'No action defined in change file',
              NO_USER_DEFINED_ERR: 'User {0} does not exist',
              NO_SONG_DEFINED_ERR: 'Song {0} does not exist',
              NO_PLAYLIST_DEFINED_ERR: 'Playlist {0} does not exist',
              SONG_LIST_EMPTY_ERR: 'Song list is empty',
              PLAYLIST_EMPTY_ERR: 'Playlists are empty',
              PLAYLIST_EXIST_ERR: 'Playlist {0} already exists. Not adding it.',
              USERLIST_EMPTY_ERR: 'User list is empty',
              SONG_EXIST_ERR: 'Song {0} already exists in the playlist. No action taken.'}
