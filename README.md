# history_lab

exploring potential dashboarding and data exploration tools for http://history-lab.org/ !

[Midterm presentation link for some more context](https://docs.google.com/presentation/d/1lVtBDouOF7UhwShfYNi-e1hWvoztE_VuZMqtXF0PJBU/edit?usp=sharing)

# Two ways to play with the app:
## 1. Running the app locally 

### Clone the repo
`git clone git@github.com:erl-ang/history_lab.git`

### Install Streamlit and dependencies
#### Installing Streamlit, Managing Python Environments.
Follow [these instructions to install Streamlit](https://docs.streamlit.io/library/get-started/installation)

Managing different versions of python is a pain. I recommend letting [Anaconda](https://www.anaconda.com/products/individual) manage your dependencies

#### Installing Dependencies via `conda`:
`conda install -c conda-forge pypdf2`

`conda install -c conda-forge spacy`

`python -m spacy download en_core_web_sm`

## 2. ORRRRR just visit a url on the deployed app :)
[url here-- let me know if you break anything that's not in the known issues!](https://share.streamlit.io/erl-ang/history_lab/test_process_demo.py)

### Known Issues:
* Browser marks the HTML PDF displayer as unsafe, so you won't be able to view your original uploaded pdf
* PyPDF2's text extraction is wonky
