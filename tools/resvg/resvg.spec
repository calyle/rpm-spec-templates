#
# spec file for package resvg
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/calyle/rpm-spec-templates
#

%global debug_package %{nil}

%global crate resvg

Name:           %{crate}
Version:        VERSION
Release:        1%{?dist}
Summary:        SVG rendering library

License:        Apache-2.0 OR MIT
URL:            https://github.com/linebender/resvg
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc, curl

%description
resvg is an SVG rendering library.
It can be used as a Rust library, as a C library, and as a CLI application to render static SVG files.
The core idea is to make a fast, small, portable SVG library with the goal to support the whole SVG spec.
Features:
* Designed for edge-cases
* Safety
* Zero bloat
* Portable
* SVG preprocessing
* Performance
* Reproducibility

%files       -n %{crate}
%license LICENSE-APACHE
%license LICENSE-MIT
%license LICENSE.dependencies
%doc README.md AUTHORS CHANGELOG.md
%{_bindir}/resvg

%package -n usvg
Summary:        SVG simplification tool

%description -n usvg
usvg is a command-line utility to simplify SVG files based on a static
SVG Full 1.1 subset. It converts an input SVG to an extremely
simple representation, which is still a valid SVG:
* No basic shapes (rect, circle, etc), only paths
* Only simple paths
* All supported attributes are resolved
* Invisible elements are removed
* Comments will be removed
* DTD will be resolved
* CSS will be resolved
and so on.

%files -n usvg
%{_bindir}/usvg

%package -n lib%{name}
Summary:        SVG rendering library (C++/Qt API)

%description -n lib%{name}
An SVG rendering library (C++/Qt API).
This package contains shared library.

%files -n lib%{name}
%{_libdir}/lib%{name}.so

%package -n %{name}-devel
Summary:        SVG rendering library (C++/Qt API)
Requires:       lib%{name} = %{version}-%{release}

%description -n %{name}-devel
An SVG rendering library (C++/Qt API).
This package contains development files.

%files -n %{name}-devel
%{_includedir}/%{name}.h
%{_includedir}/ResvgQt.h
%{_libdir}/lib%{name}.a

%prep
%autosetup -n %{crate}-%{version} -p1

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
cargo install cargo-license

%build
source "$HOME/.cargo/env"
cargo build --release --all-features --all
cargo license --color never > LICENSE.dependencies

%install
install -Dspm 0755 ./target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dspm 0755 ./target/release/usvg %{buildroot}%{_bindir}/usvg
install -Dpm 0755 ./target/release/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so
install -Dpm 0644 ./target/release/lib%{name}.a %{buildroot}%{_libdir}/lib%{name}.a
install -Dpm 0644 ./crates/c-api/*.h -t %{buildroot}%{_includedir}/

%check
source "$HOME/.cargo/env"
cargo test --release --all-features --all

%ldconfig_scriptlets -n lib%{name}

%changelog
* DATE Jo Carllyle <96739684+calyle@users.noreply.github.com>
- See Github for full changelog