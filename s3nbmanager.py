import datetime

from tornado import web

import boto

from IPython.frontend.html.notebook.nbmanager import NotebookManager
from IPython.nbformat import current
from IPython.utils.traitlets import Unicode

class S3NotebookManager(NotebookManager):
    
    aws_access_key_id = Unicode('', config=True, help='AWS access key id.')
    aws_secret_access_key = Unicode('', config=True, help='AWS secret access key.')
    aws_bucket = Unicode('', config=True, help='Bucket name for notebooks.')
    
    def __init__(self, **kwargs):
        super(S3NotebookManager, self).__init__(**kwargs)
        self.s3_con = boto.connect_s3(self.aws_access_key_id, self.aws_secret_access_key)
        self.bucket = self.s3_con.get_bucket(self.aws_bucket)
    
    def load_notebook_names(self):
        self.mapping = {}
        keys = self.bucket.get_all_keys()
        ids = [k.name for k in keys]
        
        for id in ids:
            name = self.bucket.get_key(id).get_metadata('nbname')
            self.mapping[id] = name
    
    def list_notebooks(self):
        data = [dict(notebook_id=id,name=name) for id, name in self.mapping.items()]
        data = sorted(data, key=lambda item: item['name'])
        return data
    
    def read_notebook_object(self, notebook_id):
        if not self.notebook_exists(notebook_id):
            raise web.HTTPError(404, u'Notebook does not exist: %s' % notebook_id)
        try:
            key = self.bucket.get_key(notebook_id)
            s = key.get_contents_as_string()
        except:
            raise web.HTTPError(500, u'Notebook cannot be read.')
        
        try:
            # v1 and v2 and json in the .ipynb files.
            nb = current.reads(s, u'json')
        except:
            raise web.HTTPError(500, u'Unreadable JSON notebook.')
        # Todo: The last modified should actually be saved in the notebook document.
        # We are just using the current datetime until that is implemented.
        last_modified = datetime.datetime.utcnow()
        return last_modified, nb
    
    def write_notebook_object(self, nb, notebook_id=None):
        try:
            new_name = nb.metadata.name
        except AttributeError:
            raise web.HTTPError(400, u'Missing notebook name')
        
        if notebook_id is None:
            notebook_id = self.new_notebook_id(new_name)
    
        try:
            data = current.writes(nb, u'json')
        except Exception as e:
            raise web.HTTPError(400, u'Unexpected error while saving notebook: %s' % e)
        
        try:
            key = self.bucket.new_key(notebook_id)
            key.set_metadata('nbname', new_name)
            key.set_contents_from_string(data)
        except Exception as e:
            raise web.HTTPError(400, u'Unexpected error while saving notebook: %s' % e)

        self.mapping[notebook_id] = new_name
        return notebook_id
    
    def log_info(self):
        self.log.info("Serving notebooks from s3. bucket name: %s" % self.aws_bucket)
