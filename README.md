# dalle3-game

THU ITML 课题组2024年会小游戏（最后被砍了（悲

Everything is in `main.py`;  `get_url.py` is for testing.

### What is this

Given two themes, participants write their prompts. This script sends all prompts to Dalle-3 API for image generation, and outputs a markdown demonstrating generated images anonymously. Then everyone can vote for the best generated image.

### How to use

1. Fill in your API key.
2. Determine the submission format. The four given domains are required. You can adjust the order of these domains.
3. Collect participants' submissions and organize them in the format shown in  `submission.txt`. (Use `\tab` to seperate columns)
4. Run the script `main.py`.