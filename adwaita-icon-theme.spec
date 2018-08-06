%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME default icons
Name:		adwaita-icon-theme
Version:	3.29.90
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	intltool
BuildRequires:	hicolor-icon-theme
BuildRequires:	icon-naming-utils >= 0.8.7
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildArch:	noarch
Requires:	hicolor-icon-theme
Requires(post):	gtk+3.0 >= 3.19
Requires(postun):gtk+3.0 >= 3.19

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
%setup -q

%build
%configure --enable-icon-mapping
%make

%install
%makeinstall_std

touch %{buildroot}%{_datadir}/icons/Adwaita/icon-theme.cache

#compatibility symlink
ln -s %{name}.pc %{buildroot}%{_datadir}/pkgconfig/gnome-icon-theme.pc

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
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache
%dir %{_datadir}/icons/Adwaita/*x*/
%{_datadir}/icons/Adwaita/*x*/*
%dir %{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable/*
%dir %{_datadir}/icons/Adwaita/scalable-up-to-32
%{_datadir}/icons/Adwaita/scalable-up-to-32/*
%exclude %{_datadir}/icons/Adwaita/cursors/
%{_var}/lib/rpm/filetriggers/gtk-icon-cache-adwaita.*

%files -n adwaita-cursor-theme
%{_datadir}/icons/Adwaita/cursors/

%files devel
%{_datadir}/pkgconfig/*.pc
