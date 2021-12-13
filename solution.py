#importing libraries
import xml.etree.ElementTree as ET
from PIL import Image
import numpy
import datetime
import os
import json 



class Solution:
    
    def __init__(self, imagedir, xmldir, outputdir):
        
        """
        args: 
             -imgedir(str): path of input images
             -xmldir(str):path of input xmlfiles
             -outputdir(str):path of the output dir with saved json and new images
        """
        self.imagedir = imagedir
        self.xmldir = xmldir
        self.outputdir = outputdir
    
    
    def parser(self, xml_file, image_file, cateogory_id):
        
        """function that returns the dictionary of a single xml file.
        args: -xml_file (str): path of the current xml file
              -category_id(int): category id to be given to the dictionary catagory.
        """
        
        
    
        outdir =  self.outputdir
    
    
        id_ = xml_file.split('/')[-1].replace('.xml','')
        id_ = id_ + datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        tree = ET.parse(xml_file)
        root = tree.getroot()
    
        image = {}
        for element in root.findall('path'):
            imname = element.text
    
        imname = self.imagedir+image_file.split('/')[-1]
        ratio_height = 1
        ratio_width = 1
        for element in root.findall('size'):
            for size_attr in element:
                if size_attr.tag!='depth':
                    image[size_attr.tag] = int(size_attr.text)
    
        if image['width']>800:
            ratio_width = image['width'] / 800 #saving this ratio to modify later the bounding box
            image['width'] = 800 #changing the shape
        

    
        if image['height']>450:
        
            ratio_height = image['height'] / 450 #saving this ratio to modify later the bounding box
            image['height'] = 450 #changing the shape
        
            
        
    
    
        image ['id'] = int(id_)
    
        for fname in root.findall('filename'):
        
            file_name = fname.text

        image['file_name'] = file_name
    
        new_img = Image.open(imname).resize((image['height'],image['width']))
    
    
        new_name = imname.split('/')[-1]
    
        new_img.save(outdir+new_name)
    
    #category
        category = {}
        x_coord = {}
        for element in root.findall('object'):
            for item in element:
            
                if item.tag=='name':
                    category['name'] = item.text
            
                elif item.tag=='bndbox':
                
                    for extreme in item:
                        x_coord[extreme.tag] = float(extreme.text)
    
        
        category['id'] = id_
                    
        category['supercategory'] = '?'
    
    #in this for following lines we rearrange the bbox coordinates by fixing the center 
    #and reshaping the box accordingly to how we reshaped the image
    
        new_width = (x_coord['xmax'] - x_coord['xmin']) / ratio_width
        new_height = (x_coord['ymax']-x_coord['ymin']) / ratio_height
    
        xc = (x_coord['xmax'] + x_coord['xmin']) / 2
        yc = (x_coord['ymax'] + x_coord['ymin']) / 2
    
  
    
        annotation = {}
        ann_id = id_
        annotation['id'] = ann_id
        annotation['image_id'] = image['id']
        annotation['category_id'] = category['id']
        bbox = [xc, yc, new_width, new_height]
    
        annotation['category_id'] = category['id']
    
        return category, image, annotation

    def get_data(self):
        
        """
        function that return a dictionary with structure: key = 'xml_file_path',
        value = 'image_file_path'
        """
        
        xml_path = self.xmldir
        xml_file = [f for f in os.listdir(xml_path) if f.endswith('.xml')]
    
        image_path = self.imagedir
        jpg_file = [f for f in os.listdir(image_path) if f.endswith('.jpg')]
    
        files = {}
        for index, element in enumerate(xml_file):
            files[xml_path+element] = image_path+jpg_file[index]
        
        return files
    
    def return_total_dict(self):
        #function that return the dict calculated by pars for each of the file and then append them to the list
        #which are the values of the final dict to be saved in json.
        data = self.get_data()
        categories = []
        images = []
        annotations = []
        
        total_json = {}
        
        for xml_file in data:
            
            img_file = data[xml_file]
            
            categ_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            
            category, image, annotation = self.parser(xml_file,img_file,self.outputdir)
            
            categories.append(category)
            images.append(image)
            annotations.append(annotation)
            
        
        total_json['categories'] = categories
        total_json['images'] = image
        total_json['annotation'] = annotations
        
        self.total_json = total_json
        
        return self.total_json
    
    
    def save_json(self):
        
        total_json = self.return_total_dict()
        
        with open(self.outputdir+'data.json', 'w') as fp:
            json.dump(total_json, fp,  indent=4)
