import json
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

if __name__ == '__main__':
    unittest.main()