"""Run this program to get all Spotlight Wallpapers in an image format
configured for your PC (in the highest quality) at a desired location

Works in all(?) Python versions, can be converted to Python 2,
follows (almost) all PEP-8 guidelines
"""


__author__ = 'Avinash Maddikonda'
__version__ = '1.0.0'


# Import module `os` for functions
# `makedirs`, `listdir`
import os

# Import module `shutil` for functions
# `rmtree`, `copyfile`
import shutil

# Import module `getpass` for function
# `getuser` to get current username
import getpass

# Import function `sleep` as `a` from
# module `time` to delay actions
from time import sleep as _s



user_name = getpass.getuser()
file_directory = ''.join(['C:\\Users\\', user_name,
                          '\\AppData\\Local\\Packages\
\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\
\\LocalState\\Assets'])
desktop_folder = ''.join(['C:\\Users\\', user_name, '\\',
                          'Desktop\\Spotlight Wallpapers'])

run_at_startup = True   # Set to False to not run this script at startup
if run_at_startup:
    with open(''.join(['C:\\Users\\', user_name, '\\AppData\\Roaming\
\\Microsoft\\Windows\\\Start Menu\\Programs\\Startup\
\\getSpotlightWallpapers.bat']), 'w') as startup:
        startup.write(f'python.exe "{__file__}"')

else:
    os.remove(''.join(['C:\\Users\\', user_name, '\\AppData\\Roaming\
\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\
\\getSpotlightWallpapers.bat']))


# Function to check if a file is landscape or potrait
def is_landscape(image, width_dimension):
    """Returns True if image is a landscape;
else returns False (i.e. image is a potrait)
"""
    if int(width_dimension) == width_dimension:
        width_dimension = int(width_dimension)
        
    # Read image file in binary for dimensions
    with open(image, 'rb') as img:
        img.seek(163)
        width = float((img.read(2)[0] << 8) + img.read(2)[1])
        
    if int(width) == width:
        width = int(width)

    if width == width_dimension:
        # Image is potrait; return False
        return False

    # Image is landscape; return True
    return True


# Function `get_spotlight_wallpapers` to get only
# landscape spotlight wallpapers and not potraits
# or application icons in ICO, JPG etc. formats
def get_spotlight_wallpapers(save_directory=None, file_format='png',
                             make_desktop_folder=False):
    """Function *get_spotlight_wallpapers* to get only
landscape spotlight wallpapers and not potraits
or application icons in ICO, JPG etc. formats
"""
    global user_name, file_directory, desktop_folder

    # Create the directory if it doesn't exist
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)
    
    # Check if a desktop folder already exists
    if os.path.isdir(desktop_folder):
        # Folder exists and should
        # be deleted for a new one
        shutil.rmtree(desktop_folder)

    # Create a fresh new folder to add images
    os.makedirs(desktop_folder)

    for image in os.listdir(file_directory):
        # Check if image is wallpaper or app icon
        if os.stat(''.join([file_directory, '\\',
                             image])).st_size >= 150000:
            # Image is a wallpaper and needs to be copied
            # to the desktop folder (as a *file_format*)
            shutil.copyfile(''.join([file_directory, '\\', image]),
                            ''.join([desktop_folder, '\\',
                                     image, '.', file_format]))
    
    # Check max width to help determine orientation
    max_width = []
    for wallpaper in os.listdir(desktop_folder):
        with open(''.join([desktop_folder,
                           '\\', wallpaper]), 'rb') as wall:
            wall.seek(163)
            max_width.append(float((wall.read(2)[0] << 8)
                                   + wall.read(2)[1]))
    dimension = max(max_width)

    for wallpaper in os.listdir(desktop_folder):
        # Check if wallpaper is potrait or landscape
        if is_landscape(''.join([desktop_folder,
                                 '\\', wallpaper]), dimension):
            # Wallpaper is landscape and needs
            # to be copied to *save_directory*
            shutil.copyfile(''.join([desktop_folder, '\\', wallpaper]),
                            ''.join([save_directory, '\\', wallpaper]))
        else:
            # Wallpaper is potrait and needs to
            # removed from the current folder
            os.remove(''.join([desktop_folder, '\\', wallpaper]))

    if not make_desktop_folder:
        shutil.rmtree(desktop_folder)

    return True


# Driver code
if __name__ == '__main__':
    save_dir = input('Save location: ')
    
    if save_dir == '' or save_dir.isspace():
        # Add your default wallpapers folder here
        save_dir = 'G:\\Wallpapers'
    else:
        save_dir = save_dir.replace('/', '\\')
        
    format_ = input('Image format: ')

    if format_ == '' or format_.isspace():
        # Add your desired picture format
        # (refer the list below: *The list*)
        format_ = 'png'
    else:
        format_ = format_.lower()

        if format_ not in ['bmp', 'bpg', 'gif', 'jpeg',     # The list
                           'jpg', 'png', 'svg', 'tiff']:
            print(f"Image format can't be '{format_}'; \
defaulting to 'png' format")
            format_ = 'png'

    make_desktop_folder = input('Would you like to have a desktop \
folder too?\nYes (Y) / No (N) -> ')
    
    if make_desktop_folder.lower() in ['1', 'okay', 't', 'true', 'y',
                                       'yea', 'yeah', 'yep', 'yes']:
        make_desktop_folder = True
    else:
        make_desktop_folder = False

    got_wallpapers = get_spotlight_wallpapers(save_dir, format_,
                                              make_desktop_folder)

    print()
    if got_wallpapers:
        print('Done!')
    else:
        print('Some error ocurred, please check and try again...')
    
    # Delay quitting of program when running directly
    # (opened by double-clicking on the python file)
    _s(2.5)
