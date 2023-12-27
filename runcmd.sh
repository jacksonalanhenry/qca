#docker run --rm -it --env=DISPLAY -v ~/qca/:/qca/ qca:latest python3 /qca/app/main.py
docker run --rm -it -e DISPLAY=host.docker.internal:0 -v ~/qca/:/qca/ qca:latest python3 /qca/app/main.py
#docker run --rm -it -e DISPLAY=$DISPLAY -v ~/qca/:/qca/ qca:latest python3 /qca/app/main.py
#viu ~/qca/fig.png
