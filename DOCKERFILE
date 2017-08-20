FROM amazonlinux

WORKDIR /app
ADD AllTrailsNYUrls.out /app
ADD dockertestNY.py /app

RUN cd /app

RUN sudo yum install python-pip 
RUN sudo pip install beautifulsoup4
RUN sudo pip install selenium
RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
RUN sudo yum -y install nodejs 
RUN mkdir -p /app/node_modules/phantomjs
RUN npm install phantomjs --phantomjs_cdnurl=https://bitbucket.org/ariya/phantomjs/downloads


CMD [ "python", "./dockertestNY.py" ]
