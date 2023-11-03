from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'

@app.route('/', methods=['GET'])
def index():
    # Render the HTML page for file upload
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        match_key = request.form['match_key']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        
        if file and match_key:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Process the CSV
            df = pd.read_csv(filename)
            # Assuming the CSV has a column named as the match_key
            matched_df = df[df[match_key].notna()]
            
            # Save the processed CSV
            processed_filename = f"processed_{file.filename}"
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            matched_df.to_csv(processed_filepath, index=False)
            
            # Return a response or a redirect to download
            return redirect(url_for('download_file', filename=processed_filename))

    return 'File upload error'

@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    # Set the download path
    download_folder = app.config['UPLOAD_FOLDER']
    
    # Trigger the download
    response = send_from_directory(directory=download_folder, filename=filename, as_attachment=True)
    
    # Remove the file after download
    os.remove(os.path.join(download_folder, filename))
    
    return response

if __name__ == '__main__':
    app.run(debug=True)