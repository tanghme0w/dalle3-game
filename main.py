import os.path
import io
from openai import OpenAI
from joblib import Parallel, delayed
import requests
import numpy as np
from PIL import Image


debug = False
api_key = "your API key"
submission_file_name = "submission.txt"
submission_format = ["name", "theme", "prompt", "caption"]
themes = ["A卷 我的科研故事", "B卷 我眼中的年会"]
output_path = "output"
n_jobs = 3  # Number of parallel jobs


# read prompts
submissions = []
with open(submission_file_name) as fp:
    for i, line in enumerate(fp):
        entry_terms = line.strip('\n').split('\t')
        submission_entry = dict()
        for term_name, term in zip(submission_format, entry_terms):
            submission_entry[term_name] = term
        submissions.append(submission_entry)


# Split theme A and B
themeA_submissions = []
themeB_submissions = []
for submission in submissions:
    if submission['theme'] == "1":
        themeA_submissions.append(submission)
        submission['rank'] = "A" + str(themeA_submissions.index(submission) + 1)
    elif submission['theme'] == "2":
        themeB_submissions.append(submission)
        submission['rank'] = "B" + str(themeB_submissions.index(submission) + 1)


def generate_random_image(size=(1024, 1024)):
    # Generate an array of random pixel values
    random_image_array = np.random.randint(256, size=(size[0], size[1], 3), dtype=np.uint8)
    # Create an image from the array
    return Image.fromarray(random_image_array)


# generate images and store in file
def generate_image(submission):
    for filename in os.listdir(output_path):
        if filename.strip('.png').split('_')[-1] == submission['name']:
            print(filename + " already exists, ignored.")
            return
    # Check if debug flag is on
    if debug:
        image = generate_random_image()
    else:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=submission['prompt'],
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
        else:
            print(f"Failed to get image. Status code: {response.status_code}")
            return

    # Store in file
    out_file_path = os.path.join(output_path, submission['rank'] + "_" + submission['name'] + ".png")
    submission['outfile'] = out_file_path
    image.save(out_file_path)
    print(f"Image generated successfully: {out_file_path}")
    return


# Running the tasks in parallel
Parallel(n_jobs=n_jobs)(delayed(generate_image)(submission) for submission in submissions)


# Render
content = "# 作品一览\n"
# render themeA
content += "## " + themes[0] + "\n"
for submission in themeA_submissions:
    content += ("### 作品 " + str(submission['rank']) + "\n")
    content += f"{submission['caption']}\n\n"
    content += f'<img src="{submission["rank"]}_{submission["name"]}.png" alt="{submission["rank"]}_{submission["name"]}" align="left" style="zoom:50%;" />\n\n\n\n'
# render themeB
content += "## " + themes[1] + "\n"
for submission in themeB_submissions:
    content += ("### 作品 " + str(submission['rank']) + "\n")
    content += f"{submission['caption']}\n\n"
    content += f'<img src="{submission["rank"]}_{submission["name"]}.png" alt="{submission["rank"]}_{submission["name"]}" align="left" style="zoom:50%;" />\n\n\n\n'

with open(os.path.join(output_path, "output.md"), "w") as outfile:
    outfile.write(content)
