#
# Conditional build:
%bcond_with	doc		# don't build doc (not provided by package)
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	line_profiler
Summary:	module for doing line-by-line profiling of functions
Summary(pl.UTF-8):	Moduł do optymalizacji linia po linii kodu funkcji
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	2.1
Release:	14
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/rkern/line_profiler/archive/%{version}.tar.gz
# Source0-md5:	bd1cb2ba21af02339beab7ddc3a69c66
URL:		https://github.com/rkern/line_profiler
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-Cython
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-ipython
BuildRequires:	python-prompt_toolkit
%endif
%if %{with python3}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel
BuildRequires:	python3-ipython
BuildRequires:	python3-modules
BuildRequires:	python3-prompt_toolkit
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
line_profiler will profile the time individual lines of code take to
execute. The profiler is implemented in C via Cython in order to
reduce the overhead of profiling

%description -l pl.UTF-8
line_profile wskazuje czas wykonywania poszczególnych linii kodu. Jest
zaimplementowany w C poprzez Cythona tak aby zredukować narzut
profilowania.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
line_profiler will profile the time individual lines of code take to
execute. The profiler is implemented in C via Cython in order to
reduce the overhead of profiling

%description -n python3-%{module} -l pl.UTF-8
line_profile wskazuje czas wykonywania poszczególnych linii kodu. Jest
zaimplementowany w C poprzez Cythona tak aby zredukować narzut
profilowania.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags} -DHAVE_GETTIMEOFDAY" \
%py_build %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags} -DHAVE_GETTIMEOFDAY" \
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py_sitedir}/kernprof.py[co]
%{py_sitedir}/line_profiler.py[co]
%attr(755,root,root) %{py_sitedir}/_line_profiler.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py3_sitedir}/kernprof.py
%{py3_sitedir}/line_profiler.py
%{py3_sitedir}/__pycache__
%attr(755,root,root) %{py3_sitedir}/_line_profiler.cpython-*.so
%attr(755,root,root) %{_bindir}/kernprof
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
