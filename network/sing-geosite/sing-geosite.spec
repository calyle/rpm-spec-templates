#
# spec file for package sing-geosite
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

Name:           sing-geosite
Version:        VERSION
Release:        1%{?dist}
Summary:        Geosite Database and Rule Sets for sing-box

License:        CC-BY-SA-4.0 GPL-3.0-or-later
URL:            https://github.com/SagerNet/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  git
Requires:       sing-box, sing-geosite-db, sing-geosite-rule-set
BuildArch:      noarch

%description
Geosite Database and Rule Sets for sing-box

%package        db
Summary:        Geosite Database for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    db
Geosite Database for sing-box

%package        rule-set
Summary:        Geosite Rule Sets for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    rule-set
Geosite Rule Sets for sing-box


%prep
%autosetup


%build


%install
# install sing-geosite-db
git checkout release
install -Dm644 geosite*.db -t %{buildroot}%{_datadir}/sing-box/geosite-db
# install sing-geosite-rule-set
git checkout rule-set
install -Dm644 geosite-*.srs -t %{buildroot}%{_datadir}/sing-box/geosite-rule-set

git checkout main




%files
%license LICENSE

%files db
%license LICENSE
%dir %{_datadir}/sing-box/geosite-db
%{_datadir}/sing-box/geosite-db/*

%files rule-set
%license LICENSE
%dir %{_datadir}/sing-box/geosite-rule-set
%{_datadir}/sing-box/geosite-rule-set/*


%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog