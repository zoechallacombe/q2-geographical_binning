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
            test_points = [['test_id_sw1', -180.0, -90.0],
                ['test_id_nw1', -180, 90],
                ['test_id_ne1', 180, 90],
                ['test_id_se1', 180, -90],
                ['test_id_sw2', -91.0, -44.0],
                ['test_id_nw2', -91, 44],
                ['test_id_ne2', 91, 44], 
                ['test_id_se2', 91, -44]]
            test_df =pd.DataFrame(test_points,
                columns = ['index', 'longitude', 'latitude'])
            
            test_df['latitude'] = test_df['latitude'] + 90

            test_df['longitude'] = test_df['longitude'] + 180

            self.test_df = test_df.set_index("index")
            
            #create answer dataframe
            correct_point = [['test_id_sw1', '0sw;', '0sw;1sw;'], 
                ['test_id_nw1', '0nw;', '0nw;1nw;'],
                ['test_id_ne1', '0ne;', '0ne;1ne;'],
                ['test_id_se1', '0se;', '0se;1se;'],
                ['test_id_sw2', '0sw;', '0sw;1nw;'],
                ['test_id_nw2', '0nw;', '0nw;1sw;'],
                ['test_id_ne2', '0ne;', '0ne;1se;'],
                ['test_id_se2', '0se;', '0se;1ne;']]
            
            #Set the correct dataframe
            correct_dataframe = pd.DataFrame(correct_point, 
                columns=['index', 'H1', 'H2'])
            self.correct_dataframe = correct_dataframe.set_index('index')
            
            #set the correct tree
            self.correct_tree = skbio.TreeNode.read(StringIO("(('1sw;2sw','1sw;2nw')'1sw',('1nw;2nw','1nw;2sw')'1nw',('1se;2se', '1se;2ne')'1se', ('1ne;2ne','1ne;2se')'1ne')root;"))
            #check the string, maybe semicolons wont work. Also no spaces

        
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
            
        def test_get_results_outer(self):
            threshold = 2
            test_tree, test_samples = qtrees.get_results(self.test_df, threshold)
            pdt.assert_frame_equal(test_samples, self.correct_dataframe) 

            print(test_tree.ascii_art())
            print(self.correct_tree.ascii_art())
            self.assertTrue(test_tree.compare_subsets(self.correct_tree))
            #self.assertTrue(test_tree.compare_tip_distances(self.correct_tree))
            #tree is violently not working

        def test_threshold(self):
            threshold = 1
            with self.assertRaises(ValueError):
                tree_1, samples_1 = qtrees.get_results(self.test_df, threshold)
            
            threshold = 4
            correct_point_4 = [['test_id_sw1', '0sw;'],
                ['test_id_nw1', '0nw;'],
                ['test_id_ne1', '0ne;'],
                ['test_id_se1', '0se;'],
                ['test_id_sw2', '0sw;'],
                ['test_id_nw2', '0nw;'],
                ['test_id_ne2', '0ne;'],
                ['test_id_se2', '0se;']]

            #Set the correct dataframe
            correct_dataframe_4 = pd.DataFrame(correct_point_4,
                columns=['index', 'H1'])

            correct_dataframe_4 = correct_dataframe_4.set_index('index')
            tree_4, samples_4 = qtrees.get_results(self.test_df, threshold)
            pdt.assert_frame_equal(samples_4, correct_dataframe_4)
            
            #what to do when threshold is higher than number of samples
            threshold = 9
            tree_8, samples_8 = qtrees.get_results(self.test_df, threshold)
            print("~", samples_8)

        #outer to inner methods or visa versa
        
        def test_boundaries(self):
            #question how best to test?
            #if testing the same data frame twice, testing the same points in different positions?
            boundary_points = [['test_1', 180, 90],
                ['test_2', 90, 90],
                ['test_3', 180, 45],
                ['test_4', 180, 135],
                ['test_5', 360.0, 90.0]]

            boundary_df =pd.DataFrame(boundary_points,
                columns = ['index', 'longitude', 'latitude'])
            boundary_df = boundary_df.set_index('index')
            

            boundary_points_mixed = [['test_2', 90, 90],
                ['test_1', 180, 90],
                ['test_4', 180, 135],
                ['test_3', 180, 45],
                ['test_5', 360.0, 90.0]]

            boundary_df_mix =pd.DataFrame(boundary_points_mixed,
                columns = ['index', 'longitude', 'latitude'])
            boundary_df_mix = boundary_df_mix.set_index('index')
            tree, samples = qtrees.get_results(boundary_df, 4)
            tree_mix, samples_mix = qtrees.get_results(boundary_df_mix, 4)
            print(samples_mix, samples)
            pdt.assert_frame_equal(samples_mix, samples)

        def test_contains(self):
            

        #def test_bin_by_quadtrees(self):
            #test binning correct with small threshold k = 2, and larger k = 3-4 <-done
            #test binning is consitent when on the divide between quadrants
            #test correct output for binned and samples, 
            #tree, samples = qtrees.get_results(self.test_df, 2)
            #print(samples) 
            #print(tree)
            #print(tree.ascii_art())
            #with self.assertRaises(ValueError):
            #    tree=self.correct_tree
            #print(samples)
                #goals 100% code coverage
                #level of detail may just excercise the code
                #test on the outer function (working through the stuff)
                #seperate test for inner
                #test names are correct
                #test correct outputs
if __name__ == '__main__':
    unittest.main()                
