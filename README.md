# Processing Playlist

This app is a console application that applies a batch of changes to an input playlist file in order to create an output file.
The playlist file contains info like user, playlist and songs. The changes, in a change file, contains operations like

* Add a song to an existing playlist
* Add a new playlist to a user
* Remove an existing playlist

## Getting Started

## How it works

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