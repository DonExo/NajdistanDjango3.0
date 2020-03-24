def profile_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance)
    print(dir(instance))
    print(filename)
    return 'profiles/{0}/{1}'.format(instance.user.id, filename)