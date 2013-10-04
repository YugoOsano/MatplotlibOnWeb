#------
#  generate matplotlib graph on a web browser

#  reference:
#  http://a2c.bitbucket.org/flask/quickstart.html

#  Matplotlib on Heroku
#  http://stackoverflow.com/questions/18173104/deploy-matplotlib-on-heroku-failed-how-to-do-this-correctly

#  Before running this, activate env with:
#  env/Scripts/activate
#  easy_install Flask

from flask import Flask, request, session, g, redirect, url_for, send_from_directory
from flask import render_template
import pylab as plt
import datetime

app = Flask(__name__)

#UPLOAD_FOLDER = 'uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#--- SECRET_KEY is defined to use session object ---
app.config['SECRET_KEY']='development key'

#-- prepare the image file name -- 
imgfile = 'testimg.png'

@app.route('/')
def index():
    return render_template('hello.html')   

@app.route('/test/')
@app.route('/test/<gtitle>')
def generateimage(gtitle = None):

    nameforhello = 'Matplotlib'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    g.imgfile = 'testimg' + timestamp + '.png'
    session['imgfile'] = 'testimg' + timestamp + '.png'

    t = [0.0, 2.0, 10.0]
    s = [-1.0, 5.0, 20.0]

    plt.plot(t,s, linewidth = 1.0)
    plt.xlabel('time (s)')
    plt.ylabel('value (a.u.)')
    plt.title(gtitle)
    plt.grid(True)
    plt.savefig('static/' + session['imgfile'])
    #pylab.show()
    return render_template('hello.html', name = nameforhello)
    #return render_template('imageframe.html', imagefile = session['imgfile'])

@app.route('/show/')
def showimage():
    #if not hasattr(g, 'imgfile'):
    #    g.imgfile = 'testimg.png'
    return render_template('imageframe.html', imagefile = session['imgfile'])


#@app.route('/show/<filename>')
#def uploaded_file(filename):
#    filename = 'http://127.0.0.1:5000/uploads/' + filename
#    return render_template('imageframe.html', filename=filename)

#@app.route('/uploads/<filename>')
#def send_file(filename):
#    return send_from_directory(UPLOAD_FOLDER, filename)
    


if __name__ == '__main__':
    app.run(debug=True)

