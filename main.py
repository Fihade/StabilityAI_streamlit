import streamlit as st

import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

st.title("🎨 Try :blue[STABILITY AI]")

st.header("Setup")
STABILITY_HOST = "grpc.stability.ai:443"
STABILITY_KEY = st.text_input("STABILITY_KEY")
st.caption("🔑 Getting Your API Key from [here](https://beta.dreamstudio.ai/account)")

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

st.header("Description")
prompt = st.text_input("Prompt")
negative_prompt = st.text_input("Negative Prompt")


st.header("Advanced Setting")
col1, col2 = st.columns(2)

with col1:
	sampler = st.selectbox("Sampler", 	(
		'ddim', 'plms', 'k_euler', 'k_euler_ancestral', 'k_heun', 'k_dpm_2', 'k_dpm_2_ancestral', 'k_dpmpp_2s_ancestral', 'k_lms', 'k_dpmpp_2m'
	))
	scale = st.number_input("CFG Scale", value=7, min_value=0)
	seed = st.number_input("seed", value=-1, min_value=-1)
	count = st.number_input("image count", value=1, min_value=1)
with col2:
	steps = st.number_input("steps", value=30, min_value=1)
	width = st.number_input("width", value=512)
	height = st.number_input("height", value=512)

if st.button('Say hello'):
	print(
		f"""
		host: {STABILITY_HOST}\n key: {STABILITY_KEY}\n prompt: {prompt}\n negative: {negative_prompt}\n sampler: {sampler}\n seed: {seed}\n scale={scale}\n  count: {count}\n  steps: {steps}\n width: {width}\n height: {height}\n
		""")
	st.write(f"""
		host: {STABILITY_HOST}\n key: {STABILITY_KEY}\n prompt: {prompt}\n negative: {negative_prompt}\n sampler: {sampler}\n seed: {seed}\n scale={scale}\n  count: {count}\n  steps: {steps}\n width: {width}\n height: {height}\n
		""")
	stability_api = client.StabilityInference(
		host=STABILITY_HOST,
		key=STABILITY_KEY, # API Key reference.
		verbose=True, # Print debug messages.
		engine="stable-diffusion-xl-beta-v2-2-2", # Set the engine to use for generation.
	)
	
	answers = stability_api.generate(
		prompt="expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli",
		seed=992446758, # If a seed is provided, the resulting generated image will be deterministic.
		# What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
		# Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
		steps=30, # Amount of inference steps performed on image generation. Defaults to 30. 
		cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
		# Setting this value higher increases the strength in which it tries to match your prompt.
		# Defaults to 7.0 if not specified.
		width=512, # Generation width, defaults to 512 if not included.
		height=512, # Generation height, defaults to 512 if not included.
		samples=1, # Number of images to generate, defaults to 1 if not included.
		sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
		# Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
		# (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
	)
	
	# Set up our warning to print to the console if the adult content classifier is tripped.
	# If adult content classifier is not tripped, save generated images.
	for resp in answers:
		for artifact in resp.artifacts:
			if artifact.finish_reason == generation.FILTER:
				warnings.warn(
					"Your request activated the API's safety filters and could not be processed."
					"Please modify the prompt and try again.")
				if artifact.type == generation.ARTIFACT_IMAGE:
					img = Image.open(io.BytesIO(artifact.binary))
					st.image(img)
	


