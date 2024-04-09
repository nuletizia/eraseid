import os
import sys
import json
import argparse
from io import BytesIO
from random import randint
from PIL import Image, ImageFile, ImageFilter

from eraseid_utils import process_single_image
from eraseid_api import open_image_from_path, open_image_from_url, start_call


if __name__ == '__main__':


    parser = argparse.ArgumentParser()

    parser.add_argument('--hair', help='Change also the hair', action='store_true')
    parser.add_argument('--all_faces', help='Change all the faces in the photo', action='store_true')
    parser.add_argument('--url', help='Image file url', type=str, default='https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')
    parser.add_argument('--filepath', help='Input image file absolute path', type=str, default=None)

    parser.add_argument('--identity_filepath', help='Input identity file absolute path', type=str, default=None)
    parser.add_argument('--identity_name', help='Use the face from the stored identities', default=None)
    parser.add_argument('--store_identity', help='Save the generated identity under the name pippo', action='store_true')

    parser.add_argument('--guidance_scale', help='Guidance scale', type=str, default=None)
    parser.add_argument('--prompt_strength', help='Description strength', type=str, default=None)
    parser.add_argument('--controlnet_scale', help='Conditioning scale', type=str, default=None)
    parser.add_argument('--seed', help='Generation seed', type=int, default=randint(0,100000))


    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("ERASEID_EMAIL")
    PASSWORD = os.getenv("ERASEID_PASSWORD")

    # Parameters
    CHANGE_HAIR = args.hair # False if only the face is anonymized, True if both face and hair
    CHANGE_ALL_FACES = args.all_faces # False if only a subset of the faces in the image need to be anonymize, True if all the faces

    # Consistent identity parameters
    IDENTITY_PATH = args.identity_filepath
    IDENTITY_NAME = args.identity_name # Default is None, otherwise a string of a stored name
    STORE_IDENTITY_FLAG = args.store_identity # False if the new identity shall not be saved in the user profile, viceversa True

    # Generation parameters
    GUIDANCE_SCALE = args.guidance_scale
    PROMPT_STRENGTH = args.prompt_strength
    CONTROLNET_SCALE = args.controlnet_scale
    SEED = args.seed

    # Image parameters
    URL = args.url 
    INPUT_PATH = args.filepath

    if INPUT_PATH is not None:
        if os.path.exists(INPUT_PATH):
            input_image = open_image_from_path(INPUT_PATH)
            print(f'Using as input image the file located at: {INPUT_PATH}')
        else:
            print('Wrong filepath, check again')
            sys.exit()
    else:
        try:
            input_image = open_image_from_url(URL)
            print(f'Using as input image the file located at: {URL}')
        except:
            print('Wrong URL, check again')
            sys.exit()

    if IDENTITY_PATH is not None:
        if os.path.exists(IDENTITY_PATH):
            identity_image = open_image_from_path(IDENTITY_PATH)
            print(f'Using the input identity file located at: {IDENTITY_PATH}')
        else:
            print('Wrong identity filepath, check again')
            sys.exit()

    # log in
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)

    HAIR_FACTOR = 1 if CHANGE_HAIR else 0

    PARAM_DICTIONARY = {
            'INPUT_PATH':INPUT_PATH,
            'HAIR_FACTOR':HAIR_FACTOR,
            'CHANGE_ALL_FACES':CHANGE_ALL_FACES,
            'IDENTITY_IMAGE':identity_image,
            'IDENTITY_NAME':IDENTITY_NAME,
            'STORE_IDENTITY_FLAG':STORE_IDENTITY_FLAG,
            'SEED':SEED,
            'GUIDANCE_SCALE': GUIDANCE_SCALE,
            'PROMPT_STRENGTH': PROMPT_STRENGTH,
            'CONTROLNET_SCALE': CONTROLNET_SCALE,
        }

    response = process_single_image(input_image, PARAM_DICTIONARY, TOKEN_DICTIONARY) 
