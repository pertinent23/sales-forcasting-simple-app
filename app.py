import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            print("redirection")
            return redirect(request.url)
        files = request.files.getlist( 'files[]' )
        if not files:
            return
        
        final = [ ]
        for file in files:
            if file:
                img_bytes = file.read()
                id, name = get_prediction( image_bytes=img_bytes )
                final.append( { 
                    'id': id, 
                    'name': name
                } )
        return render_template( 'result.html', list=final )
    return render_template( 'index.html' )


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
