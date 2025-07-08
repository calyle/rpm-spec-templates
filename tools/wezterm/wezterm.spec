#
# spec file for package wezterm
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global          _build_id_links none
%global          debug_package %{nil}

Name:            wezterm
Version:         VERSION
Release:         1%{?dist}
Summary:         Wez's Terminal Emulator.
License:         MIT
URL:             https://github.com/wez/%{name}
Source0:         %{url}/archive/refs/heads/main.zip

%if 0%{?suse_version}
Requires: dbus-1, fontconfig, openssl, libxcb1, libxkbcommon0, libxkbcommon-x11-0, libwayland-client0, libwayland-egl1, libwayland-cursor0, Mesa-libEGL1, libxcb-keysyms1, libxcb-ewmh2, libxcb-icccm4
%else
Requires: dbus, fontconfig, openssl, libxcb, libxkbcommon, libxkbcommon-x11, libwayland-client, libwayland-egl, libwayland-cursor, mesa-libEGL, xcb-util-keysyms, xcb-util-wm
%endif
BuildRequires: gcc, gcc-c++, make, curl, fontconfig-devel, openssl-devel, libxcb-devel, libxkbcommon-devel, libxkbcommon-x11-devel, wayland-devel, xcb-util-devel, xcb-util-keysyms-devel, xcb-util-image-devel, xcb-util-wm-devel, git, unzip

%if 0%{?suse_version}
BuildRequires: Mesa-libEGL-devel
%else
BuildRequires: mesa-libEGL-devel
%endif
%if 0%{?fedora} >= 41
BuildRequires: openssl-devel-engine
%endif

%description
wezterm is a terminal emulator with support for modern features
such as fonts with ligatures, hyperlinks, tabs and multiple
windows.

%prep
unzip %{sources}
cd %{name}-main
# read file `.gitmodules`
if [ ! -f .gitmodules ]; then
    echo ".gitmodules file not found!"
    exit 1
fi

# extract `path` and `url` for every submodule, and clone them
while IFS= read -r line; do
    if [[ $line =~ path\ =\ (.*) ]]; then
        path="${BASH_REMATCH[1]}"
    elif [[ $line =~ url\ =\ (.*) ]]; then
        url="${BASH_REMATCH[1]}"
        echo "Cloning $url into $path..."
        git clone "${url}" "${path}"
    fi
done < .gitmodules

%build
cd %{name}-main
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env

cargo build --release       -p wezterm-gui -p wezterm -p wezterm-mux-server       -p strip-ansi-escapes

%install
cd %{name}-main
set -x
cd .
install -Dm755  assets/open-wezterm-here          -t %{buildroot}%{_bindir}
install -Dsm755 target/release/wezterm            -t %{buildroot}%{_bindir}
install -Dsm755 target/release/wezterm-mux-server -t %{buildroot}%{_bindir}
install -Dsm755 target/release/wezterm-gui        -t %{buildroot}%{_bindir}
install -Dsm755 target/release/strip-ansi-escapes -t %{buildroot}%{_bindir}
install -Dm644  assets/shell-integration/*        -t %{buildroot}%{_sysconfdir}/profile.d
install -Dm644  -T assets/shell-completion/zsh       %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644  -T assets/shell-completion/bash      %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644  -T assets/icon/terminal.png          %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.wezfurlong.wezterm.png
install -Dm644  -T assets/%{name}.desktop            %{buildroot}%{_datadir}/applications/org.wezfurlong.wezterm.desktop
install -Dm644  -T assets/wezterm.appdata.xml        %{buildroot}%{_datadir}/metainfo/org.wezfurlong.wezterm.appdata.xml
install -Dm644  -T assets/wezterm-nautilus.py        %{buildroot}%{_datadir}/nautilus-python/extensions/wezterm-nautilus.py

%files
%{_bindir}/open-wezterm-here
%{_bindir}/%{name}
%{_bindir}/wezterm-gui
%{_bindir}/wezterm-mux-server
%{_bindir}/strip-ansi-escapes
%dir %{_datadir}/zsh
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/128x128/apps/org.wezfurlong.wezterm.png
%{_datadir}/applications/org.wezfurlong.wezterm.desktop
%{_datadir}/metainfo/org.wezfurlong.wezterm.appdata.xml
%dir %{_datadir}/nautilus-python/
%{_datadir}/nautilus-python/extensions/wezterm-nautilus.py*
%{_sysconfdir}/profile.d/*

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See git for full changelog
