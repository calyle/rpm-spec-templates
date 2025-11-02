#
# spec file for package usage
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

Name:           usage
Version:        VERSION
Release:        1%{?dist}
Summary:        A spec and CLI for defining CLI tools.

License:        MIT
URL:            https://github.com/jdx/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc, curl


%description
Usage is a spec and CLI for defining CLI tools. Arguments, flags, environment variables, and config files can all be defined in a Usage spec. It can be thought of like OpenAPI (swagger) for CLIs.

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
%autosetup

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
# build release
cargo build --release
RUSTFLAGS='-C strip=symbols' cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --target all \
--prefix none --format '{l}: {p}' | sort -u | sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' > LICENSE.dependencies
./target/release/%{name} --completions bash > target/%{name}
./target/release/%{name} --completions zsh  > target/_%{name}
./target/release/%{name} --completions fish > target/%{name}.fish


%install
install -Dsm755 -T target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644  -T target/_%{name}        %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644  -T target/%{name}         %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644  -T target/%{name}.fish    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish


%files
%license LICENSE LICENSE.dependencies
%{_bindir}/%{name}

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*


%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See GitHub for full changelog
