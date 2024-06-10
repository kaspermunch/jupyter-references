import os
import ipynbname
import json
import re
regex = re.compile(r'\d+\s+"([^"]+)"')
references = {}
with open(os.path.abspath(ipynbname.name()+'.ipynb')) as f:
    notebook_json = json.load(f)
for cell in notebook_json['cells']:
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        for ref in regex.findall(source):
            author, year, title, doi = ref.split('\n')
            references[ref] = dict(author=author.strip(),
                                   year=year.strip(), 
                                   title=title.strip(),
                                   doi=doi.strip())
lst = []
for i, (key, ref) in enumerate(sorted(references.items())):
    lst.append(f"{i+1}. {ref['author']}, {ref['year']}, _{ref['title']}_, [{ref['doi']}](https://doi.org/{ref['doi'].replace('DOI:', '')})")
content = "\n".join(lst)
content = '## References\n\n' + content
    
#get_ipython().run_line_magic('load', '-n content') 

from IPython.core.magic import Magics, magics_class, line_magic
@magics_class
class MyMagics(Magics):
    @line_magic
    def load_next(self, line):
        self.shell.set_next_input(line, replace=True)
ip = get_ipython()
ip.register_magics(MyMagics)
get_ipython().run_line_magic('load_next', f"{content}") 


                                                                        