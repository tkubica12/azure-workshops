FROM ubuntu:18.04 
ENV PSW_VERSION=2.11 
RUN apt-get update && apt-get install -y wget gnupg
RUN ["/bin/bash", "-c", "wget -r -l1 --no-parent -nd -A *sgx_$(echo ${PSW_VERSION//./_})_bionic_custom_version.cfg https://download.01.org/intel-sgx/sgx_repo/ubuntu/apt_preference_files/"] 
RUN ["/bin/bash", "-c", "mv *sgx_$(echo ${PSW_VERSION//./_})_bionic_custom_version.cfg /etc/apt/preferences.d/intel-sgx.pref"]
RUN echo "deb [arch=amd64] https://download.01.org/intel-sgx/sgx_repo/ubuntu bionic main" | tee /etc/apt/sources.list.d/intel-sgx.list && wget -qO - https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | apt-key add -
RUN echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/18.04/prod bionic main" | tee /etc/apt/sources.list.d/msprod.list && wget -qO - https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN apt-get update && apt-get install -y clang-7 libssl-dev gdb libprotobuf10  libsgx-dcap-ql libsgx-quote-ex az-dcap-client open-enclave git

COPY * / 
WORKDIR / 
ENV SGX_AESM_ADDR=1 
CMD ./start_host enclave.signed
