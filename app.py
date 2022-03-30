import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("redirection")
            return redirect(request.url)
        file = request.files.get( 'file' )
        file = file if file  else request.files.getList( 'file' )
        if not file:
            return

        file = request.files.get( 'file' )
        if file:
            img_bytes = file.read()
            class_name ,class_id = get_prediction( image_bytes=img_bytes )
            return render_template( 'result.html', list=[ { 'id': class_id, 'name': class_name } ] )
        else: 
            final = [ ]
            for file in request.files.getList( 'file' ):
                img_bytes = file.read()
                class_name ,class_id = get_prediction( image_bytes=img_bytes )
                final.append( { 'id': class_id, 'name': class_name } )
            return render_template( 'result.html', list=final )
    return render_template( 'index.html' )


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
