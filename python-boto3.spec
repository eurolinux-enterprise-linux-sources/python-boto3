%if 0%{?rhel} && 0%{?rhel} <= 8
%bcond_with python3
%else
%bcond_without python3
%endif

%global _with_tests 0


%global pypi_name boto3

Name:           python-%{pypi_name}
Version:        1.4.6
Release:        4%{?dist}
Summary:        The AWS SDK for Python

License:        ASL 2.0
URL:            https://github.com/boto/boto3
Source0:        %{pypi_name}-%{version}.tar.gz
Patch0:         bundled-botocore-jmespath.patch
# python-botocore bundled in python-s3transfer
#Requires:       python-botocore >= 1.5.0
# python-jmespath bundled in python-s3transfer
#Requires:       python2-jmespath >= 0.7.1
Requires:       python-s3transfer >= 0.1.10
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# python-botocore bundled in python-s3transfer
#BuildRequires:  python-botocore
#BuildRequires:  python-s3transfer

# Needed for tests
%if 0%{?_with_tests}
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  python-wheel
%endif
BuildArch:      noarch

%description
Boto3 is the Amazon Web Services (AWS) Software Development
Kit (SDK) for Python, which allows Python developers to
write software that makes use of services like Amazon S3 
and Amazon EC2.

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        The AWS SDK for Python

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-mock
BuildRequires:  python3-wheel
BuildRequires:  python3-botocore
BuildRequires:  python3-jmespath
BuildRequires:  python3-s3transfer
Requires:       python3-botocore >= 1.5.0
Requires:       python3-jmespath >= 0.7.1
Requires:       python3-s3transfer >= 0.1.10
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Boto3 is the Amazon Web Services (AWS) Software Development
Kit (SDK) for Python, which allows Python developers to
write software that makes use of services like Amazon S3 
and Amazon EC2.
%endif # with python3

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info
# Remove online tests
rm -rf tests/integration

# python-botocore and python-jmespath bundled in python-s3transfer
%patch0 -p1


%build
%py2_build
%if %{with python3}
%py3_build
%endif # with python3

%install
%if %{with python3}
%py3_install
%endif # with python3
%py2_install

%check
%if 0%{?_with_tests}
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif # with python3
%endif

%files -n python-%{pypi_name} 
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name} 
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Mon Feb 12 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.4.6-4
- Append python-botocore and python-jmespath bundled directories to
  search path where needed

  Resolves: rhbz#1509439

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.6-2
- Update to 1.4.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.4-1
- Update to 1.4.4

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.3-1
- Update to 1.4.3

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.2-2
- Rebuild for Python 3.6

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> 1.4.2-1
- Update to 1.4.2

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Thu Aug 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.4.0-1
- New upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.1-1
- New upstream release

* Tue Mar 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.3.0-1
- New upstream release

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.4-1
- New upstream release

* Thu Feb 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.3-3
- Fix python2- subpackage to require python-future

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.2.3-1
- Initial package.
