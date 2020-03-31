from bin.dataset_builder import DatasetBuilder

topics = ['Category:Economy',
          'Category:Entertainment',
          'Category:Politics',
          'Category:Science',
          'Category:Sports',
          'Category:Technology']

my_builder = DatasetBuilder()
my_builder.build(categories=topics, out_file_name='45_dataset', pages_num=7500, processed=True)