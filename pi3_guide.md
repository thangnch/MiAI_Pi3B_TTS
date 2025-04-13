# Làm máy Pi 3

Status: Việc cần làm ngay

1. Link OS: https://drive.google.com/drive/folders/1xpYca5w_XCePnwziQUeTDM9HBRwxD2jd?usp=drive_link
2. Github phần mềm: https://github.com/thanhtantran/paroli-on-orangepi
3. Model: https://huggingface.co/thanhtantran/piper-paroli-rknn-model
4. Link sản phẩm: https://orangepi.vn/shop/orange-pi-3b-chip-rk3566-wifi5-bt5-ram-4gb
5. Mã giảm giá: miai_orangepi3b, giảm 5% trên giá bán lẻ 1300k
6. 

| 1 | Install OS | Download from GDrive. Etcher (or other) write to SD

Plus SD, keyboard and monitor → start.

Insert some photo |
| --- | --- | --- |
| 2 | Visit github link | https://github.com/thanhtantran/paroli-on-orangepi3 |
| 3 | Instal rknpu lib, | git clone [https://github.com/Pelochus/ezrknn-toolkit2](https://github.com/Pelochus/ezrknn-toolkit2)

cd ezrknn-toolkit2

sudo bash [install.sh](http://install.sh/) |
| 4 | install git-lfs to clone models (which is large size)
 | (. /etc/lsb-release && curl -s [https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh](https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh) | sudo env os=ubuntu dist="${DISTRIB_CODENAME}" bash)
sudo apt-get install git-lfs |
| 5 | Install libs | sudo apt install -y cmake build-essential
sudo apt install -y libxtensor-dev nlohmann-json3-dev libspdlog-dev libopus-dev libfmt-dev libjsoncpp-dev
sudo apt install -y espeak-ng libespeak-ng-dev libogg-dev libsoxr-dev |
| 6 | Install drogon | cd ~
sudo apt install libssl-dev pkg-config libbotan-2-dev libc-ares-dev uuid-dev doxygen
sudo apt-get install zlib1g-dev
git clone [https://github.com/drogonframework/drogon](https://github.com/drogonframework/drogon)
cd drogon
git submodule update --init --recursive
mkdir build
cd build
sudo cmake ..
sudo make -j4
sudo make install |
| 7 | Install libopusenc | cd ~
wget [https://archive.mozilla.org/pub/opus/libopusenc-0.2.1.tar.gz](https://archive.mozilla.org/pub/opus/libopusenc-0.2.1.tar.gz)
tar -xvzf libopusenc-0.2.1.tar.gz
cd libopusenc-0.2.1
./configure
make -j4
sudo make install
sudo apt-get install pulseaudio |
| 8 | Download model | cd ~
git clone [https://huggingface.co/thanhtantran/piper-paroli-rknn-model](https://huggingface.co/thanhtantran/piper-paroli-rknn-model) |
| 9 | Clone runtime ONNX | cd ~
wget [https://github.com/microsoft/onnxruntime/releases/download/v1.14.1/onnxruntime-linux-aarch64-1.14.1.tgz](https://github.com/microsoft/onnxruntime/releases/download/v1.14.1/onnxruntime-linux-aarch64-1.14.1.tgz)
tar -xvf onnxruntime-linux-aarch64-1.14.1.tgz |
| 10 | Clone piper-phoemize | cd ~
wget [https://github.com/rhasspy/piper-phonemize/releases/download/2023.11.14-4/piper-phonemize_linux_aarch64.tar.gz](https://github.com/rhasspy/piper-phonemize/releases/download/2023.11.14-4/piper-phonemize_linux_aarch64.tar.gz)
tar -xvf piper-phonemize_linux_aarch64.tar.gz |
| 11 | build the app | git clone [https://github.com/thanhtantran/paroli-on-orangepi](https://github.com/thanhtantran/paroli-on-orangepi)
cd paroli-on-orangepi
sudo apt-get update
sudo apt-get install libonnxruntime-dev
mkdir build && cd build
cmake .. -DUSE_RKNN=ON -DORT_ROOT=/root/onnxruntime-linux-aarch64-1.14.1 -DPIPER_PHONEMIZE_ROOT=/root/piper_phonemize -DCMAKE_BUILD_TYPE=Release
make -j4 |
| 12 | Copy | cp -r ~/piper_phonemize/share/espeak-ng-data/ . |
| 13 | Test | ./paroli-cli --encoder /root/piper-paroli-rknn-model/encoder_vi.onnx --decoder /root/piper-paroli-rknn-model/decoder_vi-3568.rknn -c ~/piper-paroli-rknn-model/config-vi.json |
| 14 | API  | ./paroli-server --encoder /root/piper-paroli-rknn-model/encoder_vi.onnx --decoder /root/piper-paroli-rknn-model/decoder_vi-3568.rknn -c ~/piper-paroli-rknn-model/config-vi.json --ip 0.0.0.0 --port 8848 |
| 15 | Test API | curl http://localhost[:8848](http://192.168.68.139:8848/)[/api/v1/synthesise](http://your.server.address:8848/api/v1/synthesise) -X POST -H 'Content-Type: application/json' -d '{"text": "To be or not to be, that is the question"}' > test.opus |