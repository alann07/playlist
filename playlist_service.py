import logging
import json

logger = logging.getLogger(__name__)

class PlaylistService:

    ADD_SONG_TO_LIST_ACTION = 'add_a_song_to_playlist'
    ADD_LIST_TO_USER_ACTION = 'add_new_playlist_to_user'
    REMOVE_LIST_ACTION = 'remove_playlist'

    def apply_changes(self, input_json, changes_json, output_file):
        logger.info('apply changes')
        users = input_json['users']
        play_list = input_json['playlists']
        songs = input_json['songs']

        error_list = []

        changes = changes_json['changes']
        for change in changes:
            action = change['action']
            if action == self.ADD_SONG_TO_LIST_ACTION:
                self.add_song_to_list(change['playlist_id'], change['song_id'], songs, play_list, error_list)
            elif action == self.ADD_LIST_TO_USER_ACTION:
                self.add_new_list_to_user(change['playlist_id'], change['song_id'],change['user_id'], songs, play_list, error_list)
            elif action == self.REMOVE_LIST_ACTION:
                self.remove_list(change['playlist_id'], play_list, users, error_list)
            else:
                logger.warn('unsupported action: ' + action)

        result = {'users':users, 'playlists':play_list, 'songs':songs}
        output_file.write(json.dumps(result, sort_keys=False, indent=4))
        output_file.close()

        return error_list

    def add_song_to_list(self, playlist_id, song_id, songs, play_list, error_list):
        logger.info('add song id = ' + song_id + ' to playlist id = ' + playlist_id)
        song = self.get_song_by_id(song_id, songs)
        playlist = self.get_playlist_by_id(playlist_id, play_list)
        if song and playlist and song_id not in playlist['song_ids']:
            playlist['song_ids'].append(song_id)


    def add_new_list_to_user(self, playlist_id, song_id, user_id, songs, play_list, error_list):
        logger.info('add list')
        new_list = {'id': playlist_id, 'user_id': user_id, 'song_ids': [song_id]}
        play_list.append(new_list)


    def remove_list(self, playlist_id, play_list, users, error_list):
        logger.info('remove list')
        for i in range(len(play_list)):
            if play_list[i]['id'] == playlist_id:
                del play_list[i]
                break


    def get_song_by_id(self, song_id, songs):
        if song_id is None or songs is None or len(songs) == 0:
            return None

        for song in songs:
            if song['id'] == song_id:
                return song

        return None

    def get_playlist_by_id(self, playlist_id, play_list):
        if play_list is None or play_list is None or len(play_list) == 0:
            return None

        for playlist in play_list:
            if playlist['id'] == playlist_id:
                return playlist

        return None