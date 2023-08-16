default:
	# User install
	# Run "make user-install" to install in ~/.local/
	# Run "make user-uninstall" to uninstall from ~/.local/

user-install:
	pip install -r requirements.txt
	install -Dm00644 application/snxui.desktop $(HOME)/.local/share/applications/snxui.desktop
	install -Dm00755 snxui.py $(HOME)/.local/bin/snxui
	install -Dm00644 application/snxui.png $(HOME)/.local/share/icons/snxui.png
	sed -i -e "s,Exec=.*,Exec=$(HOME)/.local/bin/snxui,g" $(HOME)/.local/share/applications/snxui.desktop

user-uninstall:
	-rm $(HOME)/.local/share/applications/snxui.desktop
	-rm $(HOME)/.local/bin/snxui
	-rm $(HOME)/.local/share/icons/snxui.png
