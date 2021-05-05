# Replication package

## Running the package

### Requirements
[Docker](https://www.docker.com/)

*or*

See [`Dockerfile`](./Dockerfile) for installed packages and dependencies
and install them locally

### Steps

1. Build the docker image
    ```shell
    docker build --pull --rm -f "Dockerfile" -t pbr-lightweight:latest "."
    ```
2. Run docker image with [`run-docker.sh`](./run-docker.sh) bash script or use the command within manually.  
    **Note:** For Docker Desktop for Windows users with WSL1, use
    ```shell
    DOCKER=docker.exe ./run-docker.sh
    ```
3. Inside the container execute `./run-everything.sh`  
    **Note:** Second stage, after mutation testing, requires user input, see [`create-classifier.sh`](./create-classifier.sh)
4. Results can be found in folder `data`, copy the results out with `docker cp`
