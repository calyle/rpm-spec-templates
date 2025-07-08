#
# spec file for package neofetch
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

Name:           neofetch
Version:        VERSION
Release:        1%{?dist}
Summary:        CLI system information tool written in Bash

License:        MIT
URL:            https://github.com/dylanaraps/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
Requires:       bash >= 3.2
Requires:       bind-utils
Requires:       catimg
Requires:       coreutils
Requires:       gawk
Requires:       grep
Requires:       pciutils
Recommends:     caca-utils
Recommends:     ImageMagick
Recommends:     jp2a
Recommends:     w3m-img
Recommends:     xdpyinfo
Recommends:     xprop
Recommends:     xrandr
Recommends:     xrdb
Recommends:     xwininfo
 
%description
Neofetch displays information about your system next to an image,
your OS logo, or any ASCII file of your choice. The main purpose of Neofetch
is to be used in screenshots to show other users what OS/distribution you're
running, what theme/icons you're using and more.
 
%prep
%autosetup
sed 's,/usr/bin/env bash,/usr/bin/bash,g' -i neofetch
 
%build

%install
%make_install

%files
%{_bindir}/%{name}
%license LICENSE.md
%doc README.md
%{_mandir}/man1/%{name}.1*

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com> - VERSION-1
- Updated to VERSION
