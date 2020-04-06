import uuid

# We don't have to worry about duplicate image names because it automatically
# handles adding random characters at the end of the name if it happens

def profile_image_directory_path(instance, filename):
    return '/'.join(['profiles', uuid.uuid4().hex + ".png"])

def listing_image_directory_path(instance, filename):
    return '/'.join(['listings', uuid.uuid4().hex + ".png"])
