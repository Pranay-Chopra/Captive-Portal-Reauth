install:
	@echo "Checking and Installing Python Dependencies: "; \
	python3 -m pip install playwright systemd-python requests; \
	playwright install-deps; \
	playwright install; \
	@echo "Enter username: " \
	@read user; \
	echo "Enter password: "; \
	read -s pass; \
	sed "s|USERNAME_PLACEHOLDER|$$user|g; s|PASSWORD_PLACEHOLDER|$$pass|g" portal.py > portal_configured.py; \
	mkdir -p ~/.local/bin; \
	cp portal_configured.py ~/.local/bin/portal.py; \
	mkdir -p ~/.config/systemd/user; \
	cp portal-reauth.service ~/.config/systemd/user/portal.service; \
	systemctl --user daemon-reload; \
	systemctl --user enable portal-reauth.service; \
	systemctl --user start portal-reauth.service; \
	echo "Installed and running."

uninstall:
	systemctl --user stop portal-reauth.service || true
	systemctl --user disable portal-reauth.service || true
	rm -f ~/.config/systemd/user/portal-reauth.service
	rm -f ~/.local/bin/portal.py
	systemctl --user daemon-reload
	@echo "Removed."
