#Instructions for setting up LSQUIC with oqs:BoringSSL
#-----------------------------------------------------
#Assumptions: Ubuntu 20.04
#------------
#Build liboqs & OQS BoringSSL library:
#-----------------------------

sudo apt install -y cmake gcc ninja-build libunwind-dev pkg-config python3 python3-pytest python3-psutil python3-pytest-xdist golang libz-dev libevent-dev

cd ~
rm -rf oqs
mkdir oqs && cd oqs

git clone https://github.com/prchander/boringssl.git


BORINGSSL_DIR=$PWD/boringssl

#Build liboqs
#------------

git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs

rm -rf build
mkdir build && cd build

cmake -GNinja -DCMAKE_INSTALL_PREFIX=$BORINGSSL_DIR/oqs -DOQS_USE_OPENSSL=OFF ..

ninja
sudo ninja install

#Build OQS BoringSSL
#-------------------

cd $BORINGSSL_DIR
rm -rf build
mkdir build && cd build

cmake -DBUILD_SHARED_LIBS=ON -GNinja ..

ninja

#Build LSQUIC library
#--------------------

cd ~/oqs

git clone https://github.com/prchander/lsquic.git
cd lsquic

git submodule init
git submodule update

rm -rf build
mkdir build && cd build

cmake -DBORINGSSL_DIR=$BORINGSSL_DIR -DBORINGSSL_LIB_crypto=$BORINGSSL_DIR/build/crypto/libcrypto.so -DBORINGSSL_LIB_ssl=$BORINGSSL_DIR/build/ssl/libssl.so -GNinja ..

ninja
#ninja test

echo "Successfully completed installation."