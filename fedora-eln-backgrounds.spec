Name:           fedora-eln-backgrounds
Version:        1.0
Release:        %autorelease
Summary:        Fedora ELN default desktop background

License:        CC-BY-SA-4.0
URL:            https://docs.fedoraproject.org/en-US/eln/
Source0:        https://github.com/fedora-eln/backgrounds/releases/download/v%{version}/%{name}-%{version}.tar.xz


BuildArch:      noarch

BuildRequires:  kde-filesystem
BuildRequires:  make
BuildRequires:  ImageMagick

Requires:       %{name}-budgie = %{version}-%{release}
Requires:       %{name}-gnome = %{version}-%{release}
Requires:       %{name}-kde = %{version}-%{release}
Requires:       %{name}-xfce = %{version}-%{release}
Requires:       %{name}-mate = %{version}-%{release}


%description
This package contains desktop backgrounds for the Fedora  ELN default theme.

%package        base
Summary:        Base images for Fedora ELN default background
License:        CC-BY-SA-4.0

%description    base
This package contains base images for Fedora ELN default background.

%package        gnome
Summary:        Fedora ELN default wallpaper for Gnome
Requires:       %{name}-base = %{version}-%{release}

%description    gnome
This package contains Gnome desktop wallpaper for the
Fedora ELN default theme.

%prep
%autosetup -n %{name}-%{version}


%build
%make_build


%install
%make_install

%files
%doc

%files base
%license CC-BY-SA-4.0 Attribution
%dir %{_datadir}/backgrounds/fedora-eln
%dir %{_datadir}/backgrounds/fedora-eln/default
%{_datadir}/backgrounds/fedora-eln/default/fedora-eln*.{png,xml}

%files gnome
%{_datadir}/gnome-background-properties/fedora-eln.xml
%dir %{_datadir}/gnome-background-properties/

%changelog
%autochangelog
