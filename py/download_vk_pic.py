"""
Класс для скачивания будет вынесен в этот файл, но потом

"""


from scrapper import VkImageGrabber
import os
import requests  # method for downloading photos
from PIL import Image  # method to show pictures
from io import BytesIO


class VkDownloadImages(VkImageGrabber):

    def show_image(self):
        images_data = self.get_images_data()
        image_to_show = 0
        print(images_data)
        result = requests.get(images_data[image_to_show][4])
        print(result)
        image = Image.open(BytesIO(result.content))
        image.show()

    def download_images(self):
        images_data = self.get_images_data()
        # path to save images
        save_images_to = "../../../Pictures/Photos/"
        os.makedirs(save_images_to, exist_ok=True)
        for ind in images_data:
            result = requests.get(ind[4])
            with open(f'{save_images_to}/vk_{ind[0]}.jpg', 'wb') as file:
                file.write(result.content)
                print('Image saved.')
        print(f"Saved {len(images_data)}" ' images')


# For testing
# print(VkDownloadImages.show_image())
# print(VkDownloadImages.download_images())


