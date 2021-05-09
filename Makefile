.PHONY: run clean temp asset

run: app.py venv
	venv/bin/python app.py

asset: asset/richmenu asset/class20s.json
asset/richmenu: gen_richmenu_image.py temp venv
	venv/bin/python gen_richmenu_image.py

asset/class20s.json: gen_class20s_json.py venv
	venv/bin/python gen_class20s_json.py

venv: requirements.txt requirements-dev.txt
	rm -rf venv
	python3.9 -m venv venv
	venv/bin/pip install -r requirements.txt -r requirements-dev.txt

clean:
	rm -rf venv temp

temp:
	mkdir -p temp
	curl -L https://3.bp.blogspot.com/-8NKYZTR2p3k/W-VEjTGpRGI/AAAAAAABQGg/NXH8bcXl7AUcuKaDVpzSCidakjdbOCMmQCLcBGAs/s800/smartphone_map_app_woman.png -o temp/smartphone_map_app_woman.png
	curl -L https://tanukifont.com/download/TanukiMagic_1_22.zip -o temp/TanukiMagic_1_22.zip
	unzip temp/TanukiMagic_1_22.zip -d temp
