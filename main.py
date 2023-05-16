import streamlit as st

import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

STABILITY_KEY = st.text_input("STABILITY_KEY","input stability ai key here")

option = st.selectbox(
	'Model:',
	(
		'stable-diffusion-v1', 
		'stable-diffusion-v1-5', 
		'stable-diffusion-512-v2-0',
		'stable-diffusion-768-v2-1',
		'stable-diffusion-768-v2-0',
		'stable-diffusion-512-v2-1',
		'stable-diffusion-768-v2-1',
		'stable-diffusion-xl-beta-v2-2-2'
	)
)

#stability_api = client.StabilityInference(
#	key=STABILITY_KEY, # API Key reference.
#	verbose=True, # Print debug messages.
#	engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
#)