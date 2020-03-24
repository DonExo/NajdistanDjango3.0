import uuid

def profile_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_uuid>/profile_image.jpg
    return '/'.join(['profiles', str(instance.uuid.hex), "profile_image.jpg"])