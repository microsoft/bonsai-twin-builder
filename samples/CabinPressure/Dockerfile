# Get base image
FROM centos:7.8.2003

# Install basic dependencies
RUN yum update -y && yum upgrade -y && yum install -y \
    unzip java-11-openjdk-headless \
    gcc gcc-c++ \
    bzip2-devel gmp-devel mpfr-devel libmpc-devel \
    cmake make wget zlib-devel ant openssl-devel libgfortran5.x86_64 \
    libffi-devel \
  && rm -rf /var/lib/apt/lists/*

# Install Python 3.7
RUN wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
RUN tar xzf Python-3.7.3.tgz
WORKDIR Python-3.7.3
RUN ./configure --enable-optimizations --enable-shared --prefix=/usr/local LDFLAGS="-Wl,--rpath=/usr/local/lib"
RUN make -j$(nproc) && make install
RUN alias python='/usr/local/bin/python3'
RUN alias pip='/usr/local/bin/pip3'
RUN pip3 install --upgrade pip

# Copy resources from host machine
COPY ./TwinBuilderConnector/ /TwinBuilderConnector
COPY ./samples/CabinPressure/ /samples/CabinPressure/
WORKDIR /samples/CabinPressure
ENV LD_LIBRARY_PATH=/samples/CabinPressure/demo_package_online/Resources/python_runtime_demo/twin_runtime:/samples/CabinPressure/demo_package_online/Resources/python_runtime_demo/twin_runtime/lib
RUN pip install -r /TwinBuilderConnector/requirements.txt
CMD python3 /samples/CabinPressure/main.py
