#
# spec file for package mise
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global         debug_package %{nil}
%global         pkgname mise

Name:           %{pkgname}
Version:        VERSION
Release:        1%{?dist}
Summary:        The front-end to your dev env

License:        MIT
URL:            https://github.com/jdx/%{pkgname}
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Patch0:         mise-fix-metadata-auto.diff

BuildRequires:  gcc, curl, openssl, openssl-devel, zlib, zlib-devel, perl


%description
The front-end to your dev env

%package        bash-completion
Summary:        Bash completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion, usage
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description    bash-completion
Bash command line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       zsh, usage
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description    zsh-completion
Zsh command line completion support for %{name}.

%package        fish-completion
Summary:        Fish completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       fish, usage
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
Fish command line completion support for %{name}.

%package        fish-setup-file
Summary:        Fish setup script for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description    fish-setup-file
Fish setup script for %{name}

%package        setup-file
Summary:        Setup script for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash
Supplements:    (%{name} and bash)
BuildArch:      noarch

%description    setup-file
Setup script for %{name}

%prep
%autosetup -p1

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
cargo install cargo-license
# build release
cargo build --release --all-features
cargo license --color never > LICENSE.dependencies
./target/release/%{pkgname} completion zsh  > target/_%{pkgname}
./target/release/%{pkgname} completion bash > target/%{pkgname}
./target/release/%{pkgname} completion fish > target/%{pkgname}.fish

cat << 'EOF' > target/%{pkgname}.sh
# Activate mise. See https://mise.jdx.dev/installing-mise.html#shells
[ "$SHELL" == "/bin/bash" ] && eval "$(mise activate bash)"
[ "$ZSH_NAME" == "zsh" ] && eval "$(mise activate zsh)"
EOF

cat << 'EOF' > target/%{pkgname}_cf.fish
# Activate mise. See https://mise.jdx.dev/installing-mise.html#shells
if [ "$MISE_FISH_AUTO_ACTIVATE" != "0" ]
  mise activate fish | source
end
EOF


%install
install -Dspm755 -T target/release/%{pkgname} %{buildroot}%{_bindir}/%{pkgname}
install -Dpm644  -T man/man1/%{pkgname}.1     %{buildroot}%{_mandir}/man1/%{pkgname}.1
install -Dpm644  -T target/_%{pkgname}        %{buildroot}%{_datadir}/zsh/site-functions/_%{pkgname}
install -Dpm644  -T target/%{pkgname}         %{buildroot}%{_datadir}/bash-completion/completions/%{pkgname}
install -Dpm644  -T target/%{pkgname}.fish    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{pkgname}.fish
install -Dpm644  -T target/%{pkgname}.sh      %{buildroot}%{_sysconfdir}/profile.d/%{pkgname}.sh
install -Dpm644  -T target/%{pkgname}_cf.fish %{buildroot}%{_sysconfdir}/fish/conf.d/%{pkgname}.fish
install -dm755  %{buildroot}/usr/lib/%{pkgname}
touch           %{buildroot}/usr/lib/%{pkgname}/.disable-self-update


%files
%license LICENSE LICENSE.dependencies
%{_bindir}/%{pkgname}
%{_mandir}/man1/*
%dir /usr/lib/%{pkgname}
/usr/lib/%{pkgname}/.disable-self-update

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*

%files fish-setup-file
%{_sysconfdir}/fish/*

%files setup-file
%{_sysconfdir}/profile.d/*

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog
