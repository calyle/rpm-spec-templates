#
# spec file for package rust-starship
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%bcond check 1

%global debug_package %{nil}
%global crate starship

Name:           rust-starship
Version:        VERSION
Release:        1%{?dist}
Summary:        Minimal, blazing-fast, and infinitely customizable prompt for any shell

License:        ISC
# LICENSE.dependencies contains a full license breakdown
URL:            https://github.com/starship/starship
Source:         %{url}/archive/v%{version}/%{crate}-%{version}.tar.gz
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          starship-fix-metadata-auto.diff

BuildRequires:  rust-packaging, git

%global _description %{expand:
Minimal, blazing-fast, and infinitely customizable prompt for any shell! ☄🌌️.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
License:        ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR MIT OR Apache-2.0) AND BSD-3-Clause AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND (MIT AND Apache-2.0) AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND Unicode-3.0 AND Unlicense AND (Unlicense OR MIT) AND Zlib AND (Zlib OR Apache-2.0 OR MIT)

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/%{crate}

%package     -n %{crate}-bash-completion
Summary:        Bash Completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and bash-completion)
BuildArch:      noarch

%description -n %{crate}-bash-completion
Bash command line completion support for %{crate}.

%files       -n %{crate}-bash-completion
%{_datadir}/bash-completion/completions/%{crate}

%package     -n %{crate}-zsh-completion
Summary:        Zsh Completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and zsh)
BuildArch:      noarch

%description -n %{crate}-zsh-completion
Zsh command line completion support for %{crate}.

%files       -n %{crate}-zsh-completion
%{_datadir}/zsh/site-functions/_%{crate}

%package     -n %{crate}-fish-completion
Summary:        Fish completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and fish)
BuildArch:      noarch

%description -n %{crate}-fish-completion
Fish command line completion support for %{crate}.

%files       -n %{crate}-fish-completion
%{_datadir}/fish/vendor_completions.d/%{crate}.fish

%prep
%autosetup -n %{crate}-%{version} -p1

%build
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
RUSTFLAGS='-C strip=symbols' cargo build -j$(nproc) --all --release
RUSTFLAGS='-C strip=symbols' cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --target all \
--prefix none --format '{l}: {p}' | sort -u | sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' > LICENSE.dependencies

./target/release/%{crate} completions bash > target/%{crate}
./target/release/%{crate} completions zsh > target/_%{crate}
./target/release/%{crate} completions fish > target/%{crate}.fish

%install
install -Dspm 0755 target/release/%{crate} -t %{buildroot}%{_bindir}
install -Dpm644 target/%{crate}      -t %{buildroot}%{_datadir}/bash-completion/completions
install -Dpm644 target/_%{crate}     -t %{buildroot}%{_datadir}/zsh/site-functions
install -Dpm644 target/%{crate}.fish -t %{buildroot}%{_datadir}/fish/vendor_completions.d

%if %{with check}
%check
RUSTFLAGS='-C strip=symbols' cargo test -j$(nproc) --all --release
%endif

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See Github for full changelog