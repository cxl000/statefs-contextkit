Summary: Statefs-Contextkit bridge for Qt4
Name: statefs-contextkit
Version: x.x.x
Release: 1
License: LGPLv2
Group: System Environment/Tools
URL: http://github.com/nemomobile/statefs-contextkit
Source0: %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(statefs) >= 0.3.1
BuildRequires: cmake >= 2.8
BuildRequires: pkgconfig(cor) >= 0.1.4
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtXml)
BuildRequires: contextkit-devel

%description
Adapter to use Contextkit API to access statefs and statefs
provider to reuse contextkit providers

%package provider
Summary: Provider to expose contextkit providers properties
Group: System Environment/Libraries
Requires: statefs-loader-qt4
Requires: statefs >= 0.3.2
%description provider
Provider exposes all contextkit providers properties

%package subscriber-qt4
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs
%description subscriber-qt4
Contextkit property interface using statefs instead of contextkit

%package subscriber-qt4-devel
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs-contextkit-subscriber-qt4
Requires: contextkit-devel >= 0.5.39
%description subscriber-qt4-devel
Contextkit property interface using statefs instead of contextkit

%prep
%setup -q

%build
%cmake -DUSEQT=4
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d -D -p -m755 %{buildroot}%{_sharedstatedir}/statefs/hooks
# workaround to allow bridge to be reregistered on contextkit cfg changes
ln -sf %{_bindir}/statefs-contextkit-register %{buildroot}%{_sharedstatedir}/statefs/hooks/prestart-contextkit-register

%clean
rm -rf %{buildroot}

%files provider
%defattr(-,root,root,-)
%{_libdir}/statefs/libprovider-contextkit.so
%{_bindir}/statefs-contextkit-register
%{_sharedstatedir}/statefs/hooks/prestart-contextkit-register

%files subscriber-qt4
%defattr(-,root,root,-)
%{_libdir}/libcontextkit-statefs-qt4.so

%files subscriber-qt4-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/contextkit-statefs-qt4.pc

%post provider
statefs register --statefs-type=qt4  %{_libdir}/statefs/libprovider-contextkit.so || :
