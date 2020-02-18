config.txt.patch: config.txt.orig config.txt
	diff -u config.txt.orig config.txt > config.txt.patch || true

10-wpa_supplicant.patch: 10-wpa_supplicant.orig 10-wpa_supplicant
	diff -u 10-wpa_supplicant.orig 10-wpa_supplicant > 10-wpa_supplicant.patch || true

setup.sh: generate.py 10-wpa_supplicant.patch config.txt.patch
	./generate.py setup.sh 10-wpa_supplicant.patch config.txt.patch
