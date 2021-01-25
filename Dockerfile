# ベースイメージとして python v3.6 を使用する
FROM continuumio/anaconda3:2020.07

# 以降の RUN, CMD コマンドで使われる作業ディレクトリを指定する
# コンテナ側のルート直下にworkdir / (任意)という名前の作業ディレクトリを作り移動する
WORKDIR /workdir

#Create the environment
COPY . /workdir
COPY environment.yml .


#Activate the environment, and make sure its activated
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"] 
# https://pythonspeed.com/articles/activate-conda-dockerfile/
RUN conda env create -f environment.yml
RUN conda install -c anaconda flask-login
RUN conda install -c anaconda tensorflow

#The code to run when the container is started
COPY iris.py .
CMD ["python","iris.py"]

EXPOSE 8080