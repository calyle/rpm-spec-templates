#
# spec file for package sing-geoip
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

Name:           sing-geoip
Version:        VERSION
Release:        1%{?dist}
Summary:        GeoIP Database and Rule Sets for sing-box

License:        CC-BY-SA-4.0 GPL-3.0-or-later
URL:            https://github.com/SagerNet/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  git
Requires:       sing-box, sing-geoip-db, sing-geoip-rule-set
BuildArch:      noarch

%description
GeoIP Database and Rule Sets for sing-box

%package        db
Summary:        GeoIP Database for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    db
GeoIP Database for sing-box

%package        rule-set
Summary:        GeoIP Rule Sets for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    rule-set
GeoIP Rule Sets for sing-box


%prep
%autosetup


%build


%install
# install sing-geoip-db
git checkout release
install -Dm644 geoip*.db -t %{buildroot}%{_datadir}/sing-box/geoip-db
# install sing-geoip-rule-set
git checkout rule-set
install -Dm644 geoip-*.srs -t %{buildroot}%{_datadir}/sing-box/geoip-rule-set

git checkout main




%files
%license LICENSE

%files db
%license LICENSE
%dir %{_datadir}/sing-box/geoip-db
%{_datadir}/sing-box/geoip-db/*

%files rule-set
%license LICENSE
%dir %{_datadir}/sing-box/geoip-rule-set
%{_datadir}/sing-box/geoip-rule-set/*


%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog
