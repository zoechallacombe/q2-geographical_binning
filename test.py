import biom
import pandas as pd
import pandas.testing as pdt
import numpy as np
import skbio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap #dont need
from shapely.geometry import Point, Polygon
import unittest
import qtrees
from io import StringIO
import numpy.testing as npt
#test every path through code including exception raising for comprehension

class BasicTest(unittest.TestCase):
        def setUp(self):
            #setup function for data creation

            #set the starting input
            test_points = [['test_id_sw1', -180.0, -90.0],['test_id_nw1', -180, 90],
                ['test_id_ne1', 180, 90], ['test_id_se1', 180, -90],
                ['test_id_sw2', -91.0, -45.0],['test_id_nw2', -91, 45],
                ['test_id_ne2', 91, 45], ['test_id_se2', 91, -45]]

            test_df = pd.DataFrame(test_points, 
                columns = ['index', 'latitude', 'longitude'])
        
            self.test_df = test_df.set_index("index")
            
            #create answer dataframe
            correct_point = [['test_id_sw1', '1sw;', '1sw;2sw;'], 
                ['test_id_nw1', '1nw;', '1nw;2nw;'],
                ['test_id_ne1', '1ne;', '1ne;2ne;'],
                ['test_id_se1', '1se;', '1se;2se;'],
                ['test_id_sw2', '1sw;', '1sw;2nw;'],
                ['test_id_sw2', '1nw;', '1nw;2sw;'],
                ['test_id_sw2', '1ne;', '1ne;2se;'],
                ['test_id_sw2', '1se;', '1se;2ne;']]
            
            #Set the correct dataframe
            correct_dataframe = pd.DataFrame(correct_point, 
                columns=['index', 'H1', 'H2'])
            self.correct_dataframe = correct_dataframe.set_index('index')
            
            #set the correct tree
            self.correct_tree = skbio.TreeNode.read(StringIO("(('1sw;2sw','1sw;2nw')'1sw',('1nw;2nw','1nw;2sw')'1nw',('1se;2se', '1se;2ne')'1se', ('1ne;2ne','1ne;2se')'1ne')root;"))
            #check the string, maybe semicolons wont work. Also no spaces

        ##test reading in and reading out?
        
        #clean dataframe tests
        def test_clean_df(self):
            incorrect_points = [['test_id_sw', -180, -90],
                ['test_id_nw', -180, 90],['test_id_ne', 180, 90], 
                ['test_id_se', 180, -90],
                ['test_id_np', "Not provided", "Not provided"],
                ['test_id_na', "", ""]]
            to_clean_dataframe = pd.DataFrame(incorrect_points, 
                columns=['index', 'longitude', 'latitude'])
            to_clean_dataframe = to_clean_dataframe.set_index('index')

            
            correct_cleaned_points = [['test_id_sw', 0, 0],
                ['test_id_nw', 0, 180],['test_id_ne', 360, 180], 
                ['test_id_se', 360, 0]]
            
            correct_cleaned_df =pd.DataFrame(correct_cleaned_points, 
                columns = ['index', 'longitude', 'latitude'])

            correct_cleaned_df = correct_cleaned_df.set_index("index")
            

            correct_cleaned_df['latitude'] = correct_cleaned_df['latitude'].astype(float)
            correct_cleaned_df['longitude'] = correct_cleaned_df['longitude'].astype(float)

            
            cleaned =qtrees.clean(to_clean_dataframe)
            pdt.assert_frame_equal(cleaned, correct_cleaned_df)
            

            lat_long_str_pts = [['test_id_np', "Not provided", "Not provided"],
                ['test_id_na', "", ""]]
            str_only_df = pd.DataFrame(lat_long_str_pts,
                columns=['index', 'longitude', 'latitude'])
            str_only_df = str_only_df.set_index('index')


            with self.assertRaises(ValueError): 
                str_cleaned = qtrees.clean(str_only_df)
            
        def test_bin_by_quadtrees(self):
            
            tree, samples = qtrees.get_results(self.test_df, 2)
            
            print(tree.ascii_art())
            with self.assertRaises(ValueError):
                tree=self.correct_tree
            print(samples)
                #goals 100% code coverage
                #level of detail may just excercise the code
                #test on the outer function (working through the stuff)
                #seperate test for inner
                #test names are correct
                #test correct outputs
if __name__ == '__main__':
    unittest.main()                
