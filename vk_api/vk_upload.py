# -*- coding: utf-8 -*-

"""
@author: Kirill Python
@contact: http://vk.com/python273
@license Apache License, Version 2.0, see LICENSE file

Copyright (C) 2014
"""


class VkUpload(object):
    def __init__(self, vk):
        self.vk = vk
        # https://vk.com/dev/upload_files

    def photo(self, photos, album_id, group_id=None):
        """ Загрузка изображений в альбом пользователя

        :param photos: список путей к изображениям, либо путь к изображению
        :param album_id: идентификатор альбома
        :param group_id: идентификатор сообщества (если загрузка идет в группу)
        """

        if type(photos) == str:
            photos = [photos]

        values = {
            'album_id': album_id
        }
        if group_id:  # Если загружаем в группу
            values.update({'group_id': group_id})

        # Получаем ссылку для загрузки
        url = self.vk.method('photos.getUploadServer', values)['upload_url']

        # Загружаем
        photos_files = openPhotos(photos)
        response = self.vk.http.post(url, files=photos_files).json()
        closePhotos(photos_files)

        # Олег Илларионов:
        # это не могу к сожалению просто пофиксить
        if not 'album_id' in response:
            response['album_id'] = response['aid']

        # Сохраняем фото в альбоме
        response = self.vk.method('photos.save', response)

        return response

    def photo_messages(self, photos):
        """ Загрузка изображений в сообщения

        :param photos: список путей к изображениям, либо путь к изображению
        """

        if type(photos) == str:
            photos = [photos]

        values = {}

        url = self.vk.method('photos.getMessagesUploadServer', values)
        url = url['upload_url']

        photos_files = openPhotos(photos)
        response = self.vk.http.post(url, files=photos_files)
        closePhotos(photos_files)

        response = self.vk.method('photos.saveMessagesPhoto', response.json())

        return response

    def photo_wall(self, photos, group_id=None):
        """ Загрузка изображений на стену пользователя или в группу

        :param photos: список путей к изображениям, либо путь к изображению
        :param group_id: идентификатор сообщества (если загрузка идет в группу)
        """

        if type(photos) == str:
            photos = [photos]

        values = {}
        if group_id:
            values.update({'group_id': group_id})

        response = self.vk.method('photos.getWallUploadServer', values)
        url = response['upload_url']

        photos_files = openPhotos(photos)
        response = self.vk.http.post(url, files=photos_files)
        closePhotos(photos_files)

        response = self.vk.method('photos.saveWallPhoto', response.json())

        return response

    def document(self, file_path, title=None, tags=None, group_id=None):
        """ Загрузка документа

        :param file_path: путь к документу
        :param title: название документа
        :param tags: метки для поиска
        :param group_id: идентификатор сообщества (если загрузка идет в группу)
        """

        values = {}
        if group_id:
            values.update({'group_id': group_id})

        url = self.vk.method('docs.getUploadServer', values)['upload_url']

        with open(file_path, 'rb') as file:
            response = self.vk.http.post(url, files={'file': file}).json()

        if title:
            response.update({'title': title})

        if tags:
            response.update({'tags': tags})

        response = self.vk.method('docs.save', response)

        return response


def openPhotos(photos_paths):
    photos = {}

    for x, filename in enumerate(photos_paths):  # Открываем файлы
        photos.update(
            {'file%s' % x: open(filename, 'rb')}
        )

    return photos


def closePhotos(photos):
    for i in photos:
        photos[i].close()
