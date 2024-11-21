import os
import unittest
from unittest.mock import patch, mock_open
from services.CSVService import CSVService

class TestCSVService(unittest.TestCase):
    @patch('os.listdir') # Mocking the os.listdir function to simulate listing files in a directory.
    @patch('os.path.exists') # Mocking the os.path.exists function to simulate checking for the existence of a directory.
    def test_count_files(self, mock_exists, mock_listdir):
        
        # We simulate that the directory exists by returning True.
        mock_exists.return_value = True
        # We simulate the files in the directory.
        mock_listdir.return_value = ['file1.csv', 'file2.csv']

        # We create an instance of the CSVService class.
        service = CSVService()
        # We call the count_files method to get the number of files.
        count = service.count_files()

        # Finally, we assert that the count of files is equal to 2.
        self.assertEqual(count, 2)

    @patch('os.path.exists') # Mocking the os.path.exists function to simulate checking the existence of a directory.
    @patch('os.makedirs') # Mocking the os.makedirs function to simulate creating a directory.
    @patch('builtins.open', new_callable=mock_open)  # Mocking the open function to simulate file operations.
    def test_save_new_csv(self, mock_file, mock_makedirs, mock_exists):
        # We simulate that the directories do not exist on the first call (initialize_directories)
        # And that the csv_files directory does not exist on the fourth call (count_files)
        # Also that the csv_files directory does not exist on the fifth call (count_files in this test function)
        # but he does from the sixth call
        # (in order to check if the open(service.references_file_path, 'w'))
        # and mock_file.assert_any_call(os.path.join(service.csv_folder_path, csv_path), 'w') are called.
        mock_exists.side_effect = [False, False, False, False, False, True]
        
        # We create an instance of the CSVService class.
        service = CSVService()

        # We define some random edges, nodes, image_path
        edges_matrix = [[0, 1], [1, 0]]
        nodes = {0 : (200, 100), 1 : (100, 200)}
        image_path = 'image2.jpg'
        
        # We call the save method to execute the functionality being tested
        service.save(edges_matrix, nodes, image_path)

        # We assert that makedirs was called two times.
        # If not, it means that one directory has'nt been created: csv_files or references
        # or has been created more than two
        self.assertEqual(mock_makedirs.call_count, 2)

        # We get the number of CSV files.
        nb_files = service.count_files()
        # We generate the path for the new CSV file.
        csv_path = f"graph_{nb_files + 1}.csv"

        # We check if the references file was opened for writing.
        # The mock_exists is now turned to true in order to enter to the open condition
        mock_file.assert_any_call(service.references_file_path, 'w')

        # And then we check if the new CSV file was opened for writing.
        mock_file.assert_any_call(os.path.join(service.csv_folder_path, csv_path), 'w')

        # We get the handle for the mocked file.
        handle = mock_file()
        
        # We verify that the write method was called with the expected data in the CSV.
        handle.write.assert_any_call(f'{image_path},{csv_path}\n')
        
        # We assert that 'image1.jpg,None' was not written to the file
        # the path of the graph must indeed be written as second argument
        assert 'image1.jpg,None' not in handle.write.call_args_list

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_existing_csv(self, mock_file, mock_makedirs, mock_exists):
        mock_exists.side_effect = [True, True, True, False]
        
        # We create an instance of the CSVService class.
        service = CSVService()

        # We define some random edges, nodes, image_path
        edges_matrix = [[0, 1], [1, 0]]
        nodes = {0 : (200, 100), 1 : (100, 200)}
        image_path = 'image1.jpg'

        # We prepare a simulated content for the references.csv file
        mock_file.return_value.__iter__.return_value = iter([f"{image_path},graph_1.csv\n"])
        
        # We call the save method to execute the functionality being tested
        service.save(edges_matrix, nodes, image_path)

        # We make sure that the initialize_directories method didn't create any folder
        self.assertEqual(mock_makedirs.call_count, 0, "No other directories must be created")

        # We check if the write_csv_information method was called in order to change graph_1.csv
        mock_file.assert_any_call(os.path.join(service.csv_folder_path, "graph_1.csv"), 'w')

        # We get the handle for the mocked file.
        handle = mock_file()
        
        # We verify that de services wrote Nodes, into the file
        handle.write.assert_any_call("Nodes,")
        # And we verify that for each node, the data writen is the correct one
        for node in nodes.values():
            handle.write.assert_any_call(f'{node},')
        handle.write.assert_any_call("\n")
        
        # We check that the edges matrix has been writting into the csv file
        for row in edges_matrix:
            handle.write.assert_any_call(",".join(str(cell) for cell in row) + "\n")

        # Finally, we verify the reference of the image
        handle.write.assert_any_call(f'Image_ref,{image_path}\n')

    @patch('builtins.open', new_callable=mock_open, read_data='image1.jpg,graph_1.csv\n')
    def test_find_csv_reference_found(self, mock_file):
        service = CSVService()
        # We call the method find_csv_reference with the image path 'image1.jpg'
        result = service.find_csv_reference('image1.jpg')
        
        # We assert that the result returned from the method is equal to 'graph_1.csv'
        self.assertEqual(result, 'graph_1.csv')

    @patch('builtins.open', new_callable=mock_open, read_data='path/to/image.png,1.csv\n', )
    def test_find_csv_reference_not_found(self, mock_file):
        service = CSVService()

        # We call the method find_csv_reference with a non-existent image path.
        result = service.find_csv_reference('path/to/nonexistent_image.png')

        # We assert that the result is None since the image path does not exist in the mocked data.
        self.assertIsNone(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_load_file_exists(self, mock_exists, mock_file):
        # This test method is currently empty because the test for the file loading functionality 
        # is under development. A future implementation will verify that the file loads correctly 
        # when the file exists.
        pass

    @patch('os.path.exists')
    def test_load_file_does_not_exist(self, mock_exists):
        # We set the mock to return False, simulating that the file does not exist.
        mock_exists.return_value = False

        service = CSVService()
        # We attempt to load data using index of 1, but the file doesn't exists in any case in the mock data.
        edges_matrix, nodes_list = service.load_from_num_file(1)

        # We assert that both edges_matrix and nodes are None since the file does not exist.
        self.assertIsNone(edges_matrix)
        self.assertIsNone(nodes)
