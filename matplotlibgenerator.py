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

import os
import re
import numpy as np
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

@app.route('/', methods=['GET', 'POST'])
def index():

    session['gproperty'] = \
        {'title' : '',
         'xlabel': '',
         'ylabel': '',
         'fontsize': 15}
         
    #-- method is POST when the submit button pressed --
    if request.method == 'POST':
        session['gproperty'] =  {'title' : request.form['title'],
                                 'xlabel': request.form['xlabel'],
                                 'ylabel': request.form['ylabel'],
                                 'fontsize': request.form['fontsize'] }
        session['rawdata'] = request.form['data']
        return redirect(url_for('generateimage'))

    return render_template('hello.html')   

#  --- next to do; value transfer without using session: 
#      can't avoid using database?

@app.route('/test/')
@app.route('/test/<gtitle>')
def generateimage(gtitle = None):

    #-- remove old png files --
    os.system('rm static/*.png')

    nameforhello = session['gproperty']['title']

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    g.imgfile = 'testimg' + timestamp + '.png'

    session['imgfile'] = 'testimg' + timestamp + '.png'

    #--- data processing : split string to numbers after strip spaces ---
    #    !!! Need Exception process for wrong data  !!!
    if session['rawdata'] != '':
        nlist = map(float, \
                        re.split('\s+|\n|\t|,', session['rawdata'].strip())) 
        t = nlist[0:][::2] #-- even elements
        s = nlist[1:][::2] #-- odd  elements
    else:
        t = np.arange(0, 2.0*np.pi, 0.02*np.pi)
        s = np.sin(t)

    tmpfont = session['gproperty']['fontsize']

    plt.plot(t,s, linewidth = 1.0)
    plt.xlabel(session['gproperty']['xlabel'], fontsize = tmpfont)
    plt.xticks(fontsize = tmpfont)
    plt.ylabel(session['gproperty']['ylabel'], fontsize = tmpfont)
    plt.yticks(fontsize = tmpfont)
    #plt.title(gtitle)

    plt.title(session['gproperty']['title'], fontsize = tmpfont)
    plt.grid(True)
    plt.savefig('static/' + session['imgfile'])
    #pylab.show()
    return render_template('hello.html', name = nameforhello)

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

