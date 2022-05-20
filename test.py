import os
import sys
from PIL import Image, ImageOps
  
# define a function for
# compressing an image
# def compressMe(file, verbose = False):
    
    # Get the path of the file
    # filepath = os.path.join(os.getcwd(), 
    #                         file)
      
    # open the image
    
      
    # Save the picture with desired quality
    # To change the quality of image,
    # set the quality variable at
    # your desired level, The more 
    # the value of quality variable 
    # and lesser the compression

#     picture = Image.open(file)

#     thumi = picture.copy()

#     # # thumi.thumbnail(thum, Image.LANCZOS)
#     # picture = picture.resize((448, 615), Image.ANTIALIAS)
#     # picture = ImageOps.exif_transpose(picture)
#     # picture.save("c"+file, "JPEG", optimize = True, quality = 10)
#     # thumi = ImageOps.exif_transpose(thumi)
#     # thumi.save("c"+file, "JPEG", optimize = True, quality = 10)
#        # Get dimensions

#     new_width, new_height = 448, 615

#     width, height = picture.size

#     left = (width - new_width)/2
#     top = (height - new_height)/2
#     right = (width + new_width)/2
#     bottom = (height + new_height)/2

# # # Crop the center of the image
#     picture = picture.crop((200, 300, 700, 600))
#     picture = ImageOps.exif_transpose(picture)
#     picture.save("c"+file, "JPEG", optimize = True, quality = 10)
    
#     return True

  
# # Define a main function
# def main():
    
#     verbose = True
      
#     # checks for verbose flag
#     if (len(sys.argv)>1):
        
#         if (sys.argv[1].lower()=="-v"):
#             verbose = True
                      
#     # finds current working dir
#     cwd = os.getcwd()
  
#     formats = ('.jpg', '.jpeg')
      
#     # looping through all the files
#     # in a current directory
#     for file in os.listdir(cwd):
        
#         # If the file format is JPG or JPEG
#         if os.path.splitext(file)[1].lower() in formats:
#             print('compressing', file)
#             compressMe(file, verbose)
  
#     print("Done")
  

# print(compressMe("1640438328233.JPG"))

def make_square(im, min_size=1080, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

test_image = Image.open('static/uploads/1/2020-02-15 18.39.02_1.JPG')
test_image = ImageOps.exif_transpose(test_image)
new_image = make_square(test_image)
new_image.save("2020", "JPEG", optimize = True, quality = 10)

2020-02-15 18.39.02_1.JPG
2020-02-15_18.39.02_1.JPG