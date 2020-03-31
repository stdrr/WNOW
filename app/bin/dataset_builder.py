# =============================================================================
# This class provides a method to build a dataset from Wikipedia's content
# =============================================================================

from bin.mywiki import Wiki
import pandas as pd
from bin.text_tools import TextTools

class DatasetBuilder:
    def __init__(self):
        self.wiki = Wiki()
        
    def build(self, categories: list, pages_num=30, out_file_name='dataset', processed=False):
        dataset = pd.DataFrame(data={'text':[], 'category':''})
        for category in categories:
            result = self.wiki.get_raw_category_pages(category, pages_num=pages_num)
            tmp_dataset = pd.DataFrame(data=result)
            dataset = dataset.append(tmp_dataset, ignore_index=True)
            print('\n')
        print('\nDataset info: ', dataset.info())
        if processed:
            print('\nProcessing data...')
            t_tools = TextTools()
            dataset['text'] = dataset['text'].apply(lambda t: t_tools.preprocess(t))
            print('Processing data...DONE', end='\n\n')
        out_file = open(out_file_name+'.csv', 'w', newline='')
        dataset.to_csv(out_file, float_format='str', index=False)
        out_file.close()