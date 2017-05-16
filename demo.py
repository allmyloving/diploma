from data import utils
import functions

functions.load_train_data(100, 'en')
data = utils.retrieve_train_data('en')
