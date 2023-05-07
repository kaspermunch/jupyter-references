        
import os
import sys
import ipynbname
import json
import re
from IPython.lib import clipboard
from IPython.core.magic import Magics, magics_class, line_magic

import bibtexparser
from thefuzz import fuzz, process

@magics_class
class MyMagics(Magics):
    
    @line_magic
    def replace_content(self, line):
        self.shell.set_next_input(line, replace=True)
        
ip = get_ipython()
ip.register_magics(MyMagics)

def cite(cb=None):
    if cb is None:
        cb = clipboard.osx_clipboard_get()
    bibtex_entries = re.findall(r'\@[^\@]+', cb)
    cite_list = []
    for i, entry in enumerate(bibtex_entries):

        match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)', entry, re.DOTALL)
        if match:
            url, year, title, author = match.groups()
            if len(bibtex_entries) == 1:
                cite_list.append(f'[({author} et al. {year})](https://doi.org/{url} "{title}")')
            else:
                if i == 0:
                    cite_list.append(f'[({author} et al., {year},](https://doi.org/{url} "{title}")')
                elif i+1 == len(bibtex_entries):
                    cite_list.append(f'[{author} et al. {year})](https://doi.org/{url} "{title}")')
                else:
                    cite_list.append(f'[{author} et al. {year},](https://doi.org/{url} "{title}")')
    content = ' '.join(cite_list)
    if content:
        get_ipython().run_line_magic('replace_content', f"{content}") 
    else:
        print('clipboard is not bibtex:', cb)
        
def incite(cb=None):
    if cb is None:
        cb = clipboard.osx_clipboard_get()
    bibtex_entries = re.findall(r'\@[^\@]+', cb)
    if len(bibtex_entries) > 1:
        print('clipboard has bibtex entries:', cb)
    else:
        match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)',
            cb, re.DOTALL)
        if match:
            ref_list = {}
            url, year, title, author = match.groups()
            content = f'{author} et al. [({year})](https://doi.org/{url} "{title}")'
            get_ipython().run_line_magic('replace_content', f"{content}") 
        else:
            print('clipboard is not bibtex:', cb)
        

def ref_format_callback(i, ref):
    #format authors
    last_names, first_names = zip(*[token.split(', ') for token in refs['author'].split(' and ')])
    if len(last_names) <= 3:
        last_names = last_names[:3]
    last_names = ', '.join(last_names[:-1]) + ' and ' + last_names[-1]
    ref['author'] = last_names
        
    return f"{i}. " + "{author}, {year},\n**{title}**,\n{doi}".format(**ref)


def sort_fun(ref):
    return ref['author']
    
    
def reflist(file_base_name=None, format_fun=ref_format_callback, sort_fun=sort_fun):

    with open('bibtex.bib') as bibtex_file:
        db = bibtexparser.load(bibtex_file)
        bib_database = {}
        for entry in db.entries:
            bib_database[entry['ID']] = entry

    regex = re.compile(r'https://doi.org/(\S+)\s+"')
    references = []
    if file_base_name is None:
        file_base_name = ipynbname.name()
    if type(file_base_name) is not list:
        file_base_names = [file_base_name]
    else:
        file_base_names = file_base_name
    for name in file_base_names:
        with open(os.path.abspath(name+'.ipynb')) as f:
            notebook_json = json.load(f)
        for cell in notebook_json['cells']:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                for doi in regex.findall(source):
                    ref = bib_database[doi]
                    references.append(ref)

    l = []
    for ref in sorted(references, key=sort_fun):
        if not l or ref['ID'] != l[-1]['ID']:
            l.append(ref)
    references = l

    ref_list = []
    for i, ref in enumerate(references):
        try:
            ref['title'] = ref['title'][1:-1]
            ref_list.append(format_fun(i+1, ref))
        except KeyError:
            print(f'Skipping invalid ref: {ref}', file=sys.stderr)

    content = "\n".join(ref_list)
    get_ipython().run_line_magic('replace_content', f"{content}") 
            
    
    