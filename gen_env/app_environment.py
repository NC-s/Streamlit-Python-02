import sys
import subprocess
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime as st_runtime
from streamlit_jupyter import StreamlitPatcher, tqdm
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# As the app.py contains different encoding, we need to specify a environment variable
# cd gen_env
# python -m pipreqs.pipreqs --encoding utf-8 "./"
