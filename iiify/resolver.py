#!/usr/bin/env python

import requests
from configs import options, cors, approot, cache_root, media_root

archive = 'https://archive.org'
bookdata = '%s/BookReader/BookReaderJSON.php' % (archive)
# BookReader/BookReaderImages.php

# mediatype

def ia_resolver(identifier):
    """Resolves a iiif identifier to the resource's path on disk.

    Resolver returns the path of resource on the iiif server (as
    opposed to a remote storage host, like Internet Archive) and first
    fetches it, if it doesn't exist on disk..
    """
    path = os.path.join(media_root, identifier)
    metadata = requests.get('%s/metadata/%s' % (archive, identifier)).json()
    server = metadata.get('server', 'https://archive.org')
    subPrefix = metadata['dir']
    mediatype = metadata['mediatype']
    files = metadata['files']

    if not os.path.exists(path):
        if mediatype.lower() == 'image':
            f = next(f for f in files if f.lower().endswith('.jpg') \
                         and f['source'].lower() == 'original')

            r = requests.get(
            # r = ... (stream=True, allow_redirects=True)
            # r.iter_content(chunk_size=1024)
            # save to media dir as `id`
            pass


        elif mediatype.lower() == 'texts':
            f = next(f['name'] for f in files if
                     f['name'].endswith('_jp2.zip') and
                     f['format'] == 'Single Page Processed JP2 ZIP')
        
            r = requests.get(bookdata, data={
                    'server': server,
                    'itemPath': subPrefix,
                    'itemId': identifier
                    }).json()            

            # r = requests.get(...)  # request the specific page next
            # r = ... (stream=True, allow_redirects=True)
            # r.iter_content(chunk_size=1024)
            # save to media dir as `id`

    return os.path.join(media_root, identifier)