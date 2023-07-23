import vk_api
import requests
from py.security import *
import datetime
import time
import json
import os
from PIL import Image  # method to show pictures
from io import BytesIO


# authentication info
vk_session = vk_api.VkApi(token=access_token)  # enter token
vk = vk_session.get_api()  # get access to the API


class VkImageGrabber:

    def __init__(self, screen_id=-39043966, album_id=157131299, images_count=2):
        # if group id starts with positive number, this is a user. If with negative - it is a group
        self.screen_id = screen_id
        self.album_id = album_id
        self.images_count = images_count

    # Check if owner type is user of group
    def owner_type(self):
        if isinstance(self.screen_id, int):  # If in the url only digits, without letters, then owner type depends on
            # if value is negative or positive (+ or -)
            if self.screen_id < 0:
                owner_type = 'group'
            else:
                owner_type = 'user'
        else:  # entered screen name with letters - use VK API  method
            screen_name = vk.utils.resolveScreenName(screen_name=self.screen_id)
            owner_type = screen_name['type']
        return owner_type

    def decode_id(self):  # Based on owner type get ID and name of a user or a group.
        owner_type = self.owner_type()
        if owner_type == 'group':
            if isinstance(self.screen_id, int):  # if in screen_name is digit, take the value of the number modulo
                object_id = abs(self.screen_id)
            else:  # if not int, get id with method resolveScreenName
                group_info = vk.utils.resolveScreenName(screen_name=self.screen_id)
                object_id = abs(group_info['object_id'])
            group_id = vk.groups.getById(group_id=object_id)
            id_name_result = [group_id[0]['id'] * -1, group_id[0]['name']]  # |* -1| - coz group id must be negative
            # for test
            # print('decoded. Group_id = ', id_name_result[0], 'Group_name = ', id_name_result[1], '\n')
            return id_name_result
        else:
            if isinstance(self.screen_id, int):  # If owner type is user, and screen name = int
                object_id = abs(self.screen_id)
            else:
                # use method resolveScreenName to get user's name and surname
                screen_name = vk.utils.resolveScreenName(screen_name=self.screen_id)
                object_id = screen_name['object_id']
            user_first_name = vk.users.get(user_id=self.screen_id)[0]["first_name"]
            user_last_name = vk.users.get(user_id=self.screen_id)[0]["last_name"]
            id_name_result = list([object_id, f"{user_first_name} {user_last_name}"])
            # print('decoded. User_id = ', id_name_result[0], 'User_name = ', id_name_result[1], '\n')
        return id_name_result

    def grabbing_parameters(self):
        obj_id = self.decode_id()[0]

        if self.images_count > 0:
            response = vk.photos.get(owner_id=obj_id, album_id=self.album_id, count=self.images_count)
        else:
            count = vk.photos.get(owner_id=obj_id, album_id=self.album_id)['count']
            response = vk.photos.get(owner_id=obj_id, album_id=self.album_id, count=count, offset=0)
        # print('Response: ', len(response['items']))
        # print('Response: ', response)
        return response

    def get_album_name(self):
        obj_id = self.decode_id()[0]  # --- !!!! to do add cache !!! --- this value is used in many methods.
        album_info = vk.photos.getAlbums(owner_id=obj_id, album_ids=self.album_id)
        name = album_info['items'][0]['title']
        # print('album_name: ', name)
        return name

    def get_images_data(self):
        images_list = self.grabbing_parameters()['items']
        object_id = self.decode_id()[0]
        object_name = self.decode_id()[1]
        object_type = self.owner_type()
        album_name = self.get_album_name()
        result = []
        for image in images_list:
            date = datetime.datetime.fromtimestamp(image['date'])  # UNIX-time (POSIX)
            creation_date = date.strftime('%Y-%m-%d')
            result.append(
                {
                    'image_id': image['id'],
                    'owner_id': object_id,
                    'owner_type': object_type,
                    'owner_name': object_name,
                    'album_id': image['album_id'],
                    'album_name': album_name,
                    'creation_date': creation_date,
                    'big_picture': image['sizes'][-1]['url'],
                    # url for the biggest size is the last one in the result []
                    'thumbnail': image['sizes'][0]['url']  # url for thumbnail.
                }
            )
        # with open(f'json/{object_name}_{object_id}_{album_name}.json', 'w') as file:
        #     json.dump(result, file, indent=4, ensure_ascii=False)
        return result

    # def show_image(self):
    #     images_data = self.get_images_data()
    #     image_to_show = 0
    #     result = requests.get(images_data[image_to_show]['big_picture'])
    #     # print(images_data[result])
    #     # result = requests.get(images_data['big_picture'])
    #     print(result)
    #     image = Image.open(BytesIO(result.content))
    #     image.show()

    def download_images(self, tick=0):
        start_time = time.time()
        images_data = self.get_images_data()
        album_name = images_data[0]['album_name']
        save_images_to = f"Photos/{album_name}/"  # path to save images
        os.makedirs(save_images_to, exist_ok=True)
        # print(images_data)

        for ind in images_data:
            result = requests.get(ind['big_picture'])
            # album_name = ind['album_name']
            image_id = ind['image_id']
            tick += 1
            with open(f'{save_images_to}/vk_{album_name}_{image_id}.jpg', 'wb') as file:
                file.write(result.content)
            print(f'Image {tick} saved')

        total_seconds = time.time() - start_time
        print(f"======================="
              f"\nTotal saved images: {len(images_data)}"
              f"\nTime: {int(total_seconds // 60):02d}m : {int(total_seconds % 60):02d}s"
              f"\n=======================")

        def __str__(self):
            return f"input data: Screen_name = {self.screen_id}, album_id =" \
                   f"  {self.album_id}, images_count = {self.images_count}"


images_count = 3


# my group V
# owner_id = -39043966
# album_id = 157130717

owner_id = -70022346
album_id = 255403373




grabbed_images = VkImageGrabber(screen_id=owner_id, album_id=album_id, images_count=images_count)
# print(grabbed_images.decode_id())
# grabbed_images.download_images()

#
def run_scrapper():
    print(grabbed_images.decode_id())
    grabbed_images.download_images()
    return "FINALY"


# run_scrapper()
#
# 'Lis-And-Rox Rowe' X
# UnicodeEncodeError: 'charmap' codec can't encode character '\xf3' in position 10: character maps to <undefined>
# owner_id = 93217433
# album_id = 115419411

# random user
    # owner_id = 'mikerezler'
    # album_id = 456241036
    # # Доступ к сохранёнкам можно получить только с помощью user_access_api!!
    # # Апи сервисного приложения не подойдет.

# Me
# owner_id = 52373470
# album_id = 333658955
