import unittest
from playlist_service import PlaylistService
from response_message import ServiceError

class PlaylistServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.playlist_service = PlaylistService()
        self.users = {
            "users": [
                {
                    "id": "1",
                    "name": "Albin Jaye"
                },
                {
                    "id": "2",
                    "name": "Dipika Crescentia"
                },
                {
                    "id": "3",
                    "name": "Ankit Sacnite"
                }
            ]
        }

        self.play_lists = {
            "playlists": [
                {
                  "id" : "1",
                  "user_id" : "2",
                  "song_ids": [
                    "8",
                    "32"
                  ]
                },
                {
                  "id" : "2",
                  "user_id" : "3",
                  "song_ids": [
                    "6",
                    "8",
                    "11"
                  ]
                }
            ]
        }

        self.songs = {
            "songs": [
                {
                  "id" : "1",
                  "artist": "Camila Cabello",
                  "title": "Never Be the Same"
                },
                {
                  "id" : "2",
                  "artist": "Zedd",
                  "title": "The Middle"
                },
                {
                  "id" : "3",
                  "artist": "The Weeknd",
                  "title": "Pray For Me"
                }
            ]
        }

        self.changes = {
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

    def tearDown(self):
        pass

    # Test add_song_to_list
    def test_add_song_to_list_list_not_exist(self):
        error_list = []
        self.playlist_service.add_song_to_list('40', '1', self.songs['songs'], self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.NO_PLAYLIST_DEFINED_ERR in error_list[0]

    def test_add_song_to_list_song_not_exist(self):
        error_list = []
        self.playlist_service.add_song_to_list('2', '19', self.songs['songs'], self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.NO_SONG_DEFINED_ERR in error_list[0]

    def test_add_song_to_list_song_list_empty(self):
        error_list = []
        self.playlist_service.add_song_to_list('2', '19', [], self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.SONG_LIST_EMPTY_ERR in error_list[0]

    def test_add_song_to_list_successful(self):
        error_list = []
        play_lists = self.play_lists['playlists']
        num_songs_before_add = len(play_lists[0]['song_ids'])
        self.playlist_service.add_song_to_list('1', '2', self.songs['songs'], play_lists, error_list)
        num_songs_after_add = len(play_lists[0]['song_ids'])
        assert len(error_list) == 0
        assert num_songs_before_add == num_songs_after_add - 1

    # Test add_new_list_to_user
    def test_add_new_list_to_user_song_not_exist(self):
        error_list = []
        self.playlist_service.add_new_list_to_user('4', '18', '3', self.users['users'], self.songs['songs'],
                                                   self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.NO_SONG_DEFINED_ERR in error_list[0]

    def test_add_new_list_to_user_list_already_exist(self):
        error_list = []
        self.playlist_service.add_new_list_to_user('2', '1', '3', self.users['users'], self.songs['songs'],
                                                   self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.PLAYLIST_EXIST_ERR in error_list[0]

    def test_add_new_list_to_user_no_such_user(self):
        error_list = []
        self.playlist_service.add_new_list_to_user('2', '1', '33', self.users['users'], self.songs['songs'],
                                                   self.play_lists['playlists'], error_list)
        assert len(error_list) == 2
        assert ServiceError.PLAYLIST_EXIST_ERR in error_list[0]
        assert ServiceError.NO_USER_DEFINED_ERR in error_list[1]

    def test_add_new_list_to_user_successful(self):
        error_list = []
        play_lists = self.play_lists['playlists']
        num_lists_before_add = len(play_lists)

        self.playlist_service.add_new_list_to_user('4', '1', '1', self.users['users'], self.songs['songs'],
                                                   play_lists, error_list)
        num_lists_after_add = len(play_lists)
        assert len(error_list) == 0
        assert num_lists_before_add == num_lists_after_add - 1

    # Test remove_list
    def test_remove_list_lists_empty(self):
        error_list = []
        self.playlist_service.remove_list('1', [], error_list)
        assert len(error_list) == 1
        assert ServiceError.PLAYLIST_EMPTY_ERR in error_list[0]

    def test_remove_list_list_not_exist(self):
        error_list = []
        self.playlist_service.remove_list('5', self.play_lists['playlists'], error_list)
        assert len(error_list) == 1
        assert ServiceError.NO_PLAYLIST_DEFINED_ERR in error_list[0]

    def test_remove_list_successful(self):
        error_list = []
        play_lists = self.play_lists['playlists']
        num_lists_before_remove = len(play_lists)

        self.playlist_service.remove_list('1', play_lists, error_list)
        num_lists_after_remove = len(play_lists)
        assert len(error_list) == 0
        assert num_lists_before_remove == num_lists_after_remove + 1

if __name__ == '__main__':
    unittest.main()