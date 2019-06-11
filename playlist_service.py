import logging
import json

from response_message import ServiceError

logger = logging.getLogger(__name__)

class PlaylistService:
    """
    Service to process playlist based on the actions from changes json file
    """

    ADD_SONG_TO_LIST_ACTION = 'add_a_song_to_playlist'
    ADD_LIST_TO_USER_ACTION = 'add_new_playlist_to_user'
    REMOVE_LIST_ACTION = 'remove_playlist'

    def apply_changes(self, input_json, changes_json, output_file):
        """
        apply the actions specified in changes json object. currently only 3 actions are supported.
        :param input_json: input json object
        :param changes_json: json object which contains changes
        :param output_file: output file handle
        :return:
        """
        error_list = []
        if input_json is None or changes_json is None or output_file is None \
                or 'users' not in input_json or 'playlists' not in input_json \
                or 'songs' not in input_json or 'changes' not in changes_json:
            error_list.append({ServiceError.INPUT_ERR: ServiceError.Errors[ServiceError.INPUT_ERR]})
            return error_list

        logger.info('apply changes')
        users = input_json['users']
        play_lists = input_json['playlists']
        songs = input_json['songs']

        changes = changes_json['changes']
        if changes is None or len(changes) == 0:
            error_list.append({ServiceError.NO_ACTION_DEFINED_ERR: ServiceError.Errors[ServiceError.NO_ACTION_DEFINED_ERR]})
        else:
            for change in changes:
                action = change['action']
                if action == self.ADD_SONG_TO_LIST_ACTION:
                    self.add_song_to_list(change['playlist_id'], change['song_id'], songs, play_lists, error_list)
                elif action == self.ADD_LIST_TO_USER_ACTION:
                    self.add_new_list_to_user(change['playlist_id'], change['song_id'],change['user_id'], users, songs, play_lists, error_list)
                elif action == self.REMOVE_LIST_ACTION:
                    self.remove_list(change['playlist_id'], play_lists, error_list)
                else:
                    logger.warn('unsupported action: ' + action)

        result = {'users':users, 'playlists':play_lists, 'songs':songs}
        output_file.write(json.dumps(result, sort_keys=False, indent=4))
        output_file.close()

        return error_list

    def add_song_to_list(self, playlist_id, song_id, songs, play_lists, error_list):
        """
        Add a song to an existing playlist.
        :param playlist_id: playlist id to add the song
        :param song_id: song id to be added into the playlist
        :param songs: object contains all the songs
        :param play_lists: play list which contains all the lists.
        :param error_list: error list which contains all the errors processing from the current action
        :return: void
        """
        logger.info('add song id = ' + song_id + ' to playlist id = ' + playlist_id)
        if songs is None or len(songs) == 0:
            error_list.append({ServiceError.SONG_LIST_EMPTY_ERR: ServiceError.Errors[ServiceError.SONG_LIST_EMPTY_ERR]})
            return

        song = self.get_song_by_id(song_id, songs)
        playlist = self.get_playlist_by_id(playlist_id, play_lists)
        if song and playlist and song_id not in playlist['song_ids']:
            playlist['song_ids'].append(song_id)
        else:
            if song is None:
                error_list.append({ServiceError.NO_SONG_DEFINED_ERR: ServiceError.Errors[
                    ServiceError.NO_SONG_DEFINED_ERR].format(song_id)})
            if playlist is None:
                error_list.append({ServiceError.NO_PLAYLIST_DEFINED_ERR: ServiceError.Errors[
                    ServiceError.NO_PLAYLIST_DEFINED_ERR].format(playlist_id)})
            if playlist and song_id in playlist['song_ids']:
                error_list.append({ServiceError.SONG_EXIST_ERR: ServiceError.Errors[
                    ServiceError.SONG_EXIST_ERR].format(song_id)})
        return


    def add_new_list_to_user(self, playlist_id, song_id, user_id, users, songs, play_lists, error_list):
        """
        Add new play list to the user.
        :param playlist_id: the new playlist id to be added
        :param song_id: song id which needs to exist in a new playlist
        :param user_id: user id which this new playlist is assigned to
        :param users: object which contains all users
        :param songs: object which contains all songs
        :param play_lists: it contains all the playlists
        :param error_list: error list which contains all the errors processing from the current action
        :return: void
        """
        logger.info('add new list ' + playlist_id + ' to user ' + user_id)
        song = self.get_song_by_id(song_id, songs)
        playlist = self.get_playlist_by_id(playlist_id, play_lists)
        user = self.get_user_by_id(users, user_id)

        if song and not playlist and user:
            new_list = {'id': playlist_id, 'user_id': user_id, 'song_ids': [song_id]}
            play_lists.append(new_list)
        else:
            if song is None:
                error_list.append({ServiceError.NO_SONG_DEFINED_ERR: ServiceError.Errors[
                    ServiceError.NO_SONG_DEFINED_ERR].format(song_id)})
            if playlist:
                error_list.append({ServiceError.PLAYLIST_EXIST_ERR: ServiceError.Errors[
                    ServiceError.PLAYLIST_EXIST_ERR].format(playlist_id)})
            if user is None:
                error_list.append({ServiceError.NO_USER_DEFINED_ERR: ServiceError.Errors[
                    ServiceError.NO_USER_DEFINED_ERR].format(user_id)})

    def remove_list(self, playlist_id, play_lists, error_list):
        """
        Remove an existing playlist
        :param playlist_id: the playlist id to be removed
        :param play_lists: it contains all the playlists
        :param error_list: error list which contains all the errors processing from the current action
        :return: void
        """
        if play_lists is None or len(play_lists) == 0:
            error_list.append({ServiceError.PLAYLIST_EMPTY_ERR: ServiceError.Errors[
                ServiceError.PLAYLIST_EMPTY_ERR]})
            return
        logger.info('remove list ' + playlist_id)
        for i in range(len(play_lists)):
            if play_lists[i]['id'] == playlist_id:
                del play_lists[i]
                return
        error_list.append({ServiceError.NO_PLAYLIST_DEFINED_ERR: ServiceError.Errors[
            ServiceError.NO_PLAYLIST_DEFINED_ERR].format(playlist_id)})

    def get_song_by_id(self, song_id, songs):
        """
        Util function to get the song object by song id.
        :param song_id: song id to be searched
        :param songs: it contains all the songs
        :return: song object if it's found; otherwise, None,
        """
        if song_id is None or songs is None or len(songs) == 0:
            return None

        for song in songs:
            if song['id'] == song_id:
                return song

        return None

    def get_playlist_by_id(self, playlist_id, play_lists):
        """
        Get playlist by playlist id
        :param playlist_id: playlist id to search for
        :param play_lists: it contains all the playlists
        :return: playlist object
        """
        if play_lists is None or play_lists is None or len(play_lists) == 0:
            return None

        for playlist in play_lists:
            if playlist['id'] == playlist_id:
                return playlist

        return None

    def get_user_by_id(self, users, user_id):
        """
        Get user by id.
        :param users: all the users
        :param user_id: user id to be searched for
        :return: user object
        """
        if user_id is None or users is None or len(users) == 0:
            return None

        for user in users:
            if user['id'] == user_id:
                return user

        return None