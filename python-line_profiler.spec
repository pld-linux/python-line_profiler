#
# Conditional build:
%bcond_with	doc		# don't build doc (not provided by package)
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	line_profiler
Summary:	module for doing line-by-line profiling of functions
Summary(pl.UTF-8):	Moduł do optymalizacji linia po linii kodu funkcji
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	1.0
Release:	3
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/l/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	2f8352acfedf83f701a564583db5e14d
URL:		https://github.com/rkern/line_profiler
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
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
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
%attr(755,root,root) %{py3_sitedir}/_line_profiler.cpython-*m.so
%attr(755,root,root) %{_bindir}/kernprof
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
