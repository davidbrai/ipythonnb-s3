# IPython notebook S3 store

[IPython notebook](http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html) manager which saves to [S3](http://aws.amazon.com/s3/).
Currently working with IPython dev branch.

By default the notebook server stores the notebook files in a local directory.  
This plugin seamlessly stores and reads the notebooks files from and to an S3 bucket.  
It uses the great [boto](https://github.com/boto/boto) package to communicate with AWS.

It requires credentials to an AWS account.


## How to use

The plugin is not yet available as an installable python package.

1. Place `s3nbmanager.py` somewhere accessible by your `PYTHONPATH`, site-packages folder for example.

2. Create a profile for your notebook server by running:   
    ```
    ipython profile create nbserver
    ```    

3. Edit your `ipython_notebook_config.py` file:

    ```python
    c.NotebookApp.notebook_manager_class = 's3nbmanager.S3NotebookManager'
    c.S3NotebookManager.aws_access_key_id = '<put your aws access key id here>'
    c.S3NotebookManager.aws_secret_access_key = '<put your aws secret access key here>'
    c.S3NotebookManager.aws_bucket = '<put the name of the bucket you want to use>'
    ```
