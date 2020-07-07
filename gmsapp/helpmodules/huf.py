import os

def handle_uploaded_file(f,filename):
    os.chdir('gmsapp/attachment')
    with open(filename, 'wb+') as destination:

        for chunk in f.chunks():
            destination.write(chunk)
