#
# spec file for package zellij
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

%ifarch         x86_64
%define         arch amd64
%endif
%ifarch         aarch64
%define         arch arm64
%endif

Name:           zellij
Version:        VERSION
Release:        1%{?dist}
Summary:        Terminal workspace with batteries included
License:        MIT
URL:            https://github.com/zellij-org/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  perl, gcc, curl

%description
Zellij is a workspace aimed at developers, ops-oriented people and anyone who loves the terminal.
At its core, it is a terminal multiplexer (similar to tmux and screen), but this is merely its
infrastructure layer.

Zellij includes a layout system, and a plugin system allowing one to create plugins in any
language that compiles to WebAssembly.

%package bash-completion
Summary:        Bash completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description bash-completion
Bash command line completion support for %{name}.

%package zsh-completion
Summary:        Zsh completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
Zsh command line completion support for %{name}.

%package fish-completion
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
# Remove prebuilt binaries
rm -v zellij-utils/assets/plugins/*

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
# fetch deps
cargo fetch --locked
# Update env `RUSTFLAGS`
export RUSTFLAGS="-Copt-level=3 -Cdebuginfo=2 -Ccodegen-units=1 -Cstrip=none -Cforce-frame-pointers=yes"
# First rebuilt plugins we just deleted
# Note: RUSTFLAGS break linking with WASM-files, so we don't use the cargo_build-macro here
pushd default-plugins/compact-bar
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/status-bar
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/tab-bar
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/strider
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/session-manager
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/fixture-plugin-for-tests
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/configuration
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/plugin-manager
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/about
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/multiple-select
cargo --offline build --release --target=wasm32-wasip1
popd
pushd default-plugins/share
cargo --offline build --release --target=wasm32-wasip1
popd

# Move the results to the place they are expected
mv -v target/wasm32-wasip1/release/*.wasm zellij-utils/assets/plugins/

# Build zellij proper
cargo --offline build --release --features unstable
RUSTFLAGS='-C strip=symbols' cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --target all \
--prefix none --format '{l}: {p}' | sort -u | sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' > LICENSE.dependencies

for shell in "zsh" "bash" "fish"
do
  ./target/release/%{name} setup --generate-completion "$shell" > target/%{name}."$shell"
done

# get pandoc
pandoc_ver=$(curl -s https://api.github.com/repos/jgm/pandoc/releases/latest | grep -oP -m 1 '"tag_name": "\K(.*)(?=")')
curl -L -O https://github.com/jgm/pandoc/releases/download/${pandoc_ver}/pandoc-${pandoc_ver}-linux-%{arch}.tar.gz
tar xf pandoc-${pandoc_ver}-linux-%{arch}.tar.gz && rm -f pandoc-${pandoc_ver}-linux-%{arch}.tar.gz
chmod +x pandoc-${pandoc_ver}/bin/pandoc
# generate man doc
./pandoc-${pandoc_ver}/bin/pandoc docs/MANPAGE.md -s -t man -o target/%{name}.1

%install
install -Dsm755 -T target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644  -T ./target/%{name}.bash  %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644  -T ./target/%{name}.fish  %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm644  -T ./target/%{name}.zsh   %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644  -T ./target/%{name}.1     %{buildroot}%{_mandir}/man1/%{name}.1
install -Dm644  -T %{_builddir}/%{name}-%{version}/assets/logo.png         %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -Dm644  -T %{_builddir}/%{name}-%{version}/assets/%{name}.desktop  %{buildroot}%{_datadir}/applications/%{name}.desktop


install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -av example/themes %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE.md LICENSE.dependencies
%doc README.md docs/ARCHITECTURE.md docs/MANPAGE.md docs/TERMINOLOGY.md docs/THIRD_PARTY_INSTALL.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/themes
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%{_mandir}/man1/*

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See Github for full changelog
