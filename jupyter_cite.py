# def auth_year_cite():
#     match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)',
#         clipboard.osx_clipboard_get(), re.DOTALL)
#     if match:
#         url, year, title, author = match.groups()
#         return f'[({author}, {year})]({url} "{title}")'
# if __name__ == "__main__":
#     link_text = auth_year_cite()
#     get_ipython().run_line_magic('load', '-n link_text')
    
# import re
# from IPython.lib import clipboard
# cb = clipboard.osx_clipboard_get()
# match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)',
#     cb, re.DOTALL)
# if match:
#     url, year, title, author = match.groups()
#     link_text = f'[({author}, {year})](https://doi.org/{url} "{author} et al., {year},\n{title},\nDOI:{url}")'
#     get_ipython().run_line_magic('load', '-n link_text')    
#     # get_ipython().run_cell_magic('markdown', '', link_text)    
# else:
#     print('clipboard is not bibtex:', cb)

        
# import re
# from IPython.lib import clipboard

    
# from IPython.core.magic import Magics, magics_class, line_magic
# @magics_class
# class MyMagics(Magics):
#     @line_magic
#     def replace_content(self, line):
#         self.shell.set_next_input(line, replace=True)
# ip = get_ipython()
# ip.register_magics(MyMagics)
    
# cb = clipboard.osx_clipboard_get()
# bibtex_entries = re.findall(r'\@[^\@]+', cb)
# cite_list = []
# for i, entry in enumerate(bibtex_entries):
    
#     match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)', entry, re.DOTALL)
#     if match:
#         url, year, title, author = match.groups()
#         if len(bibtex_entries) == 1:
#             cite_list.append(f'[({author} {year})](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
#         else:
#             if i == 0:
#                 cite_list.append(f'[({author} {year},](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
#             elif i+1 == len(bibtex_entries):
#                 cite_list.append(f'[{author} {year})](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
#             else:
#                 cite_list.append(f'[{author} {year},](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')

# if cite_list:
#     content = ' '.join(cite_list)
#     # get_ipython().run_line_magic('load', '-n link_text')   
#     get_ipython().run_line_magic('replace_content', f"{content}") 
# else:
#     print('clipboard is not bibtex:', cb)
        
import re
from IPython.lib import clipboard

from IPython.core.magic import Magics, magics_class, line_magic
@magics_class
class MyMagics(Magics):
    @line_magic
    def replace_content(self, line):
        self.shell.set_next_input(line, replace=True)
ip = get_ipython()
ip.register_magics(MyMagics)

def _cite(cb=clipboard.osx_clipboard_get()):
    bibtex_entries = re.findall(r'\@[^\@]+', cb)
    cite_list = []
    for i, entry in enumerate(bibtex_entries):

        match = re.search(r'@\w+{([^,]+).*year = {(\d+)}.*title = {{(.*)}}.*author = {([^,]+)', entry, re.DOTALL)
        if match:
            url, year, title, author = match.groups()
            if len(bibtex_entries) == 1:
                cite_list.append(f'[({author} {year})](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
            else:
                if i == 0:
                    cite_list.append(f'[({author} {year},](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
                elif i+1 == len(bibtex_entries):
                    cite_list.append(f'[{author} {year})](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
                else:
                    cite_list.append(f'[{author} {year},](https://doi.org/{url} "{author} et al.\n{year}\n{title}\nDOI:{url}")')
    content = ' '.join(cite_list)
    if content:
        get_ipython().run_line_magic('replace_content', f"{content}") 
    else:
        print('clipboard is not bibtex:', cb)

if __name__ == "__main__":
    _cite()
    