# Generic helper to clean up the previous runs of the script.

hello:
	@echo "Usage: make clean"
	@echo " "
	@echo "This will destroy all the keys. Do this only for fresh key generation including the CA keys"
	@echo " "

clean:
	rm -rf ca/
	rm -rf client/
