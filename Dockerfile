FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server openssh-client \
    python3 python3-pip \
    openmpi-bin libopenmpi-dev \
    sudo iputils-ping net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir mpi4py

RUN useradd -m -s /bin/bash mpiuser && echo "mpiuser:mpiuser" | chpasswd

RUN mkdir /var/run/sshd

USER mpiuser
WORKDIR /home/mpiuser
RUN ssh-keygen -t rsa -f /home/mpiuser/.ssh/id_rsa -N "" && \
    cat /home/mpiuser/.ssh/id_rsa.pub >> /home/mpiuser/.ssh/authorized_keys && \
    chmod 700 /home/mpiuser/.ssh && \
    chmod 600 /home/mpiuser/.ssh/authorized_keys

USER root

COPY hosts /home/mpiuser/hosts
RUN chown mpiuser:mpiuser /home/mpiuser/hosts

RUN echo "Host *\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null" \
    >> /etc/ssh/ssh_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
