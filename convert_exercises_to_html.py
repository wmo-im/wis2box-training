import markdown
import glob

local_path = 'topics/*/*.md'

filepaths = glob.glob(local_path)
if len(filepaths) == 0:
    print(f'No files found for pattern={local_path}')

index_file = open('topics/index.html','w')
index_file.write('<h1>Topics</h1>\n')
# loop over files in ../topics
for filepath in filepaths:
    print(filepath)
    with open(filepath, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    html_filepath = filepath.replace('.md','.html')
    with open(html_filepath, 'w') as f:
        f.write(html)
    delim = '/'
    if '\\' in html_filepath:
        delim = '\\'
    topic_url = html_filepath.replace(f'topics{delim}','')
    topic_title = topic_url.split(delim)[0]
    index_file.write(f'<a href="{topic_url}">{topic_title}</a></br>\n')
    