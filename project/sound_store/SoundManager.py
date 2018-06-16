from .models import UserData, Sounds
from .src.DataManager import DataManager
from .BasicManager import BasicManager, STORE_PATH


class SoundManager(BasicManager):
    manager = DataManager(1, STORE_PATH)

    def get(self, user_id):
        result = None
        user = UserData.user_object(user_id)
        if user is not None:
            self.manager.set_user_id(user_id)
            result = Sounds.user_sounds_data(user_id)
        return result

    def create(self, user_id, sound_name, file):
        result = None
        user = UserData.user_object(user_id)
        if user is not None:
            self.manager.set_user_id(user_id)
            is_existing_user_folder = self.manager.file_manager.is_valid_existing_folder_path(self.manager.user_folder)
            if is_existing_user_folder is False:
                # create user folder if user register in first time
                self.manager.create_user_folder()
            self.manager.save_audio_file(sound_name, file)
            full_sound_path = self.manager.get_full_file_path(sound_name)
            sound = Sounds(path=full_sound_path, name=sound_name, user=user)
            sound.save()
            result = Sounds.sound_data_by_id(sound.pk)
        return result

    def delete(self, user_id, sound_name):
        result = None
        user = UserData.user_object(user_id)
        if user is not None:
            result = Sounds.sound_data_by_name(user_id, sound_name)
            if result and result is not None:
                sound = Sounds.sound_object(result['id'])
                if sound is not None:
                    sound.delete()
                    self.manager.set_user_id(user_id)
                    self.manager.delete_user_file(sound_name)
        return result

    def update(self, *args):
        pass

    def load(self, user_id, sound_name):
        result = None
        user = UserData.user_object(user_id)
        if user is not None:
            self.manager.set_user_id(user_id)
            data = Sounds.sound_data_by_name(user_id, sound_name)
            if data and data is not None:
                file_path = data['path']
                if file_path:
                    file_object = open(file_path, 'rb')
                    result = file_object
        return result
