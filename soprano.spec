#
# TODO:
# - pl
#
Summary:	soprano
#Summary(pl.UTF-8):	soprano
Name:		soprano
Version:	20070602
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	8785c5166b4c36bba29eb943c558c51d
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cmake
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	redland-devel
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Soprano.

#%description -l pl.UTF-8

%package devel
Summary:	Header files for soprano
Summary(pl.UTF-8):	Pliki nagłówkowe dla soprano
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for soprano.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla soprano.

%prep
%setup -q -n %{name}

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DQT_QMAKE_EXECUTABLE=%{_bindir}/qt4-qmake \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so*
%dir %{_libdir}/soprano
%attr(755,root,root) %{_libdir}/soprano/*.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/soprano
%{_includedir}/soprano/*.h
