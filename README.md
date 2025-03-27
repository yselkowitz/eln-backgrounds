# fedora-eln-backgrounds
A set of default wallpapers for Fedora ELN

## Testing

One way to test these is to install them on your system
* obtain the src rpm, for example using
```bash
    wget https://github.com/fedora-eln/backgrounds/releases/download/v1.0/fedora-eln-backgrounds-1.0-1.eln145.src.rpm
```
* install tools to build an rpm file, [follow the guide](https://fedoramagazine.org/how-rpm-packages-are-made-the-source-rpm/):
```bash
    sudo dnf install fedora-packager
```
* then build the rpm
```bash
    sudo dnf builddep fedora-eln-backgrounds-1.0-1.eln145.src.rpm
    rpmbuild --rebuild fedora-eln-backgrounds-1.0-1.eln145.src.rpm
```
* to install the rpm go to the directory where it has been built, assuming the commands above have been used, the following should work
```bash
    cd rpmbuild/RPMS/noarch
```
* then install the base
```bash
    dnf install fedora-eln-backgrounds-base-1.0-1.eln145.src.rpm
```
* finally install backgrounds for your desktop, for example for KDE 
```bash
    dnf install fedora-eln-backgrounds-kde-1.0-1.eln145.src.rpm
```

The directory should also contain the following rpms

   * fedora-eln-backgrounds-1.0-1.eln145.src.rpm
   * fedora-eln-backgrounds-base-1.0-1.eln145.src.rpm
   * fedora-eln-backgrounds-gnome-1.0-1.eln145.src.rpm

* You can then change the wallpaper, for example on GNOME, right click on the desktop and a menu should appear. Click on the menu and choose *Change Background* then select one of the newly installed wallpapers.
