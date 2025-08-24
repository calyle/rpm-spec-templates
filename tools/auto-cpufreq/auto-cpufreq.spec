#
# spec file for package auto-cpufreq
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

Name:           auto-cpufreq
Version:        VERSION
Release:        1%{?dist}
Summary:        Automatic CPU speed & power optimizer for Linux

License:        LGPL-3.0-or-later
URL:            https://github.com/AdnanHodzic/%{name}
Source0:        %{name}-%{version}.tar.gz
Source1:        auto-cpufreq
Source2:        _auto-cpufreq
Source3:        auto-cpufreq.fish
Patch1:         001-fix-icon-n-style-locations.patch
Patch2:         002-fix-other-icon-path.patch
Patch3:         003-fix-auto_cpufreq-service.patch
Patch4:         004-fix-path-in-core.patch

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros, systemd-rpm-macros
BuildRequires:  python3dist(pip)
BuildRequires:	python3dist(poetry-dynamic-versioning)
BuildRequires:  python3dist(poetry-core)
BuildRequires:  git
%if 0%{?fedora}
Requires:	python3
Requires:	dmidecode
Requires:	python3-inotify, python3-distro, python3-psutil, python3-click, python3-gobject, python3-requests, python3-urwid, python3-pyasyncore
Requires:	cairo, gobject-introspection, cairo-gobject, gtk3
%endif

%description
Automatic CPU speed & power optimizer for Linux. Actively monitors laptop battery state, CPU usage, CPU temperature, and system load, ultimately allowing you to improve battery life without making any compromises.


%package        bash-completion
Summary:        Bash completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description    bash-completion
Bash command line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description    zsh-completion
Zsh command line completion support for %{name}.

%package        fish-completion
Summary:        Fish completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
Fish command line completion support for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files auto_cpufreq
install -Dm644 scripts/org.auto-cpufreq.pkexec.policy -t %{buildroot}%{_datadir}/polkit-1/actions
install -Dm644 images/icon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -Dm644 scripts/auto-cpufreq-gtk.desktop -t %{buildroot}%{_datadir}/applications
install -Dm644 scripts/auto-cpufreq.service     -t %{buildroot}/usr/lib/systemd/system
install -Dm755 scripts/cpufreqctl.sh            -t %{buildroot}%{_datadir}/%{name}/scripts
install -Dm755 scripts/auto-cpufreq-install.sh  -t %{buildroot}%{_datadir}/%{name}/scripts
install -Dm755 scripts/auto-cpufreq-remove.sh   -t %{buildroot}%{_datadir}/%{name}/scripts
install -Dm644 scripts/style.css                -t %{buildroot}%{_datadir}/%{name}/scripts
install -Dm644 images/icon.png                  -t %{buildroot}%{_datadir}/%{name}/images
install -Dm644 %{SOURCE1}                       -t %{buildroot}%{_datadir}/bash-completion/completions
install -Dm644 %{SOURCE2}                       -t %{buildroot}%{_datadir}/zsh/site-functions
install -Dm644 %{SOURCE3}                       -t %{buildroot}%{_datadir}/fish/vendor_completions.d

%post
if [ "$1" -eq 1 ]; then
  echo -e 'Important notice: the daemon installer provided does not work, instead run the following command:\n'
  echo -e 'systemctl enable --now auto-cpufreq\n'
  echo -e 'To view live log, run:\n'
  echo -e 'auto-cpufreq --stats\n'
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
if [ "$1" -eq 0 ]; then
  rm -f /usr/bin/cpufreqctl.auto-cpufreq
fi


%files -n %{name} -f %{pyproject_files}
%license LICENSE
%doc README.md auto-cpufreq.conf-example
%{_bindir}/%{name}
%{_bindir}/%{name}-gtk
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/polkit-1/actions/org.auto-cpufreq.pkexec.policy
/usr/lib/systemd/system/*

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*


%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog
