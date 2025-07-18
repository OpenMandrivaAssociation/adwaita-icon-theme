%undefine _debugsource_packages
%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME default icons
Name:		adwaita-icon-theme
Version:	48.1
Release:    1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		https://www.gnome.org/
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:    meson
BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme
BuildRequires:	icon-naming-utils >= 0.8.7
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildArch:	noarch
Requires:	hicolor-icon-theme
Requires:	gtk+3.0 >= 3.19

# gnome-icon-theme and gnome-icon-theme-symbolic were merged
# into one pkg adwaita-icon-theme
%rename	gnome-icon-theme
%rename	gnome-icon-theme-symbolic

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%package -n adwaita-cursor-theme
Summary:	Adwaita cursor theme
Group:		Graphical desktop/GNOME
BuildArch:	noarch

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package devel
Summary:	Development files for adwaita-icon-theme
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
Development files for gnome-icon-theme

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson
%meson_build

%install
%meson_install

touch %{buildroot}%{_datadir}/icons/Adwaita/.icon-theme.cache
touch %{buildroot}%{_datadir}/icons/Adwaita/icon-theme.cache

#compatibility symlink
ln -s %{name}.pc %{buildroot}%{_datadir}/pkgconfig/gnome-icon-theme.pc

# automatic gtk icon cache update on rpm installs/removals
%transfiletriggerin -- %{_datadir}/icons/Adwaita
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_datadir}/icons/Adwaita &>/dev/null || :
fi

%transfiletriggerpostun -- %{_datadir}/icons/Adwaita
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_datadir}/icons/Adwaita &>/dev/null || :
fi

%files
%doc %{_datadir}/licenses/adwaita-icon-theme/COPYING*
%doc AUTHORS NEWS
%dir %{_datadir}/icons/Adwaita/
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache
%dir %{_datadir}/icons/Adwaita/*x*/
%{_datadir}/icons/Adwaita/*x*/*
%dir %{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable/*
%{_datadir}/icons/Adwaita/symbolic*
%{_datadir}/icons/Adwaita/.icon-theme.cache
%exclude %{_datadir}/icons/Adwaita/cursors/

%files -n adwaita-cursor-theme
%{_datadir}/icons/Adwaita/cursors/

%files devel
%{_datadir}/pkgconfig/*.pc
