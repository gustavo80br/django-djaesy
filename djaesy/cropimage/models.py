import os

from PIL import Image
from django.db import models


class CropImage(models.Model):

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    class Meta:
        abstract = True

    def need_cropping(self):

        image_changed = False

        for ratio_field in self.ratio_fields:

            ratio_field_instance = self._meta.get_field(ratio_field)
            image_field = getattr(self, ratio_field_instance.image_field)
            ratio = getattr(self, ratio_field)

            if not self._state.adding:
                image_changed = bool(image_field != self._loaded_values[ratio_field_instance.image_field] and image_field and ratio_field and ratio)

        return image_changed

    def save(self, *args, **kwargs):
        self.save_cropped_image(*args, **kwargs)

        # for ratio_field in self.ratio_fields:
        #
        #     ratio_field_instance = self._meta.get_field(ratio_field)
        #     image_field = getattr(self, ratio_field_instance.image_field)
        #     ratio = getattr(self, ratio_field)
        #
        #     if image_field:
        #
        #         filename, extension = os.path.splitext(str(image_field.file))
        #         cropped_filename = f'{filename}.{ratio_field}{extension}'
        #
        #         no_crop_file = False
        #         image_changed = False
        #
        #         if not self._state.adding:
        #             ratio_changed = bool(ratio != self._loaded_values[ratio_field] and ratio_field and image_field and ratio)
        #             image_changed = bool(image_field != self._loaded_values[ratio_field_instance.image_field] and image_field and ratio_field and ratio)
        #             no_crop_file = not os.path.exists(cropped_filename)
        #         else:
        #             ratio_changed = bool(ratio_field and image_field)
        #
        #         if (ratio_changed or image_changed or no_crop_file) and ratio:
        #             width = ratio_field_instance.width
        #             height = ratio_field_instance.height
        #             image = Image.open(image_field.file)
        #             cropped_image = image.crop(list(map(lambda x: int(x), ratio.split(','))))
        #             resized_image = cropped_image.resize((width, height), Image.ANTIALIAS)
        #             resized_image.save(cropped_filename)
        #
        # super().save(*args, **kwargs)

    def save_cropped_image(self, *args, **kwargs):

        for ratio_field in self.ratio_fields:

            ratio_field_instance = self._meta.get_field(ratio_field)
            image_field = getattr(self, ratio_field_instance.image_field)
            ratio = getattr(self, ratio_field)

            if image_field:

                filename, extension = os.path.splitext(str(image_field.file))
                cropped_filename = f'{filename}.{ratio_field}{extension}'

                no_crop_file = False
                image_changed = False

                if not self._state.adding:
                    ratio_changed = bool(
                        ratio != self._loaded_values[ratio_field] and ratio_field and image_field and ratio)
                    image_changed = bool(image_field != self._loaded_values[
                        ratio_field_instance.image_field] and image_field and ratio_field and ratio)
                    no_crop_file = not os.path.exists(cropped_filename)
                else:
                    ratio_changed = bool(ratio_field and image_field)

                if (ratio_changed or image_changed or no_crop_file) and ratio:
                    width = ratio_field_instance.width
                    height = ratio_field_instance.height
                    image = Image.open(image_field.file)
                    cropped_image = image.crop(list(map(lambda x: int(x), ratio.split(','))))
                    resized_image = cropped_image.resize((width, height), Image.ANTIALIAS)
                    resized_image.save(cropped_filename)

        super().save(*args, **kwargs)