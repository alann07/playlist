# Processing Playlist

This app is a console application that applies a batch of changes to an input playlist file in order to create an output file.
The playlist file contains info like user, playlist and songs. The changes, in a change file, contains operations like

* Add a song to an existing playlist
* Add a new playlist to a user
* Remove an existing playlist

## Getting Started

### How it works

The input JSON file, which is called mixtape.json in this project, or any name you like.

For the changes in changes.json, below is the format.

```
{
  "changes": [
    {
      "action": "add_a_song_to_playlist",
      "playlist_id": "1",
      "song_id": "40"
    },
    {
      "action": "add_new_playlist_to_user",
      "user_id": "5",
      "playlist_id": "4",
      "song_id": "5"
    },
    {
      "action": "remove_playlist",
      "playlist_id": "2"
    }
  ]
}
```

It contains 3 basic actions, i.e., add a song to a playlist, add a new playlist to a user and remove the playlist. The file may contain multiple actions.

### How to Run

From the console for this project, you run

```
$ python process_playlist.py <input-file> <changes-file> <output-file>
```

For example:

```
$ python process_playlist.py mixtape.json changes.json output-file.json
```

### Output

output.json contains the current status of the playlist after the changes are appplied.

If the changes are applied successfully, the console will show change applied, as well as the "successful" message
```
2019-06-10 22:21:05,748 - playlist_service - INFO - apply changes
2019-06-10 22:21:05,748 - playlist_service - INFO - add song id = 40 to playlist id = 1
2019-06-10 22:21:05,748 - playlist_service - INFO - add new list 4 to user 5
2019-06-10 22:21:05,749 - playlist_service - INFO - remove list 2
2019-06-10 22:21:05,749 - __main__ - INFO - Playlist Processing Successful
```

Besides, if there are any errors during process, errors are recorded and display on the console. Error from one action won't stop applying changes from other actions.

```
2019-06-10 22:23:16,384 - playlist_service - INFO - apply changes
2019-06-10 22:23:16,384 - playlist_service - INFO - add song id = 40 to playlist id = 1
2019-06-10 22:23:16,384 - playlist_service - INFO - add new list 4 to user 50
2019-06-10 22:23:16,384 - playlist_service - INFO - remove list 2
2019-06-10 22:23:16,385 - __main__ - INFO - Playlist processing has errors:
2019-06-10 22:23:16,385 - __main__ - INFO - 1001: User 50 does not exist
```

For the above message, if you try to add a new playlist to user 50, such user does not exist, and hence the message "User 50 does not exist".

For current design, 10 error codes and message are defined.

```
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
```

The corresponding messages are
```
NO_ACTION_DEFINED_ERR: 'No action defined in change file',
NO_USER_DEFINED_ERR: 'User {0} does not exist',
NO_SONG_DEFINED_ERR: 'Song {0} does not exist',
NO_PLAYLIST_DEFINED_ERR: 'Playlist {0} does not exist. Not removing it.',
SONG_LIST_EMPTY_ERR: 'Song list is empty',
PLAYLIST_EMPTY_ERR: 'Playlists are empty',
PLAYLIST_EXIST_ERR: 'Playlist {0} already exists. Not adding it.',
USERLIST_EMPTY_ERR: 'User list is empty',
SONG_EXIST_ERR: 'Song {0} already exists in the playlist. No action taken.'
```

## How to Scale / Optimize

When the playlist file or changes file becomes very large, it is a big performance hit to read and write them from/to files. Here are a few thoughts.

### Host the process as a service and playlist in a DB

If the file, like mixtape becomes larger than the memory limit, we may put it into a database, and retrieve it using paging approach.

If the app is used frequently, we may run it as a service, in order to save the time to load from playlist input file.

When using the service, we can further apply the following

* Use cache to hold the playlist
* Use distributed DB to store playlist based on the cluster of, for example, user name, or playlist id, so that the processing can be done parallely.

If we have clustered user info, such playlist can be processed concurrently with seperate instances of playlist processor.

### Algorithm Optimization

If the playlist to be removed is the new listed added earlier or has a song added earlier, the previous add song or add new playlist before the removal does not need to be applied.

Or, we may group operations for the same playlist id, and spring a new instance/thread to process it concurrently.