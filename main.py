import streamlit as st

import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

STABILITY_HOST = "grpc.stability.ai:443"
STABILITY_KEY = st.text_input("STABILITY_KEY")

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

if st.button('Say hello'): 
	stability_api = client.StabilityInference(
		host=STABILITY_HOST,
		key=STABILITY_KEY, # API Key reference.
		verbose=True, # Print debug messages.
		engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
	)

	