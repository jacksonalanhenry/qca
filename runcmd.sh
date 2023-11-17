docker run --rm -it --env=DISPLAY qca:latest python3 /app/main.py
docker run --rm -it -e DISPLAY=host.docker.internal:0 -v ~/qca/:/qca/ qca:latest python3 /qca/app/main.py
