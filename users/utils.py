import uuid

def profile_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # return 'profiles/{0}/{1}'.format(instance.pk, filename)
    extension = filename.rsplit('.', 1)[1] # .jpg
    return '/'.join(['profiles', str(instance.id), str(uuid.uuid4().hex + "." + extension)])