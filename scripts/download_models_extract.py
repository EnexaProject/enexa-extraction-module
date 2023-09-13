
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("ibm/knowgl-large")
model = AutoModelForSeq2SeqLM.from_pretrained("ibm/knowgl-large")

