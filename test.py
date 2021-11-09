import os
import streamlit as st
import PyPDF2 as ppdf
import base64

# from pdf2image import convert_from_bytes, convert_from_path

# global vars
DET_ARCHS = ['db_resnet50', 'db_mobilenet_v3_large', 'linknet16']
RECO_ARCHS = ["crnn_vgg16_bn", "master", "sar_resnet31"]


def main():
	# Wide mode
	st.set_page_config(layout="wide")
	# Designing the interface
	st.title("Testing: Text Processing")
	st.write('\n')
	st.write('Find more info at: http://history-lab.org/')
	st.write('\n')
	# Instructions
	st.markdown("*Hint: click on the top-right corner of an image to enlarge it!*")
	# Set the columns
	cols = st.columns((1, 1))
	cols[0].subheader("Input page")
	cols[1].subheader("Text Extracted")

	# Sidebar
	# File selection
	st.sidebar.title("Document selection")
	# Disabling warning
	st.set_option('deprecation.showfileUploaderEncoding', False)
	# Choose your own image
	uploaded_file = st.sidebar.file_uploader("Upload files", type=['pdf'])

	# Model selection -- setting up UI for future use
	st.sidebar.title("Model selection")
	det_arch = st.sidebar.selectbox("Text Extraction Model", DET_ARCHS)
	reco_arch = st.sidebar.selectbox("Redaction Model", RECO_ARCHS)
	button = st.sidebar.button("Analyze Page")

	if button and uploaded_file is not None:

		if uploaded_file.name.endswith('.pdf'):

			pdf_reader = ppdf.PdfFileReader(uploaded_file)

			page_idx = st.sidebar.selectbox("Page selection", [idx + 1 for idx in range(pdf_reader.numPages)]) - 1
			page = pdf_reader.getPage(page_idx)

			with st.container():
				"""
				trying to use pdf2image to display an uploaded pdf as an image instead
				"""
				# pdf_image = convert_from_bytes(uploaded_file.read())
				"""
				trying to use pdf2image to display a local pdf as an image
				"""
				# pdf_image = convert_from_path("~/Downloads/Liang_Erin_Resume.pdf")

				"""
				maybe use Doctr library?
				"""
				# pdf_image = DocumentFile.from_pdf(uploaded_file.read()).as_images()

				# display as an image
				# cols[0].image(pdf_image[page_idx])

				"""
				Displaying markdown instead
				"""
				# pdf_html = get_pdf_html_embed(uploaded_file)
				pdf_html =  get_pdf_html_iframe(uploaded_file)

				
				cols[0].markdown(pdf_html, unsafe_allow_html=True)
				# image_url = get_uploaded_image_url(uploaded_file)

				# possibly uploading to s3?
				# st.markdown(f'<iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url={image_url}" width="100%" height="1100">', unsafe_allow_html=True)

			# attempt to extract text
			with st.container():
				cols[1].write(page.extractText())

			# prints document information dictionary
			# st.write(pdf_reader.getDocumentInfo())
		else:
			st.write("Not Implemented Yet, Check Back Later")

	if uploaded_file is None:
			st.sidebar.write("Please upload a document")

	# For newline
	st.sidebar.write('\n')

def get_pdf_html_embed(file):
	base64_pdf = base64.b64encode(file.read()).decode('utf-8')
	pdf_html_embed = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1100" type="application/pdf">' 
	# parameterize dimensions later
	return pdf_html_embed

def get_pdf_html_iframe(file):
	base64_pdf = base64.b64encode(file.read()).decode('utf-8')
	pdf_html_iframe = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="1000" type="application/pdf"></iframe>'
	return pdf_html_iframe

if __name__ == '__main__':
    main()