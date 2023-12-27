# FROM inanimate/echo-server
FROM ubuntu:latest
COPY files/key.pub /root/.ssh/authorized_keys
# https://stackoverflow.com/questions/62299928/r-installation-in-docker-gets-stuck-in-geographic-area
RUN apt-get update && apt-get install -y openssh-server python3
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
EXPOSE 8000
# RUN pip3 install echo-server
COPY files/startup.sh /root/startup.sh
RUN chmod +x /root/startup.sh
# CMD ["/usr/sbin/sshd", "-D"]
CMD ["bash", "/root/startup.sh"]