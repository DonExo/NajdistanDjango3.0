import uuid

def profile_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_uuid>/*.jpg
    return '/'.join(['profiles', str(instance.uuid.hex), str(instance.uuid.hex)[:8] + ".jpg"])