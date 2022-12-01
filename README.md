If You have a CTF (Capture The Flag) that reads input from stdin and send output to stdout, you can use this script to support mutliple clients over the network.

The CTF executable will be run on a docker, so each client will receive a sterile and isolated environment to play with.

This script can run several CTF's in parallel (on different ports)

When a client connects to the port, the CTF docker container will be run, and all that is written to the port will be sent to it's stdin, and all it's output will be written back to the port.

This CTF server contains a simple CTF example.

How to use:
1. Create your ctf docker:
    - Write your own dockerfile (see example in Dockerfile_random)
        - Copy relevant files to /usr/src/ctf/ using the `COPY` command
        - Run your executable like this: `CMD ["python3", "ctf_docker_server.py", "{YOUR_EXE_NAME}"]`
    - build the docker (`docker build -f Dockerfile_{your_docker_name} -t {your_docker_name} .`)
2. Write a config file `ctf_server.cfg`. Each line contains the docker name and the desired port:
    - `{your_docker_name}  {port_number}`
3. Install required python packages: `python3 -m pip install -r requirements.txt`
4. Run the server `sudo python3 ctf_server.py`

Note:
- Your application must cancel stdout buffering. On a C program you can do this by calling: `setvbuf(stdout, NULL, _IONBF, 0);`





