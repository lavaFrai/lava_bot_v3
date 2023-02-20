docker stop discord_bot
docker rm discord_bot
docker run -it -d --restart=always --name=discord_bot -p 80:5000/tcp $(docker build -q .)