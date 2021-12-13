from solution import Solution

#final app. 
#Is is only required for the user to input the three path required by the assignement to generate the json and the other files. 
imagedir = 'insert input dir for images'
xmldir ='inser input dir for xml files'
outputdir = 'insert output dir'

sol = Solution(imagedir,xmldir,outputdir)

sol.save_json()


