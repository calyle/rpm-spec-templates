#
# spec file for package zsh-completions
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _build_id_links none
%global debug_package %{nil}

Name:           zsh-completions
Version:        VERSION
Group:          Development/Tools
Release:        1%{?dist}
Summary:        Additional completion definitions for Zsh.

License:        MIT
URL:            https://github.com/zsh-users/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       zsh

%description
Additional completion definitions for Zsh.


%prep
%autosetup


%build


%install
install -Dm644 src/_* -t %{buildroot}/usr/share/zsh/site-functions/


%files
%license LICENSE
%dir %{_datadir}/zsh
%{_datadir}/zsh/*


%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog
