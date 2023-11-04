from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'

@app.route('/', methods=['GET'])
def index():
    # Render the HTML page for file upload
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        column_name = request.form['column_name']
        match_value = request.form['match_value']
        group_name = request.form['group_name']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and column_name and match_value and group_name:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            df = pd.read_csv(filename)
            if column_name not in df.columns:
                return f"The column '{column_name}' does not exist in the CSV file.", 400
            
            matched_df = df[df[column_name].astype(str).str.strip() == match_value.strip()]

            rdg_content = generate_rdg(matched_df, group_name)
            processed_filename = f"processed_{file.filename}.rdg"
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            
            with open(processed_filepath, 'w') as rdg_file:
                rdg_file.write(rdg_content)
            
            return redirect(url_for('download_file', filename=processed_filename))

    return 'File upload error'

def prettify_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_rdg(df, group_name):
    root = ET.Element('RDCMan', programVersion="2.93", schemaVersion="3")
    file_node = ET.SubElement(root, 'file')
    group_node = ET.SubElement(file_node, 'group')
    properties_node = ET.SubElement(group_node, 'properties')
    ET.SubElement(properties_node, 'expanded').text = 'True'
    ET.SubElement(properties_node, 'name').text = group_name

    for index, row in df.iterrows():
        server_node = ET.SubElement(group_node, 'server')
        properties_node = ET.SubElement(server_node, 'properties')
        ET.SubElement(properties_node, 'displayName').text = row['FQDN']
        ET.SubElement(properties_node, 'name').text = row['IP Address']
        comment_text = f"Configuration Item :{row['Configuration Item Name']}"
        if 'Secret Server URL' in row and pd.notnull(row['Secret Server URL']):
            comment_text += f"\nSS URL:{row['Secret Server URL']}"
        ET.SubElement(properties_node, 'comment').text = comment_text

    return prettify_xml(root)

@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    download_folder = app.config['UPLOAD_FOLDER']
    file_path = os.path.join(download_folder, filename)
    
    if not os.path.isfile(file_path):
        return "File not found.", 404

    response = send_file(file_path, as_attachment=True, download_name=filename)
    os.remove(file_path)
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
