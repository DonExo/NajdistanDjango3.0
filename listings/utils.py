import imghdr


def _check_image_validness(files):
    print(f"Received {len(files)} files")
    invalid_files = []
    valid_files = []
    for file in files:
        if imghdr.what(file) == None:
            invalid_files.append(file)
        else:
            valid_files.append(file)
    print(f"Returning {len(valid_files)} images and {len(invalid_files)} files to the caller.")
    return valid_files, invalid_files
