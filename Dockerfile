FROM zerohertzkr/dev:latest

COPY requirements.txt requirements.txt
RUN sudo apt-get update && \
    sudo apt-get install -y libpq-dev && \
    /home/zerohertz/miniconda/bin/pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt
