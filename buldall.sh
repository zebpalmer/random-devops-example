cd app_b
docker build . -t registry.halo.sh/app-b:latest
docker push registry.halo.sh/app-b:latest
cd ../app_a
docker build . -t registry.halo.sh/app-a:latest
docker push registry.halo.sh/app-a:latest