# Solution
Directory with my solution to the assignment: Gaffuri Riva Filippo.

For this project i created a class solution which takes as input the three user input required by the assignment:
- the xml input dir
- the image input dir
- the output dir in which new images and the json are going to be saves.

With the python module parser we parse the file and using xml.etree.ElementTree 
and we build the dictionaries required retrieving the necessary values. Furthermore if
image has to be modified we modified the image shrinking it at the dimension (800,450)
and modifying in case also the parameters of the bounding box. To modify such parameters
we first compute the center of the box using its coordinates and we later calculate the new
width and height by dividing the actual dimensions for the ratio given by (ratio_height: original_height/800, 
ratio_width: orginal_width/450. Nb this is done separately for each dimension, in order to be sure
that if only the height is higher than 800 then it's the only dimension of bbox to be modified and viceversa).

Each id for the images is unique since it's generated using a timestamp. 

Each image is resized to the possibly new shape using the Library Pillow. 

