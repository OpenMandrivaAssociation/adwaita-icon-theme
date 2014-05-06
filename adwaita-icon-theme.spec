%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME default icons
Name:		adwaita-icon-theme
Version:	3.13.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme
BuildRequires:	icon-naming-utils >= 0.8.7
BuildRequires:	gtk+2.0
BuildArch:	noarch
Requires:	hicolor-icon-theme
Requires(post):	gtk+2.0 >= 2.6.0
Requires(postun):gtk+2.0 >= 2.6.0

# gnome-icon-theme and gnome-icon-theme-symbolic were merged
# into one pkg adwaita-icon-theme
%rename	gnome-icon-theme
%rename	gnome-icon-theme-symbolic

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%package -n	adwaita-cursor-theme
Summary:	Adwaita cursor theme
Group:		Graphical desktop/GNOME
BuildArch:	noarch
Conflicts:	%{name} < 3.13.1-2

%description -n	adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%prep
%setup -q

%build
%configure2_5x --enable-icon-mapping
%make

%install
%makeinstall_std

touch %{buildroot}%{_datadir}/icons/Adwaita/icon-theme.cache

# automatic gtk icon cache update on rpm installs/removals
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %{buildroot}%{_var}/lib/rpm/filetriggers

cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-adwaita.filter << EOF
^./usr/share/icons/Adwaita/
EOF

cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-adwaita.script << EOF
#!/bin/sh
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --force --quiet /usr/share/icons/Adwaita
fi
EOF

chmod 755 %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-adwaita.script

%post
%update_icon_cache Adwaita

%postun
%clean_icon_cache Adwaita

%files
%doc AUTHORS NEWS README
%dir %{_datadir}/icons/Adwaita/
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache
%dir %{_datadir}/icons/Adwaita/*x*/
%{_datadir}/icons/Adwaita/*x*/*
%dir %{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable/*
%exclude %{_datadir}/icons/Adwaita/cursors/
%{_var}/lib/rpm/filetriggers/gtk-icon-cache-adwaita.*

%{_datadir}/pkgconfig/%{name}.pc

%files -n adwaita-cursor-theme
%{_datadir}/icons/Adwaita/cursors/
