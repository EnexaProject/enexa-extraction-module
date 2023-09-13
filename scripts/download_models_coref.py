
import nltk
from crosslingual_coreference import Predictor

nltk.download('punkt')
nltk.download('omw-1.4')

def create_dummy_predictor():
    predictor = Predictor(language="en_core_web_sm", device=-1, model_name="minilm")


# Create a dummy predictor to force the download of the model
create_dummy_predictor()

