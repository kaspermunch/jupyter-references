        
import os
import sys
import ipynbname
import json
import re
from IPython.lib import clipboard
from IPython.core.magic import Magics, magics_class, line_magic

import bibtexparser
from thefuzz import fuzz, process

class left:
    def __rlshift__(self, df):
        "Left align columns of data frame: df << left()"
        left_aligned_df = df.style.set_properties(**{'text-align': 'left'})
        left_aligned_df = left_aligned_df.set_table_styles(
        [dict(selector = 'th', props=[('text-align', 'left')])])
        display(left_aligned_df)  
        
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
        

##########################

import nbformat
import ipynbname
import hashlib
import IPython
import ipylab
from IPython.display import Javascript
import time
import re

def save_notebook(file_path):
    start_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()
    display(Javascript('IPython.notebook.save_checkpoint();'))
    current_md5 = start_md5
    
    while start_md5 == current_md5:
        time.sleep(1)
        current_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()

def get_notebook_cells(notebook_path=None, cell_types=["markdown", "code", "raw"]):
    if not notebook_path:
        ip = get_ipython()
        if '__vsc_ipynb_file__' in ip.user_ns:
            notebook_path = ip.user_ns['__vsc_ipynb_file__']
        else:
            notebook_path = ipynbname.path()

    # save_notebook(notebook_path)
    # app = ipylab.JupyterFrontEnd()
    # app.commands.execute('docmanager:save')
    
    with open(notebook_path, "r", encoding="utf-8") as rf:
        nb = nbformat.read(rf, as_version=4)

    cells = [cell for i, cell in enumerate(nb.cells) if cell["cell_type"] in cell_types]
    return cells


def get_cell_source():
    cell_id = get_ipython().get_parent()["metadata"]["cellId"]
    cells = get_notebook_cells()
    for idx, cell in enumerate(cells):
        if cell["id"] == cell_id:
            return cell['source']

def format_ref():
    cell_content = get_cell_source()
    return re.sub(r'ref\([^)]*\)', 'REF', cell_content)

# # ref()

# print(format_ref())

# TODO: %cite and %incite should be custum line magics:

# bla bla bla bla
# %cite <bibtex entry> or else read from clipboard
# bla bla bla bla



##########################


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
    
    
def reflist(file_base_name=None, ref_file_name='readcube.json', format_fun=ref_format_callback, sort_fun=sort_fun):

    with open(ref_file_name) as f:
        if ref_file_name.endswith('.bib'):
            ref_entries = bibtexparser.load(f).entries
        elif ref_file_name.endswith('.json'):
            ref_entries = json.load(f)['items']
        else:
            assert 0
        bib_database = {}
        for entry in ref_entries:
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
            
import ipywidgets as widgets
import pandas as pd
from time import sleep



def search():
    Authors = widgets.Text(description='Authors', continuous_update=False, layout=widgets.Layout(width='30%'))
    Year = widgets.Text(description='Year', continuous_update=False, layout=widgets.Layout(width='140px'))
    Title = widgets.Text(description='Title', continuous_update=False, layout=widgets.Layout(width='30%'))
    Select = widgets.Text(description='Select', continuous_update=False, layout=widgets.Layout(width='140px'))

    def f(authors, year, title, select):
        df = pd.DataFrame(dict(ID=['10110:/asdfk.sd2421']*5, Authors=[authors]*5, Year=[year]*5, Title=[title]*5))
        df.set_index(df.index+1, inplace=True)
        if not select:
            with pd.option_context('display.max_colwidth', 100):
                left_aligned_df = df.style.set_properties(**{'text-align': 'left'})
                left_aligned_df = left_aligned_df.set_table_styles(
                [dict(selector = 'th', props=[('text-align', 'left')])])

                display(left_aligned_df)
        else:
            idx = list(map(int, select.split()))
            print('produce citation markdown for:', df.loc[idx])
            df.loc[idx].to_clipboard(index=False, header=False)
            print('selected bibtex entry copied to clipboard')
            out.close()
            clear_output()            
            return "THIS IS A BIBTEX ENTRY"            

    out = widgets.interactive_output(f, {'authors': Authors, 'year': Year, 'title': Title, 'select': Select})


    from IPython.display import clear_output
    print('Loading refernce database... (this is only done once)')

    import json
    # with open('/Users/kmt/Desktop/jupyter-references/readcube.json') as f:
    #     ref_db = json.load(f)['items']
    # ref_db[:1]

    sleep(1)
    clear_output()

    # widgets.VBox([widgets.VBox([Authors, Year, Title]), out])
    display(widgets.VBox([widgets.HBox([Authors, Year, Title, Select]), out]))

search()
