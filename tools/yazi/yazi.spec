#
# spec file for package yazi 
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}

%if 0%{?fedora}
%global vergen_git_sha Fedora
%elif 0%{?suse_version}
%global vergen_git_sha openSUSE
%elif 0%{?el8} || 0%{?el9}
%global vergen_git_sha RedHat
%else
%global vergen_git_sha %{_os}
%endif

Name:           yazi
Version:        VERSION
Release:        1%{?dist}
Summary:        Blazing fast terminal file manager written in Rust, based on async I/O
License:        MIT
Group:          Productivity/Text/Utilities
URL:            https://github.com/sxyazi/yazi
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Requires:       file

BuildRequires:  gcc, curl
%if ! 0%{?rhel}
BuildRequires:  ImageMagick
%endif

Recommends:     ffmpeg
Recommends:     jq
%if 0%{?suse_version}
Recommends:     7zip
Recommends:     poppler-tools
Recommends:     fd
%else
Recommends:     p7zip
Recommends:     p7zip-plugins
Recommends:     poppler-utils
Recommends:     fd-find
%endif
Recommends:     ripgrep
Recommends:     fzf
Recommends:     zoxide
Recommends:     resvg
Recommends:     ImageMagick
Recommends:     git
Recommends:     chafa

%description
Yazi (means "duck") is a terminal file manager written in Rust, based on non-blocking async I/O. It aims to provide an efficient, user-friendly, and customizable file management experience.


%package        bash-completion
Summary:        Bash Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description bash-completion
The official bash completion script for %{name}.

%package fish-completion
Summary:        Fish Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description fish-completion
The official fish completion script for %{name}.

%package zsh-completion
Summary:        ZSH Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for %{name}.

%prep
%autosetup -p1

# Oniguruma fails to compile because gcc15 defaults to std=gnu23
%if 0%{?fedora} >= 42
  %global optflags %{optflags} -std=gnu17
%endif

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
export YAZI_GEN_COMPLETIONS=true
export VERGEN_GIT_SHA=%{vergen_git_sha}
cargo build --release --locked


%install
install -Dsm755 target/release/%{name}             %{buildroot}%{_bindir}/%{name}
install -Dsm755 target/release/ya                  %{buildroot}%{_bindir}/ya
install -Dm 644 yazi-boot/completions/%{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm 644 yazi-boot/completions/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
install -Dm 644 yazi-boot/completions/_%{name}     %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm 644 yazi-cli/completions/ya.bash       %{buildroot}%{_datadir}/bash-completion/completions/ya
install -Dm 644 yazi-cli/completions/ya.fish       %{buildroot}%{_datadir}/fish/vendor_completions.d/ya.fish
install -Dm 644 yazi-cli/completions/_ya           %{buildroot}%{_datadir}/zsh/site-functions/_ya

%if ! 0%{?rhel}
install -Dm 644 assets/%{name}.desktop             %{buildroot}%{_datadir}/applications/%{name}.desktop
for r in 16 24 32 48 64 128 256; do
    install -dm755 "%{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps"
    magick assets/logo.png -resize "${r}x${r}" "%{buildroot}%{_datadir}/icons/hicolor/${r}x${r}/apps/yazi.png"
done
%endif

%check
export YAZI_GEN_COMPLETIONS=true
export VERGEN_GIT_SHA=%{vergen_git_sha}
source "$HOME/.cargo/env"
cargo test --all


%files
%license LICENSE LICENSE-ICONS
%doc README.md
%{_bindir}/%{name}
%{_bindir}/ya
%if ! 0%{?rhel}
%{_datadir}/icons/*
%{_datadir}/applications/*
%endif

%files bash-completion
%{_datadir}/bash-completion

%files fish-completion
%{_datadir}/fish

%files zsh-completion
%{_datadir}/zsh

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See Github for full changelog