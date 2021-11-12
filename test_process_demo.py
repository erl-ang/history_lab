import streamlit as st
import PyPDF2 as ppdf
import base64
import pandas as pd

# nlp packages
import spacy
from spacy import displacy

# global vars for site copy
MAIN_TITLE_TEXT = 'Explore Text Processing Pipelines\n'
TITLE_DESCRIPTION = '*Built for http://history-lab.org/*\n'

DET_ARCHS = ['PyPDF2', 'Other OCR Method to test', 'filler']
NER_ARCHS = ["spaCy English (en_core_web_sm)", "BERT"]

def main():
	# Wide mode
	st.set_page_config(layout="centered")
	# Designing the interface
	st.title(MAIN_TITLE_TEXT)
	st.write(TITLE_DESCRIPTION)
	st.subheader("Uploaded PDF")

	# Sidebar
	# File selection
	st.sidebar.title("Document selection")
	# Disabling warning
	st.set_option('deprecation.showfileUploaderEncoding', False)
	# Choose your own image
	uploaded_file = st.sidebar.file_uploader("Upload files", type=['pdf'])

	# Model selection -- setting up UI for future use
	st.sidebar.title("Model selection")
	det_arch = st.sidebar.selectbox("OCR Method", DET_ARCHS)
	ner_arch = st.sidebar.selectbox("NER Model", NER_ARCHS)
	button = st.sidebar.button("Analyze Page")

	if uploaded_file is None:
		st.info('Please upload a document')
		st.subheader("Text Extracted")
		st.info('Upload a document')
		st.subheader("Show Named Entities")
		st.info('Please upload a document')


	else:
		with st.container():
			# Displaying markdown instead
			pdf_html = get_pdf_html_iframe(uploaded_file)
				
			st.markdown(pdf_html, unsafe_allow_html=True)

		# attempt to extract text
		with st.container():
			st.subheader("Text Extracted")

			ppdf_reader = ppdf.PdfFileReader(uploaded_file)
			page_idx = st.sidebar.selectbox("Page selection", [idx + 1 for idx in range(ppdf_reader.numPages)]) - 1
			ppdf_page = ppdf_reader.getPage(page_idx)
			page_text = ppdf_page.extractText()

			st.write(f'{get_html(page_text)}',  unsafe_allow_html=True)
			# st.write(page_text)
			
		# analyze the text
		with st.container():
			st.subheader("Show Named Entities")

			# tokenize text
			doc = get_spacy_en_doc(page_text)
			nlp_result = entity_analyzer(doc)
			st.json(nlp_result)
			
			# use displacy to visualize NER results
			# style = "<style>mark.entity { display: inline-block }</style>"
			html = displacy.render(doc, style="ent")
			st.write(f'{get_html(html)}',  unsafe_allow_html=True)
			st.dataframe(get_entity_df(doc))
			

	# For newline
	st.sidebar.write('\n')

def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")
    formatted_html = WRAPPER.format(html)
    styled_html = "<style>mark.entity { display: inline-block }</style>" + formatted_html
    return styled_html

def text_analyzer(file_text):
	"""
	Uses spacy to tokenize my_text

	Params:
	file_text (String): 
	"""
	nlp = spacy.load("en_core_web_sm")

	docx = nlp(file_text)
	
	# tokens = [token.text for token in docx]
	allData = [('"Tokens":{},\n"Lemma:{}'.format(token.text, token.lemma_)) for token in docx]
	return allData

def entity_analyzer(doc):
	"""
	Uses spacy to apply NER

	Params:
	"""
	tokens = [token.text for token in doc]
	entities =[(entity.text, entity.label_) for entity in doc.ents]
	allData = [('"Tokens":{},\n"Entities:{}'.format(tokens, entities)) for tokens in doc]

	return allData

def get_spacy_en_doc(file_text):
	"""
	helper so i don't have to keep fucking running things
	"""
	nlp = spacy.load('en_core_web_sm')
	doc = nlp(file_text)
	return doc

def get_entity_df(doc):
	"""
	"""
	attrs = ["text", "label_", "start", "end", "start_char", "end_char"]
	data = [
                [str(getattr(ent, attr)) for attr in attrs]
                for ent in doc.ents
        	]
	df = pd.DataFrame(data, columns=attrs)
	return df


def get_pdf_html_iframe(file):
	base64_pdf = base64.b64encode(file.read()).decode('utf-8')
	pdf_html_iframe = f'<iframe src="data:application/pdf;base64,{base64_pdf}"\
			 width="700" height="400" type="application/pdf">\
			</iframe>'
	return pdf_html_iframe

if __name__ == '__main__':
    main()