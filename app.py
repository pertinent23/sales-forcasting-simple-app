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
                class_name, class_id = get_prediction( image_bytes=img_bytes )
                isint = isinstance( class_id, int )
                final.append( { 
                    'id': class_id if isint else class_name, 
                    'name': class_name if isint else class_id
                } )
        return render_template( 'result.html', list=final )
    return render_template( 'index.html' )


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
