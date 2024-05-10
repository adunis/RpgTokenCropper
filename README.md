The program take a list of folders as inputs, broswe in them and convert the images found in a token image with progressive names in this format:

[directory_name]_[file_number]_circular.png

Then it proceeds to delete the original images (in the future a toggle option to mantain the original images would be included)

Usage:

- Set a directory path in the "directory_path" parameter. For example (directory_path = 'C:/portraits')
- Set a path for the image of the border to apply on the token in the "border_path" parameter. For example (border_path = 'C:/border.png')
- Put the folder with the images under the path choosen in the "directory_path" parameter. For example ('C:/portraits/DRAGONS')
- Choose a "param_border" parameter, this define the percentage of resize applyed to the image compared to the border size, this is optional and used to avoid bad overlap between border and the image to tokenize. For example if the border is 256x256, with a param_border of 0.85 the image to tokenize will be resised to 220x220. With a param_border of 1 the image won't be resized (this option is here because of the different size of the border choosen)
- If optional parameter "paste_the_border" if set to False, then the program will not apply the border to the image and only crop it.

So for example with a folder set like this: ('C:/portraits/DRAGONS') and with 2 files inside DRAGONS folder the results will be:

-DRAGONS_1_circular.png
-DRAGONS_2_circular.png
