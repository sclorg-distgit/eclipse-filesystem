%{?scl:%scl_package eclipse-filesystem}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

%global debug_package %{nil}

Name:           %{?scl_prefix}eclipse-filesystem
Version:        1.0
Release:        7.%{baserelease}%{?dist}
Summary:        Eclipse Platform Filesystem Layout
License:        EPL
URL:            http://www.eclipse.org/

# javapackages-tools defines %%{_javaconfdir} macro and owns that directory
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
Requires:       %{?scl_prefix_java_common}javapackages-tools
Requires:       %{?scl_prefix}runtime

%description
This package provides directories needed by the Eclipse platform and other
Eclipse plug-ins. This is abstracted out of the main Eclipse package due to
the need to build some Eclipse plug-ins before the Eclipse platform itself
without introducing circular dependencies.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# Generate Eclipse configuration file
cat <<EOCONF >eclipse.conf
# Eclipse platform root directory
eclipse.root=%{_libdir}/eclipse
# Location of architecture-independant dropins
eclipse.dropins.noarch=%{_datadir}/eclipse/dropins
# Location of architecture-independant droplets
eclipse.droplets.noarch=%{_datadir}/eclipse/droplets
# Location of architecture-dependant dropins
eclipse.dropins.archful=%{_libdir}/eclipse/dropins
# Location of architecture-dependant droplets
eclipse.droplets.archful=%{_libdir}/eclipse/droplets
# Comma-separated list of directories searched for external bundles
eclipse.bundles=%{_javadir},%{_jnidir},%{_javadir}-1.8.0,%{_jnidir}-1.8.0,%{_javadir}-1.7.0,%{_jnidir}-1.7.0,%{_javadir}-1.6.0,%{_jnidir}-1.6.0,%{_javadir}-1.5.0,%{_jnidir}-1.5.0
# Software collection ID (empty if not SCL)
scl.namespace=%{?scl}
# Software collection root directory (empty if not SCL)
scl.root=%{?_scl_root}
EOCONF
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# Platform bundles
install -m 755 -d %{buildroot}%{_libdir}/eclipse/features
install -m 755 -d %{buildroot}%{_libdir}/eclipse/plugins
# Archful dropins
install -m 755 -d %{buildroot}%{_libdir}/eclipse/dropins
# Archful droplets
install -m 755 -d %{buildroot}%{_libdir}/eclipse/droplets
# Noarch dropins
install -m 755 -d %{buildroot}%{_datadir}/eclipse/dropins
# Noarch droplets
install -m 755 -d %{buildroot}%{_datadir}/eclipse/droplets
# eclipse.conf
install -m 755 -d %{buildroot}%{_javaconfdir}
install -m 644 -p eclipse.conf %{buildroot}%{_javaconfdir}/
%{?scl:EOF}


%files
%dir %{_libdir}/eclipse
%dir %{_libdir}/eclipse/features
%dir %{_libdir}/eclipse/plugins
%dir %{_libdir}/eclipse/dropins
%dir %{_libdir}/eclipse/droplets
%dir %{_datadir}/eclipse
%dir %{_datadir}/eclipse/dropins
%dir %{_datadir}/eclipse/droplets
%config(noreplace) %{_javaconfdir}/eclipse.conf

%changelog
* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 1.0-7.2
- Ensure SCL runtime package is installed

* Fri Jul 22 2016 Mat Booth <mat.booth@redhat.com> - 1.0-7.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 27 2015 Roland Grunberg <rgrunber@redhat.com> - 1.0-6
- Add support for p2 Droplets.

* Tue Aug 25 2015 Mat Booth <mat.booth@redhat.com> - 1.0-5
- Don't use EOF since it may conflict with SCL-isation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-3
- Generate and install eclipse.conf

* Mon Sep 08 2014 Mat Booth <mat.booth@redhat.com> - 1.0-2
- Suppress debuginfo package generation

* Tue Aug 26 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial package
