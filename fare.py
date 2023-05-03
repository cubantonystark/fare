'''
FARE - Fast Area Rendering at the Edge
Lightweight Fast Area Rendering tool for Law Enforcement, First Responders and military. Version 1.0
(C) 2022, Reynel Rodriguez, Silentblade Technologies, LLC.
Portions of this framework use Open Source Software from Nvidia, Inc. (https://github.com/NVlabs/instant-ngp)
Compile with: pyinstaller fare.py --onefile --icon D:\Projects\fare\static\floorplans\camera.ico --add-data "templates;templates" --add-data "static;static"
'''

import os, glob, shutil, ctypes, fnmatch, win32api, ntpath
from flask import Flask, request
from flask import render_template, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

#app = Flask(__name__, template_folder = 'templates')
app.config['TESTING'] = True
app.config["SESSION_REFRESH_EACH_REQUEST"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

os.system('python -m webbrowser -t "http://localhost:8080"')

@app.route('/')

def index():
	
	global working_dir
	
	def find(pattern, drive):
	
		result = []
	
		for root, dirs, files in os.walk(drive):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
					result.append(os.path.join(root, name))
		return result
	
	def get_drives():
	
		drives = win32api.GetLogicalDriveStrings()
		drives = drives.split('\000')[:-1]
	
		for drive in drives:
	
			result = find('beacon.txt', drive)
	
		filepath = result[0]
		path, file = ntpath.split(filepath)
		return path
	
	try:
		with open('file.txt', 'r') as filepath:
			
			working_dir = filepath.read()
			
	except FileNotFoundError:
		
		working_dir = get_drives()
		
		with open('file.txt', 'w') as filepath:
			
			filepath.write(str(working_dir))
	
	#read the templates folder and create an updated list of available assets
	main_dir = os.listdir(working_dir+'\\templates\\imagery\\')
	
	with open(working_dir+'\\templates\\index.html', 'w+') as index_file:
		
		index_file.write('<html>\r')
		index_file.write('<head>\r')
		index_file.write('<title>Assets</title>\r')
		index_file.write('<link rel="stylesheet" href="/static/bootstrap.min.css">\r') 
		index_file.write('<link rel="stylesheet" href="/static/font-awesome.min.css">\r')
		index_file.write('<style>\r')
		index_file.write('.center {\r')
		index_file.write('margin-left: auto;\r')
		index_file.write('margin-right: auto;\r')
		index_file.write('}\r')
		index_file.write('</style>\r')
		index_file.write('</head>\r')
		index_file.write('<body>\r')
		index_file.write('<br /><br /><br /><br /><br /><br />\r')
		index_file.write('<table class="table-bordered center">\r')
		index_file.write('<thead>\r')
		index_file.write('	<tr>\r')
		index_file.write('	<th class = "text-center" scope="col">Assets</th>\r')
		index_file.write('	</tr>\r')
		index_file.write('</thead>\r')
		index_file.write('<tbody>\r')
		index_file.write('	<tr>\r')
		index_file.write('	<td scope="row">&nbsp;</td>\r')
		index_file.write('	<tr>\r')		

		for file in main_dir:
			url = file.split("\\")
			total = len(url)-2
			link_name = url[total]
			line = '<td class = "text-center" scope="row">&nbsp;<a href = http://localhost:8080/render_asset?target='+str(link_name)+'>'+link_name.replace('_', ' ')+'</a>&nbsp;</td>\r'
			index_file.write('<tr>\r') 
			index_file.write(line)
		
		index_file.write('<tr>\r') 
		index_file.write('<td class = "text-center" scope="row">&nbsp;</td>\r')
		index_file.write('<tr>\r')      
		index_file.write('<td class = "text-center" scope="row"><a href = http://localhost:8080/new_asset>New</a></td>\r')      
		index_file.write('<tr>\r')    
		index_file.write('</table>')
		index_file.write('</body></html>\r')
		
	return render_template('index.html')


@app.route('/render_asset', methods = ['GET', 'POST'])

def render_asset():

	if request.method == 'GET':
		target = request.args.get('target')
	building = target

	files = [f for f in glob.glob(working_dir+'\\templates\\imagery\\'+target+'/info.dat')]
	map_file = target.lower()

	with open(files[0], "r") as infofile:

		data = infofile.readlines()

	parent_dir = os.listdir(working_dir+'\\templates\\imagery\\'+target)

	info_line1 = '&nbsp;<font size = 5>'+str(data[0])+'</font>'
	info_line2 = '&nbsp;<font size = 5>'+str(data[1])+'</font>'

	return_line = '<a href = http://localhost:8080/>Main Menu</a>\r' 
	#new_area_link = '<a href = http://localhost:8080/new_asset_area/>Add new Area</a>\r'

	with open(working_dir+'\\templates\\imagery\\'+target+'\\index.html', 'w+') as index_file:

		index_file.write('<html>\r')
		index_file.write('<head>\r')
		index_file.write('<title>Asset Explorer</title>\r')
		index_file.write('<link rel="stylesheet" href="/static/bootstrap.min.css">\r') 
		index_file.write('<link rel="stylesheet" href="/static/font-awesome.min.css">\r')
		index_file.write('<style>\r')
		index_file.write('.center {\r')
		index_file.write('margin-left: auto;\r')
		index_file.write('margin-right: auto;\r')
		index_file.write('}\r')
		index_file.write('</style>\r')
		index_file.write('</head>\r')
		index_file.write('<body>\r')
		
		index_file.write('<div class = "center">\r')
		index_file.write('<table class="table-bordered center">\r')
		index_file.write('<table width = 800 class="table-bordered center">\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row"><font size = 5>&nbsp;'+info_line1+'</font></td>\r')
		index_file.write('</tr>\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row"><font size = 5>&nbsp;'+info_line2+'</font></td>')
		index_file.write('<tr>\r')
		index_file.write('</table>\r')
		index_file.write('</div>\r')
		index_file.write('<br /><br />\r')
		
		index_file.write('<table class = "table-bordered" width = 250 border = 1 style="display: inline-block; float: left; ">\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row">&nbsp;<font size = 4>Areas</font></td>\r')      
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row">&nbsp;<font size = 5></font></td>\r')
		index_file.write('<tr>\r')

		for file in parent_dir:
			url = file.split("\\")
			total = len(url)-2
			link_name = url[total]
			if link_name == 'index.html' or link_name == 'blueprint.png' or link_name == 'info.dat' or link_name == 'blueprint.jpg':
				continue

			line = '<td width = 250 align = center valign = middle>&nbsp;<font size = 4><a href = http://localhost:8080/render_area?target='+str(link_name)+'&building='+building+'>'+link_name.replace('_', ' ')+'</a></font></td>\r'
			index_file.write('<tr>\r')
			index_file.write(line+'\r')
			index_file.write('<tr>\r')
		
		index_file.write('<td class = "text-center" scope="row">&nbsp;<font size = 5></font></td>\r')
		index_file.write('<tr>\r')		
		index_file.write('<td class = "text-center" scope="row">&nbsp;<a href = http://localhost:8080/new_asset_area?target='+target+'>Add new Area</a></td>\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row">&nbsp;<font size = 3>'+return_line+'</font></td>\r')
		index_file.write('</table>') 
		index_file.write('<table class = "table-centered" width = 1000 border = 1 style="display: inline-block; float: left">\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row">&nbsp;Asset Floorplan</td>\r')
		index_file.write('</tr>\r')
		index_file.write('<tr>\r')
		index_file.write('<td class = "text-center" scope="row"><img src = "/static/floorplans/'+str(map_file)+'.jpg" width = 900 height = 600></td>')
		index_file.write('<tr>\r')
		index_file.write('</table>')
		index_file.write('</table>\r')
		index_file.write('</body></html>\r')


	return render_template('imagery/'+target+'/index.html')


@app.route('/render_area', methods = ['GET', 'POST'])

def render_area():
	
	if request.method == 'GET':
		target = request.args.get('target', None)    
		building = request.args.get('building', None)   
		command = 'python '+working_dir+'\\neural_rendering\\scripts\\run.py --load_snapshot '+working_dir+'\\fare\\templates\\imagery\\'+str(building)+'\\'+str(target)+'\\snapshot.ingp --gui'
		os.system(command)

	return render_template('imagery/'+building+'/index.html')


@app.route('/ingest_asset', methods = ['POST'])

def ingest_asset():

	if request.method == 'POST':
		asset_name = request.form['asset_name']
		asset_address = request.form['asset_address']
		f = request.files['filename']

		if len(asset_name) == 0 or len(asset_address) == 0:
			render_template('index.html')

		else:

			filename = secure_filename(f.filename)
			
			extension = filename.split(".")
			
			try:
			
				if extension[1].lower() != 'jpg' or extension[1] is None:
					ctypes.windll.user32.MessageBoxW(0, "Only png files are accepted. PLease try again.", "Error", 0x1000)
					return redirect('http://localhost:8080/new_asset')					
					 
			except IndexError:
				
				pass
			
			asset_as_filename = asset_name.replace(' ', '_')
			f.save(working_dir+'\\static\\floorplans\\'+filename+'.jpg')
			shutil.move(working_dir+'\\static\\floorplans\\'+filename+'.jpg', working_dir+'\\static/floorplans\\'+asset_as_filename+'.jpg')

			if os.stat(working_dir+'\\static\\floorplans\\'+asset_as_filename+'.jpg').st_size == 0:
				os.unlink(working_dir+'\\static\\floorplans\\'+asset_as_filename+'.jpg')
				shutil.copy2(working_dir+'\\static\\floorplans\\blank.jpg', working_dir+'\\static/floorplans\\'+asset_as_filename+'.jpg')            

			try:

				os.mkdir(working_dir+'\\templates\\imagery\\'+asset_as_filename)

				with open(working_dir+'\\templates\\imagery\\'+asset_as_filename+'\\info.dat', 'w+') as info_file:
					info_file.write(asset_name+'\r')
					info_file.write(asset_address+'\r')

			except FileExistsError:

				return redirect('http://localhost:8080')

	return redirect('http://localhost:8080')


@app.route('/new_asset')

def new_asset():

	#return render_template('new_asset.html')
	return('''
			<html>
			<head>
			<title>New Asset</title>
			<link rel="stylesheet" href="/static/bootstrap.min.css"> 
			<link rel="stylesheet" href="/static/font-awesome.min.css">
			</head>
			<body>
			<br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
			<form class="form-horizontal form-md" enctype = "multipart/form-data" action = "http://localhost:8080/ingest_asset" method = "post">
			<fieldset>
			
			<!-- Asset name input-->
			<div class="form-group">
			<label class="col-md-4 control-label" for="textinput">Asset Name:</label>  
			<div class="col-md-4">
			<input id="asset_name" name="asset_name" type="text" class="form-control input-md" required="">
			</div>
			</div>
			<!-- Asset address input-->
			<div class="form-group">
			<label class="col-md-4 control-label" for="asset_address">Asset Address:</label>  
			<div class="col-md-4">
			<input id="asset_address" name="asset_address" type="text" class="form-control input-md">
				
			</div>
			</div>
			<!-- File Button --> 
			<div class="form-group">
			<label class="col-md-4 control-label" for="filename">Floor plan</label>
			<div class="col-md-4">
				<input id="filename" name="filename" class="input-file" type="file">
			</div>
			</div>
			<!-- Button -->
			<div class="form-group">
			<label class="col-md-4 control-label" for="submit"></label>
			<div class="col-md-4">
				<button id="submit" name="submit" class="btn btn-primary">Process</button>
			</div>
			</div>
			</fieldset>
			</form>
			</body>
			<html>
	''')

@app.route('/new_asset_area', methods = ['GET', 'POST'])

def new_asset_area():
	
	if request.method == 'GET':
		target = request.args.get('target')
	
	#return render_template('new_area.html')
	return('''
			<html>
			<head>
			<title>New Area</title>
			<link rel="stylesheet" href="/static/bootstrap.min.css"> 
			<link rel="stylesheet" href="/static/font-awesome.min.css">
			</head>
			<body>
			<br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
			<form class="form-horizontal form-md" enctype = "multipart/form-data" action = "http://localhost:8080/ingest_area" method = "post">
			<fieldset>
			
			<!-- Asset name input-->
			<div class="form-group">
			<label class="col-md-4 control-label" for="textinput">Area Name:</label>  
			<div class="col-md-4">
			<input id="asset_name" name="area_name" type="text" class="form-control input-md" required="">
			<input type = "hidden" name = "target" value = "'''+target+'''" />
			</div>
			</div>
			<!-- File Button --> 
			<div class="form-group">
			<label class="col-md-4 control-label" for="filename">Area file</label>
			<div class="col-md-4">
				<input id="filename" name="filename" class="input-file" type="file">
			</div>
			</div>
			<!-- Button -->
			<div class="form-group">
			<label class="col-md-4 control-label" for="submit"></label>
			<div class="col-md-4">
				<button id="submit" name="submit" class="btn btn-primary">Process</button>
			</div>
			</div>
			</fieldset>
			</form>
			</body>
			<html>
	''')


@app.route('/ingest_area', methods = ['POST']) #

def ingest_area():
	
	if request.method == 'POST':
		area_name = request.form['area_name']
		target = request.form['target']
		f = request.files['filename']
		
		area_name = area_name.replace(' ', '_')
	
		filename = secure_filename(f.filename)

		if len(area_name) == 0 or len(filename) == 0:
			return redirect('http://localhost:8080/render_asset?target='+target)	
		
		else:
			extension = filename.split(".")
			
			if extension[1] != 'ingp':
				ctypes.windll.user32.MessageBoxW(0, "Wrong Area file supplied. Please try again", "Error", 0x1000)
				return redirect('http://localhost:8080/new_asset_area?target='+target)
			
			os.mkdir(working_dir+'\\templates\\imagery\\'+target+'\\'+area_name)
			f.save(working_dir+'\\templates\\imagery\\'+target+'\\'+area_name+'\\'+filename)
		
	return redirect('http://localhost:8080/render_asset?target='+target)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 8080)
